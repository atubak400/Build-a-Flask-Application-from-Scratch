# Building a Flask Application from Scratch

## Step 1

![1a](./img/1a.png)

## Step 2

![1a](./img/1b.png)

## Step 3

![1a](./img/2a.png)

## Step 4

![1a](./img/2b.png)

## Step 5

![1a](./img/2c.png)

## Step 6

Create a form

![1a](./img/3a.png)

## Step 7

![1a](./img/3b.png)

## Step 8

Create greet.html in template directory

![1a](./img/3c.png)

## Step 9

Update app.py

![1a](./img/3d.png)

## Step 10

Run the application using `flask run` and visit the provided url

![1a](./img/3e.png)

## Step 11

Type in a name

![1a](./img/3ee.png)

==

## Step 12

![1a](./img/3f.png)

## Step 13

Introducing Jinja Template

![1a](./img/4aa.png)

## Step 14

![1a](./img/4bb.png)

## Step 15

![1a](./img/4cc.png)

## Step 16

Repeat step 10, 11 and 12 again to confirm that Jinja works

# Authentication and Database Connection

## Step 17

> Familiarize with Postgresql

* `https://www.youtube.com/watch?v=wTqosS71Dc4` - install postgresql on Mac video
* `https://postgresapp.com/downloads.html` - download website
* `https://www.youtube.com/watch?v=2rqMRkVvXcw` - install pgadmin on Mac
* `https://www.postgresql.org/ftp/pgadmin/pgadmin4/v7.8/macos/` - download website
* `https://www.youtube.com/watch?v=WFT5MaZN6g4` - pgAdmin Tutorial - How to Use pgAdmin
* `https://www.youtube.com/watch?v=0n41UTkOBb0&t` - install postgresql on windows video

## Step 18

run `code login.html register.html` and paste these code

* login.html
```
{% extends "layout.html" %}

{% block body %}
    <form action="/login" method="post">
        <input name="username" placeholder="Username" type="text" required>
        <input name="password" placeholder="Password" type="password" required>
        <button type="submit">Login</button>
    </form>
    <p>New user? <a href="/register">Register here</a>.</p>
{% endblock %}
```
and

* register.html
```
{% extends "layout.html" %}

{% block body %}
    <form action="/register" method="post">
        <input name="username" placeholder="Username" type="text" required>
        <input name="password" placeholder="Password" type="password" required>
        <button type="submit">Register</button>
    </form>
    <p>Already have an account? <a href="/login">Login here</a>.</p>
{% endblock %}
```

![login and Register](./img/7.png)


## Step 19

Create a Postgresql database in pgadmin. You can call the database Flask

![pgadmin](./img/8.png)

## Step 20

Run the code below to create a user table

![pgadmin](./img/9.png)

## Step 21

Run the code below to see your user table content

![pgadmin](./img/10.png)

## Step 22

update app.py to connect to database and handle login.html and register.html


```
from flask import Flask, render_template, request, redirect, url_for, session
import psycopg2
from werkzeug.security import generate_password_hash, check_password_hash

app = Flask(__name__)
app.secret_key = 'atuba_kingsley_??_990909'

# Database connection parameters
conn_params = {
    'dbname': 'Flask',
    'user': 'kingsleyatuba',
    'password': '',
    'host': 'localhost'
}

def get_db_connection():
    conn = psycopg2.connect(**conn_params)
    return conn

@app.route("/")
def index():
    if 'user_id' not in session:
        return redirect(url_for('login'))  # Redirect to login if the session is not set
    # Render index.html if the session is established
    return render_template("index.html")

@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password")

        conn = get_db_connection()
        cur = conn.cursor()
        cur.execute("SELECT * FROM users WHERE username = %s", (username,))
        user = cur.fetchone()
        print("User found:", user)  # Debug print
        cur.close()
        conn.close()

        if user and check_password_hash(user[2], password):
            session['user_id'] = user[0]  # Store the user's id in the session
            print("Password match!")  # Debug print
            return redirect(url_for('index'))
        else:
            print("Password mismatch!")  # Debug print
            return "Invalid username or password"

    return render_template("login.html")


@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]
        hashed_password = generate_password_hash(password)

        # Connect to the database
        conn = get_db_connection()
        cur = conn.cursor()

        # Insert the new user into the database
        cur.execute("INSERT INTO users (username, password) VALUES (%s, %s)", (username, hashed_password))
        conn.commit()

        # Close the database connection
        cur.close()
        conn.close()

        # Redirect to the login page after successful registration
        return redirect(url_for("login"))

    # If it's a GET request or the form submission was not valid
    return render_template("register.html")


@app.route("/greet", methods=["POST"])
def greet():
    name = request.form.get("name")
    return render_template("greet.html", name=name)


@app.route("/logout")
def logout():
    session.pop('user_id', None)  # Remove the user_id from the session
    return redirect(url_for('login'))


if __name__ == "__main__":
    app.run(debug=True)

```

