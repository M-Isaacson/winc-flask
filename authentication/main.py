import os

from flask import Flask, redirect, render_template, request, session, url_for
from helpers import get_users, hash_password

__winc_id__ = "8fd255f5fe5e40dcb1995184eaa26116"
__human_name__ = "authentication"

app = Flask(__name__)

app.secret_key = os.urandom(16)


@app.route("/home")
def redirect_index():
    return redirect(url_for("index"))


@app.route("/")
def index():
    return render_template("index.html", title="Index")


@app.route("/about")
def about():
    if "username" in session:
        return render_template("about.html", title="About")
    return redirect(url_for("login"))


@app.route("/lon")
def lon():
    if "username" in session:
        return render_template("lon.html", title="League of Nations")
    return redirect(url_for("login"))


@app.route("/login", methods=["GET", "POST"])
def login():
    error = None
    if request.method == "POST":
        the_hash = hash_password(request.form["password"])
        for key, value in get_users().items():
            if key == request.form["username"] and value == the_hash:
                session["username"] = request.form["username"]
                return redirect(url_for("dashboard"))
        error = "Invalid username/password! Please try again."
    return render_template("login.html", error=error)


@app.route("/dashboard")
def dashboard():
    if "username" in session:
        return render_template("dashboard.html")
    return redirect(url_for("login"))


@app.route("/logout", methods=["GET", "POST"])
def logout():
    session.pop("username", None)
    return redirect(url_for("index"))
