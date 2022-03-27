from app import app
from flask import render_template, request, redirect
import users
import gymplan

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "GET":
        return render_template("login.html")
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]
        if users.login(username, password):
            return redirect("/")
        else:
            return render_template("error.html", message="Väärä tunnus tai salasana")

@app.route("/logout")
def logout():
    users.logout()
    return redirect("/")

@app.route("/signin", methods=["GET", "POST"])
def signin():
    if request.method == "GET":
        return render_template("signin.html")
    if request.method == "POST":
        username = request.form["username"]
        password1 = request.form["password1"]
        password2 = request.form["password2"]
        if password1 != password2:
            return render_template("error.html", message="Salasanojen on oltava samat")
        if users.signin(username, password1):
            return redirect("/")
        else:
            return render_template("error.html", message="Virhe rekisteröitymisessä")

@app.route("/gymplan", methods=["GET", "POST"])
def gymplan():
    if request.method == "GET":
        return render_template("gymplan.html")
    if request.method == "POST":
        name = request.form["name"]
        if gymplan.create_new_gymplan(name):
            return redirect("/")


