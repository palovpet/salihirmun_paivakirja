from crypt import methods
from app import app
from flask import render_template, request, redirect
import users
import plans
import moves
import stats

@app.route("/")
def index():
    list_plans = plans.list_all()
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

@app.route("/addplan", methods=["GET", "POST"])
def addplan():
    list_plans = plans.list_all()
    if request.method == "GET":
        return render_template("index.html", plans=list_plans)
    if request.method == "POST":
        name = request.form["name"]
        count_plans = users.get_count_plans()
        if int(count_plans) >= 5:
            return render_template("error.html", message="Sinulla on jo viisi suunnitelmaa, et saa luoda enempää")
        if name == "":
            return render_template("error.html", message="Saliohjelman nimi ei voi olla tyhjä")
        if not plans.validate_name(name):
            return render_template("error.html", message="Sinulla on jo tämän niminen saliohjelma")
        if not plans.add_new(name):
            return render_template("error.html",  message="Virhe uuden suunnitelman teossa")
        return redirect("/addplan")          

@app.route("/editplan", methods=["GET","POST"])
def edit_plan():
    if request.method == "GET":
        return render_template("editplan.html")
    if request.method == "POST":
        plan_name=request.form["plan_name"]
        return render_template("editplan.html", moves=moves.list_all(), plan_name=plan_name, plan_id=plans.get_id(plan_name), planinfo=plans.get_moves(plans.get_id(plan_name)))

@app.route("/addmove", methods=["POST"])
def add_move_to_plan():
    plan_id = request.form["plan_id"]
    if plans.count_moves(plan_id) >= 10:
        return render_template("error.html", message="Suunnitelmassa on jo kymmenen liikettä, et voi lisätä enempää")
    move_name = request.form["move_name"]
    move_id = moves.get_id(move_name)
    sets = request.form["sets"]
    reps = request.form["reps"]
    if not moves.validate_sets_reps(sets, reps):
        return render_template("error.html", message="Syötit virheellisiä lukuja sarjoihin tai toistoihin, molempien on olatava vähintään 1")
    weight = 0
    if not moves.accepted_values(sets, reps, weight):
        return render_template("error.html", message="Syötit virheellisiä tietoja")
    if not plans.add_move(plan_id, move_id, sets, reps, weight):
        return render_template("error.html", message="Virhe lisättäessä liikettä suunnitelmaan")  
    return render_template("editplan.html", moves=moves.list_all(), plan_name=plans.get_name(plan_id), plan_id=plan_id, planinfo=plans.get_moves(plan_id))

@app.route("/deletemove", methods=["POST"])
def delete_move_from_plan():
    moveinformations_id = request.form["moveinformations_id"]
    plan_id = plans.get_id_with_moveinfo_id(moveinformations_id)
    if not plans.delete_move(moveinformations_id):
        return render_template("error.html", message="Virhe poistettaessa liikettä suunnitelmasta")
    return render_template("editplan.html", moves=moves.list_all(), plan_name=plans.get_name(plan_id), plan_id=plan_id, planinfo=plans.get_moves(plan_id))

@app.route("/opengymplan", methods=["POST", "GET"])
def document_gymvisit():
    if request.method == "GET":
        return render_template("document.html")
    if request.method == "POST":
        plan_name=request.form["plan_name"]
        date=request.form["date"]
        plan_id=plans.get_id(plan_name)
        if date == "":
            return render_template("error.html", message="Et valinnut päivämäärää, jolle kirjaat salikäyntiä")
        return render_template("/document.html", date=date, plan_name=plan_name, planinfo=plans.get_moves(plan_id))

@app.route("/documentmove", methods=["GET","POST"])
def document_move():
    weight=request.form["weight"] 
    moveinformations_id=request.form["moveinformations_id"]
    plan_name=request.form["plan_name"]
    date=request.form["date"]
    plan_id=plans.get_id(plan_name)
    if not moves.validate_weight(weight):
        return render_template("error.html", message="Paino ei voi olla negatiivinen")
    if not moves.document_moveinformation(weight, moveinformations_id, plan_id, date):
        return render_template("error.html", "Virhe kirjattaessa treeniä")
    return render_template("/document.html", date=date, plan_name=plan_name, planinfo=plans.get_moves(plan_id))

@app.route("/statistics", methods=["POST"])
def statistics_per_plan():
    plan_name = request.form["plan_name"]
    plan_id = plans.get_id(plan_name)
    stats_all = stats.move_stats(plan_id)
    count_workouts = stats.gymvisits_one(plan_id)
    first_time = stats.first_time_one(plan_id)
    last_time = stats.last_time_one(plan_id)
    return render_template("statistics.html", plan_name=plan_name, planinfo=plans.get_moves(plan_id), stats_all=stats_all, count_workouts=count_workouts, first_time=first_time, last_time=last_time)
