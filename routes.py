from flask import render_template, request, redirect
from app import app
import users
import plans
import moves
import stats

@app.route("/")
def index():
    list_plans = plans.list_all()
    stats_found = bool(int(stats.gymvisits_all()) > 0)
    today = stats.today_date()
    return render_template("index.html", plans=list_plans,
                           moves=moves.list_all(), stats_found=stats_found, today=today)

@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "GET":
        return render_template("index.html")
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]
        if users.login(username, password):
            return redirect("/")
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
            return render_template("error.html", message="Olet jo luonut viisi suunnitelmaa")
        if not plans.name_valid(name):
            return render_template("error.html", message="Virhe saliohjelman nimessä")
        if not plans.add_new(name):
            return render_template("error.html", message="Virhe uuden suunnitelman teossa")
        return redirect("/addplan")

@app.route("/editplan", methods=["GET", "POST"])
def edit_plan():
    if request.method == "GET":
        return render_template("editplan.html")
    if request.method == "POST":
        plan_name = request.form["plan_name"]
        return render_template("editplan.html", moves=moves.list_all(), plan_name=plan_name,
                               plan_id=plans.get_id_with_name(plan_name),
                               planinfo=plans.get_moves_in_plan(plans.get_id_with_name(plan_name)))

@app.route("/addmove", methods=["POST"])
def add_move_to_plan():
    plan_id = request.form["plan_id"]
    if plans.count_moves_in_plan(plan_id) >= 10:
        return render_template("error.html", message="Suunnitelmassa on jo kymmenen liikettä")
    move_name = request.form["move_name"]
    move_id = moves.get_move_id_with_name(move_name)
    sets = request.form["sets"]
    reps = request.form["reps"]
    if not plans.move_already_in_plan(plan_id, move_id):
        return render_template("error.html", message="Tämä liike on jo tässä saliohjelmassa")
    if not moves.sets_and_reps_valid(sets, reps):
        return render_template("error.html", message="Syötit virheellisiä lukuja")
    weight = 0
    if not plans.add_move_to_plan(plan_id, move_id, sets, reps, weight):
        return render_template("error.html", message="Virhe lisättäessä liikettä suunnitelmaan")
    return render_template("editplan.html", moves=moves.list_all(),
                           plan_name=plans.get_name_with_plan_id(plan_id),
                           plan_id=plan_id, planinfo=plans.get_moves_in_plan(plan_id))

@app.route("/deletemove", methods=["POST"])
def delete_move_from_plan():
    moveinformations_id = request.form["moveinformations_id"]
    plan_id = plans.get_id_with_moveinfo_id(moveinformations_id)
    if not plans.delete_move_from_plan(moveinformations_id):
        return render_template("error.html", message="Virhe poistettaessa liikettä suunnitelmasta")
    return render_template("editplan.html", moves=moves.list_all(),
                           plan_name=plans.get_name_with_plan_id(plan_id),
                           plan_id=plan_id, planinfo=plans.get_moves_in_plan(plan_id))

@app.route("/opengymplan", methods=["POST", "GET"])
def document_gymvisit():
    if request.method == "GET":
        return render_template("document.html")
    if request.method == "POST":
        plan_name = request.form["plan_name"]
        date = request.form["date"]
        plan_id = plans.get_id_with_name(plan_name)
        if date == "":
            return render_template("error.html", message="Et valinnut päivämäärää")
        return render_template("/document.html", date=date, plan_name=plan_name,
                               planinfo=plans.get_moves_in_plan(plan_id),
                               moves_and_weights=plans.moves_and_last_weight(plan_id))

@app.route("/documentmove", methods=["GET", "POST"])
def document_move():
    weight = request.form["weight"]
    moveinformations_id = request.form["moveinformations_id"]
    plan_name = request.form["plan_name"]
    date = request.form["date"]
    plan_id = plans.get_id_with_name(plan_name)
    if stats.move_documented_today(moveinformations_id, date, plan_id):
        return render_template("error.html", message="Kirjasit jo suorittaneesi tämän liikkeen")
    if not moves.weight_valid(weight):
        return render_template("error.html", message="Paino ei voi olla negatiivinen eikä tyhjä")
    if not moves.document_moveinfo(weight, moveinformations_id, plan_id, date):
        return render_template("error.html", message="Virhe kirjattaessa treeniä")
    return render_template("/document.html", date=date, plan_name=plan_name,
                           planinfo=plans.get_moves_in_plan(plan_id),
                           moves_and_weights=plans.moves_and_last_weight(plan_id))

@app.route("/statistics_one", methods=["POST"])
def statistics_per_plan():
    plan_name = request.form["plan_name"]
    plan_id = plans.get_id_with_name(plan_name)
    stats_all = stats.moves_per_plan(plan_id)
    count_workouts = stats.gymvisits_one_plan(plan_id)
    first = stats.first_time_one_plan(plan_id)
    last = stats.last_time_one_plan(plan_id)
    if first == last:
        last = ""
    else:
        last = f", ja viimeksi  {last}"
    return render_template("statistics_one.html", plan_name=plan_name,
                           planinfo=plans.get_moves_in_plan(plan_id), stats_all=stats_all,
                           count_workouts=count_workouts, first=first, last=last)

@app.route("/statistics_all", methods=["POST"])
def statistics_all():
    max_weights = stats.max_weight_per_move()
    monthly_workouts = stats.print_monthly_workout_stats()
    yearly_workouts = stats.print_yearly_workout_stats()
    count_workouts = stats.gymvisits_all()
    first = stats.first_time_all_plans()
    last = stats.last_time_all_plans()
    if first == last:
        last = ""
    else:
        last = f", ja viimeksi  {last}"
    return render_template("statistics_all.html", max_weights=max_weights,
                           monthly_workouts=monthly_workouts, yearly_workouts=yearly_workouts,
                           count_workouts=count_workouts, first=first, last=last)

@app.route("/statistics_move", methods=["POST"])
def statistics_move():
    move_name = request.form["move_name"]
    move_id = moves.get_move_id_with_name(move_name)
    all_weights = stats.all_weigths_per_move(move_id)
    return render_template("statistics_move.html", all_weights=all_weights, move_name=move_name)
