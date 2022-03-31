from crypt import methods
from app import app
from flask import render_template, request, redirect
import users
import plans
import moves

@app.route("/")
def index():
    list_plans = plans.get_list()
    return render_template("index.html", plans=list_plans)

@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "GET":
        return render_template("index.html")
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
        return render_template("index.html", plans=list_plans)
    if request.method == "POST":
        name = request.form["name"]
        count_plans = users.get_count_plans()
        print(users.user_id())
        print(count_plans)
        if int(count_plans) >= 5:
            return render_template("error.html", message="Sinulla on jo viisi suunnitelmaa, et saa luoda enempää")
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
    if plans.get_count_moves(plan_id) >= 10:
        return render_template("error.html", message="Suunnitelmassa on jo kymmenen liikettä, et voi lisätä enempää")
    move_name = request.form["move_name"]
    move_id = moves.get_move_id(move_name)
    sets = request.form["sets"]
    reps = request.form["reps"]
    weights = 0
    if not plans.add_move(plan_id, move_id, sets, reps, weights):
        return render_template("error.html", message="Virhe lisättäessä liikettä suunnitelmaan")  
    print("liikkeitä on: " + str(plans.get_count_moves(plan_id)))
    return render_template("editplan.html", moves=moves.get_moves(), plan_name=plans.get_name(plan_id), plan_id=plan_id, planinfo=plans.get_moves_in_plan(plan_id))

@app.route("/deletemove", methods=["POST"])
def delete_move_from_plan():
    moveinformations_id = request.form["moveinformations_id"]
    plan_id = plans.get_plan_id_with_moveinfo_id(moveinformations_id)
    if not plans.delete_move(moveinformations_id):
        return render_template("error.html", message="Virhe poistettaessa liikettä suunnitelmasta")
    return render_template("editplan.html", moves=moves.get_moves(), plan_name=plans.get_name(plan_id), plan_id=plan_id, planinfo=plans.get_moves_in_plan(plan_id))
