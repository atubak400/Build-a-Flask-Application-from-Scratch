from flask import Flask
from routes import index, login, register, greet, logout  # Import the route functions


app = Flask(__name__)
app.secret_key = 'atuba_kingsley_??_990909'

app.add_url_rule("/", "index", index)
app.add_url_rule("/login", "login", login, methods=["GET", "POST"])
app.add_url_rule("/register", "register", register, methods=["GET", "POST"])
app.add_url_rule("/greet", "greet", greet, methods=["POST"])
app.add_url_rule("/logout", "logout", logout)

if __name__ == "__main__":
    app.run(debug=True)
