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



"""
from flask import Flask:
This line imports the Flask class from the flask module. Flask is the main class of the Flask web framework and is used to create an instance of a web application.

from routes import index, login, register, greet, logout:
Imports specific functions index, login, register, greet, and logout from a module named routes. These functions are likely to be view functions, which handle the logic for different routes (URLs) in your application.

app = Flask(__name__):
Creates an instance of the Flask class. The __name__ variable is passed to help Flask determine the root path of the application, which is used for relative path calculations.

app.secret_key = 'atuba_kingsley_??_990909':
Sets the secret key for the application, which is used by Flask to encrypt session data. It's important to keep this key secret and unpredictable for security reasons.

app.add_url_rule("/", "index", index):
Adds a URL rule for the root URL ("/") which is handled by the index function. The "index" string is the endpoint name.

app.add_url_rule("/login", "login", login, methods=["GET", "POST"]):
Adds a URL rule for "/login". The login function handles this route, and it accepts both GET and POST HTTP methods.

app.add_url_rule("/register", "register", register, methods=["GET", "POST"]):
Similar to the previous line, this adds a URL rule for "/register", handled by the register function, accepting GET and POST methods.

app.add_url_rule("/greet", "greet", greet, methods=["POST"]):
Adds a URL rule for "/greet", handled by the greet function. This route only accepts POST methods, which is typical for routes that process data submitted by the user.

app.add_url_rule("/logout", "logout", logout):
Adds a URL rule for "/logout", handled by the logout function. No specific HTTP methods are mentioned, so it defaults to GET.

if __name__ == "__main__":
This is a common Python idiom that checks if the script is being run as the main program and not imported as a module in another script. It's a standard way to control the execution of code in a Python module.

app.run(debug=True):
Starts the Flask application with the debug mode enabled. Debug mode provides a debugger and reloader for convenient development, but it should be turned off in a production environment.





"""