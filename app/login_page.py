from app import app
from flask import render_template, session


@app.route("/login")
def login():
    session["username"] = "test_logged_username"
    return render_template("login_page.html")