![pgadmin](./img/app_old.png)



# Application modularization (or breaking app.py into seperate files)

## Step 23

run `code routes.py database.py` and paste these code

* ### routes.py
```
from flask import session, redirect, url_for, render_template, request
from werkzeug.security import check_password_hash, generate_password_hash
from database import get_db_connection


def index():
    if 'user_id' not in session:
        return redirect(url_for('login'))  # Redirect to login if the session is not set
    # Render index.html if the session is established
    return render_template("index.html")

def login():
    if request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password")

        conn = get_db_connection()
        cur = conn.cursor()
        cur.execute("SELECT * FROM users WHERE username = %s", (username,))
        user = cur.fetchone()
        print("User found:", user)  # Debug print
        cur.close()
        conn.close()

        if user and check_password_hash(user[2], password):
            session['user_id'] = user[0]  # Store the user's id in the session
            print("Password match!")  # Debug print
            return redirect(url_for('index'))
        else:
            print("Password mismatch!")  # Debug print
            return "Invalid username or password"

    return render_template("login.html")

def register():
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]
        hashed_password = generate_password_hash(password)

        # Connect to the database
        conn = get_db_connection()
        cur = conn.cursor()

        # Insert the new user into the database
        cur.execute("INSERT INTO users (username, password) VALUES (%s, %s)", (username, hashed_password))
        conn.commit()

        # Close the database connection
        cur.close()
        conn.close()

        # Redirect to the login page after successful registration
        return redirect(url_for("login"))

    # If it's a GET request or the form submission was not valid
    return render_template("register.html")

def greet():
    name = request.form.get("name")
    return render_template("greet.html", name=name)

def logout():
    session.pop('user_id', None)  # Remove the user_id from the session
    return redirect(url_for('login'))
```

> Code Explanation

* index Function:

Checks if user_id is in the session. If not, it redirects to the login page.
If user_id is present, it renders the index.html template, indicating the user is logged in.

* login Function:
Handles the login functionality.
On a POST request (when the user submits the login form):
Retrieves the username and password from the form.
Connects to the database to find a user with the given username.
If a user is found and the password hash matches the one stored in the database, it stores the user's ID in the session and redirects to the index page.
If the credentials are incorrect, it returns an error message.
On a GET request, it simply renders the login.html template.

* register Function:
Handles user registration.
On a POST request (when the user submits the registration form):
Retrieves the username and password from the form.
Hashes the password for secure storage.
Inserts the new user into the database.
Redirects to the login page after successful registration.
On a GET request, it renders the register.html template.

* greet Function:
A simple function that retrieves a name from a form and renders greet.html with the provided name.

* logout Function:
Logs out the user by removing user_id from the session.
Redirects to the login page.


* ### database.py
```
import psycopg2

conn_params = {
    'dbname': 'Flask',
    'user': '<your-database-user-name>',
    'password': '',
    'host': 'localhost'
}

def get_db_connection():
    return psycopg2.connect(**conn_params)

```

