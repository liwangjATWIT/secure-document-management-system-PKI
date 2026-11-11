from flask import Flask, render_template, request, redirect, url_for, session, flash
from werkzeug.security import generate_password_hash, check_password_hash

from database import get_db_connection, initialize_database

import os


# Initialize the Flask application
app = Flask(__name__)

# Set a secret key for session management
app.config["SECRET_KEY"] = os.environ.get(
    "SECRET_KEY",
    "dev-only-change-this-secret"
)

#Initialize the database
initialize_database()

# Home page
@app.route("/")
def home():
    return render_template("index.html")

# User registration
@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        username = request.form["username"].strip()
        email = request.form["email"].strip().lower()
        password = request.form["password"]
        
        if not username or not email or not password:
            flash("All fields are required.")
            return redirect(url_for("register"))
        
        if len(password) < 8:
            flash("Password must be at least 8 characters.")
            return redirect(url_for("register"))
        
        password_hash = generate_password_hash(password)
        
        connection = get_db_connection()
        
        try:
            connection.execute(
                """
                INSERT INTO users (username, email, password_hash)
                VALUES (?, ?, ?)
                """,
                (username, email, password_hash)
            )
            
            connection.commit()
            
        except Exception as e:
            flash("An error occurred: This email may already be registered under an account.")
            return redirect(url_for("register"))
        
        finally:
            connection.close()
            
        flash("Account registration successful! Please log in.")
        return redirect(url_for("login"))
    
    return render_template("register.html")

@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        email = request.form["email"].strip().lower()
        password = request.form["password"]
        
        connection = get_db_connection()
        
        user = connection.execute(
            "SELECT * FROM users WHERE email = ?",
            (email,)
        ).fetchone()
        
        connection.close()
        
        if user and check_password_hash(user["password_hash"], password):
            session.clear()
            session["user_id"] = user["id"]
            session["username"] = user["username"]
            
            return redirect(url_for("dashboard"))
        
        flash("Invalid email or password.")
        
    return render_template("login.html")

@app.route("/dashboard")
def dashboard():
    if "user_id" not in session:
        return redirect(url_for("login"))
    
    return render_template("dashboard.html", username=session["username"])

@app.route("/logout")
def logout():
    session.clear()
    return redirect(url_for("home"))
        
# Run application
if __name__ == "__main__":
    app.run(debug=True)
