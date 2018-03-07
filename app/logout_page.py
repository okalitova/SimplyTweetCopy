from app import app
from flask import session, redirect, url_for

@app.route("/logout")
def logout():
    session.pop("username", None)
    return redirect(url_for("main_page"))
