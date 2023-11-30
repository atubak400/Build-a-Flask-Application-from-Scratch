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


  git init
  git add README.md
  git commit -m "modularised app.py"
  git branch -M main
  git remote add origin https://github.com/atubak400/Build-a-Flask-Application-from-Scratch.git
  git push -u origin main