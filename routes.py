from crypt import methods
from app import app
from flask import render_template, request, redirect
import users
import plans
import moves

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
    list_plans = plans.get_list()
    if request.method == "GET":
        return render_template("gymplan.html", plans=list_plans)
    if request.method == "POST":
        name = request.form["name"]
        if plans.create_new_gymplan(name):
            return redirect("/gymplan")
        else:
            return render_template("error.html",  message="Virhe uuden suunnitelman teossa")


@app.route("/editplan", methods=["GET","POST"])
def edit_plan():
    if request.method == "GET":
        return render_template("editplan.html")
    if request.method == "POST":
        plan_name=request.form["plan_name"]
        return render_template("editplan.html", moves=moves.get_moves(), plan_name=plan_name, plan_id=plans.get_id(plan_name), planinfo=plans.get_moves_in_plan(plans.get_id(plan_name)))

@app.route("/addmove", methods=["POST", "GET"])
def add_move_to_plan():
    plan_id = request.form["plan_id"]
    move_name = request.form["move_name"]
    move_id = moves.get_move_id(move_name)
    sets = request.form["sets"]
    reps = request.form["reps"]
    weights = 0
    if not plans.add_move(plan_id, move_id, sets, reps, weights):
        return render_template("error.html", message="Virhe lisättäessä liikettä suunnitelmaan")
    return render_template("editplan.html", moves=moves.get_moves(), plan_name=plans.get_name(plan_id), plan_id=plan_id, planinfo=plans.get_moves_in_plan(plan_id))
