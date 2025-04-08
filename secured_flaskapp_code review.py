from flask import Flask, request, render_template, redirect, session
import sqlite3
import os
from werkzeug.security import generate_password_hash, check_password_hash
from dotenv import load_dotenv

# Load or Set Environment Variables
load_dotenv()  # ✅ Loads variables from a .env file (if it exists)
os.environ.setdefault("SECRET_KEY", "your_super_secure_random_key")  # ✅ Sets a default key if not already set

app = Flask(__name__)
app.secret_key = os.getenv("SECRET_KEY")  # ✅ Secure storage of secret key

# Database connection
def get_db():
    conn = sqlite3.connect("users.db")
    conn.row_factory = sqlite3.Row
    return conn

# Home Route
@app.route("/")
def home():
    return "Welcome to the Secure Flask App!"

# User Registration Route
@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]

        hashed_password = generate_password_hash(password)  # ✅ Secure password hashing

        conn = get_db()
        cursor = conn.cursor()
        cursor.execute("INSERT INTO users (username, password) VALUES (?, ?)", (username, hashed_password))  # ✅ Prevents SQL Injection
        conn.commit()
        conn.close()

        return redirect("/login")

    return render_template("register.html")

# User Login Route
@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]

        conn = get_db()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM users WHERE username=?", (username,))
        user = cursor.fetchone()
        conn.close()

        if user and check_password_hash(user["password"], password):  # ✅ Secure password verification
            session["user"] = username  # ✅ Secure session management
            return "Login successful!"
        else:
            return "Invalid credentials!"

    return render_template("login.html")

if __name__ == "__main__":
    app.run(debug=True)
