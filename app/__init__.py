import os
from .db import create_tables, create_user, get_users, check_password
from flask import Flask, render_template, request, flash, redirect, url_for

create_tables()

app = Flask(__name__)

app.config["SECRET_KEY"] = "super secret!"

@app.route("/")
def index():
    env = os.getenv("ENV", "dev")
    users = get_users()

    return render_template("index.html", env=env, users=users)

@app.route("/sign-up", methods=["GET", "POST"])
def sign_up():
    if request.method == "POST":
        username, password = request.form["username"], request.form["password"]

        create_user(username, password)
        flash("Created user")
        return redirect(url_for("index"))
        
    return render_template("sign_up.html")

@app.route("/sign-in", methods=["GET", "POST"])
def sign_in():
    if request.method == "POST":
        username, password = request.form["username"], request.form["password"]

        is_correct_password = check_password(username, password)

        if is_correct_password:
            flash(f"Signed in as {username}")
            return redirect(url_for("index"))
        else:
            flash(f"Incorrect username or password")

    return render_template("sign_in.html")
