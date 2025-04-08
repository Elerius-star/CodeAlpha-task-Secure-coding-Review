from flask import Flask, request, render_template, redirect, session
import sqlite3

app = Flask(__name__)
app.secret_key = "hardcoded_secret"  # ❌ Hardcoded Secret Key

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
        password = request.form["password"]  # ❌ Plaintext password storage

        conn = get_db()
        cursor = conn.cursor()
        cursor.execute(f"INSERT INTO users (username, password) VALUES ('{username}', '{password}')")  # ❌ SQL Injection Risk
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
        cursor.execute(f"SELECT * FROM users WHERE username='{username}' AND password='{password}'")  # ❌ SQL Injection Risk
        user = cursor.fetchone()
        conn.close()

        if user:
            session["user"] = username  # ❌ Session Fixation Risk
            return "Login successful!"
        else:
            return "Invalid credentials!"

    return render_template("login.html")

if __name__ == "__main__":
    app.run(debug=True)