> Code Explanation

* import psycopg2:

This line imports the psycopg2 module, which is a PostgreSQL adapter for the Python programming language. It allows Python programs to connect to and interact with PostgreSQL databases.

* conn_params = { ... }:
Here, a dictionary named conn_params is created. It contains the parameters needed to establish a connection to a PostgreSQL database. These parameters include:
'dbname': 'Flask' – The name of the database to connect to, in this case, 'Flask'.
'user': '<your-database-user-name>' – The username of the database user. You need to replace <your-database-user-name> with the actual username.
'password': '' – The password for the database user. It's currently an empty string, so you would need to provide the actual password if authentication is required.
'host': 'localhost' – The host address of the database server. In this case, it's localhost, indicating that the database is running on the same machine as the Python script.

* def get_db_connection()::
This line defines a function named get_db_connection. This function, when called, will create and return a new database connection using the parameters defined in conn_params.

* return psycopg2.connect(**conn_params):
Inside the get_db_connection function, this line is responsible for creating the actual connection to the PostgreSQL database. The psycopg2.connect() function is called with **conn_params, which unpacks the conn_params dictionary and passes the connection parameters to connect(). The function then returns this new connection object.

* ### app.py
```
from flask import Flask
from routes import index, login, register, greet, logout


app = Flask(__name__)
app.secret_key = 'atuba_kingsley_??_990909'

app.add_url_rule("/", "index", index)
app.add_url_rule("/login", "login", login, methods=["GET", "POST"])
app.add_url_rule("/register", "register", register, methods=["GET", "POST"])
app.add_url_rule("/greet", "greet", greet, methods=["POST"])
app.add_url_rule("/logout", "logout", logout)

if __name__ == "__main__":
    app.run(debug=True)
```

> Code Explanation

* from flask import Flask:
This line imports the Flask class from the flask module. Flask is the main class of the Flask web framework and is used to create an instance of a web application.

* from routes import index, login, register, greet, logout:
Imports specific functions index, login, register, greet, and logout from a module named routes. These functions are likely to be view functions, which handle the logic for different routes (URLs) in your application.

* app = Flask(__name__):
Creates an instance of the Flask class. The __name__ variable is passed to help Flask determine the root path of the application, which is used for relative path calculations.

* app.secret_key = 'atuba_kingsley_??_990909':
Sets the secret key for the application, which is used by Flask to encrypt session data. It's important to keep this key secret and unpredictable for security reasons.

* app.add_url_rule("/", "index", index):
Adds a URL rule for the root URL ("/") which is handled by the index function. The "index" string is the endpoint name.

* app.add_url_rule("/login", "login", login, methods=["GET", "POST"]):
Adds a URL rule for "/login". The login function handles this route, and it accepts both GET and POST HTTP methods.

* app.add_url_rule("/register", "register", register, methods=["GET", "POST"]):
Similar to the previous line, this adds a URL rule for "/register", handled by the register function, accepting GET and POST methods.

* app.add_url_rule("/greet", "greet", greet, methods=["POST"]):
Adds a URL rule for "/greet", handled by the greet function. This route only accepts POST methods, which is typical for routes that process data submitted by the user.

* app.add_url_rule("/logout", "logout", logout):
Adds a URL rule for "/logout", handled by the logout function. No specific HTTP methods are mentioned, so it defaults to GET.

* if __name__ == "__main__":
This is a common Python idiom that checks if the script is being run as the main program and not imported as a module in another script. It's a standard way to control the execution of code in a Python module.

* app.run(debug=True):
Starts the Flask application with the debug mode enabled. Debug mode provides a debugger and reloader for convenient development, but it should be turned off in a production environment.



## Step 24

add the code below to both index.html and greet.html

```
<p><a href="{{ url_for('logout') }}">Logout</a></p>
```

![login and Register](./img/12.png)


## Step 25

Run the code below on the terminal

```
flask run
```