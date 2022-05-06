from flask import render_template, request, redirect
from app import app
import users
import plans
import moves
import stats

@app.route("/")
def index():
    return render_template("index.html", plans=plans.list_all(),
                           moves=moves.list_all(),
                           stats_found=bool(int(stats.gymvisits_all()) > 0),
                           today=stats.today_date())

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
        if not users.signin(username, password1):
            return render_template("error.html",
                                   message="Tunnus tai salasana on väärän mittainen " +
                                   "tai tunnus jo käytössä")
        users.login(username, password1)
        return redirect("/")

@app.route("/addplan", methods=["GET", "POST"])
def addplan():
    if request.method == "GET":
        return render_template("index.html", plans=plans.list_all(),
                               moves=moves.list_all(),
                               stats_found=bool(int(stats.gymvisits_all()) > 0),
                               today=stats.today_date())
    if request.method == "POST":
        users.check_csrf()
        name = request.form["name"]
        if int(users.get_count_plans()) >= 5:
            return render_template("error.html", message="Olet jo luonut viisi suunnitelmaa")
        if not plans.name_valid(name):
            return render_template("error.html", message="Saliohjelman nimessä on väärä määrä " +
                                   "merkkejä tai sinulla on jo samanniminen saliohjelma")
        if not plans.add_new(name):
            return render_template("error.html", message="Odottamaton virhe tallennuksessa, " +
                                   "yritä uudelleen")
        return redirect("/addplan")

@app.route("/editplan", methods=["GET", "POST"])
def edit_plan():
    if request.method == "GET":
        return render_template("editplan.html")
    if request.method == "POST":
        users.check_csrf()
        plan_name = request.form["plan_name"]
        return render_template("editplan.html", moves=moves.list_all(), plan_name=plan_name,
                               plan_id=plans.get_id_with_name(plan_name),
                               planinfo=plans.get_moves_in_plan(plans.get_id_with_name(plan_name)))

@app.route("/addmove", methods=["POST"])
def add_move_to_plan():
    users.check_csrf()
    plan_id = request.form["plan_id"]
    if plans.count_moves_in_plan(plan_id) >= 10:
        return render_template("error.html", message="Suunnitelmassa on jo kymmenen liikettä")
    move_name = request.form["move_name"]
    sets = request.form["sets"]
    reps = request.form["reps"]
    if not plans.move_already_in_plan(plan_id, moves.get_move_id_with_name(move_name)):
        return render_template("error.html", message="Tämä liike on jo tässä saliohjelmassa")
    if not moves.sets_and_reps_valid(sets, reps):
        return render_template("error.html", message="Syötit virheellisiä lukuja")
    weight = 0
    if not plans.add_move_to_plan(plan_id,
                                  moves.get_move_id_with_name(move_name), sets, reps, weight):
        return render_template("error.html", message="Hups! Sovellusvirhe, yritä uudelleen")
    return render_template("editplan.html", moves=moves.list_all(),
                           plan_name=plans.get_name_with_plan_id(plan_id),
                           plan_id=plan_id, planinfo=plans.get_moves_in_plan(plan_id))

@app.route("/deletemove", methods=["POST"])
def delete_move_from_plan():
    users.check_csrf()
    moveinfo_id = request.form["moveinformations_id"]
    if not plans.delete_move_from_plan(moveinfo_id):
        return render_template("error.html", message="Hups! Sovellusvirhe, yritä uudelleen")
    return render_template("editplan.html", moves=moves.list_all(),
                           plan_name=plans.get_name_with_plan_id(plans.get_id_with_moveinfo_id(moveinfo_id)),
                           plan_id=plans.get_id_with_moveinfo_id(moveinfo_id),
                           planinfo=plans.get_moves_in_plan(plans.get_id_with_moveinfo_id(moveinfo_id)))

@app.route("/opengymplan", methods=["POST", "GET"])
def document_gymvisit():
    if request.method == "GET":
        return render_template("document.html")
    if request.method == "POST":
        users.check_csrf()
        plan_name = request.form["plan_name"]
        date = request.form["date"]
        if date == "":
            return render_template("error.html", message="Et valinnut päivämäärää")
        return render_template("/document.html", date=date, plan_name=plan_name,
                               planinfo=plans.get_moves_in_plan(plans.get_id_with_name(plan_name)),
                               moves=plans.moves_and_last_weight(plans.get_id_with_name(plan_name)))

@app.route("/documentmove", methods=["GET", "POST"])
def document_move():
    users.check_csrf()
    weight = request.form["weight"]
    moveinfo_id = request.form["moveinformations_id"]
    plan_name = request.form["plan_name"]
    date = request.form["date"]
    if stats.move_documented_today(moveinfo_id, date, plans.get_id_with_name(plan_name)):
        return render_template("error.html", message="Kirjasit jo suorittaneesi tämän liikkeen")
    if not moves.weight_valid(weight):
        return render_template("error.html",
                               message="Paino ei voi olla negatiivinen, tyhjä tai yli 300kg")
    if not moves.document_moveinfo(weight, moveinfo_id, plans.get_id_with_name(plan_name), date):
        return render_template("error.html", message="Virhe kirjattaessa treeniä")
    return render_template("/document.html", date=date, plan_name=plan_name,
                           planinfo=plans.get_moves_in_plan(plans.get_id_with_name(plan_name)),
                           moves=plans.moves_and_last_weight(plans.get_id_with_name(plan_name)))

@app.route("/statistics_one", methods=["POST"])
def statistics_per_plan():
    users.check_csrf()
    plan_name = request.form["plan_name"]
    if int(stats.gymvisits_one_plan(plans.get_id_with_name(plan_name))) < 1:
        return render_template("error.html", message="Valitulle saliohjelmalle ei ole kirjauksia")
    return render_template("statistics_one.html", plan_name=plan_name,
                           planinfo=plans.get_moves_in_plan(plans.get_id_with_name(plan_name)),
                           stats_all=stats.moves_per_plan(plans.get_id_with_name(plan_name)),
                           count=stats.gymvisits_one_plan(plans.get_id_with_name(plan_name)),
                           first=stats.first_time_one_plan(plans.get_id_with_name(plan_name)),
                           last=stats.last_time_one_plan(plans.get_id_with_name(plan_name)))

@app.route("/statistics_all", methods=["POST"])
def statistics_all():
    users.check_csrf()
    return render_template("statistics_all.html", max_weights=stats.max_weight_per_move(),
                           monthly_workouts=stats.print_monthly_workout_stats(),
                           yearly_workouts=stats.print_yearly_workout_stats(),
                           count=stats.gymvisits_all(), first=stats.first_time_all_plans(),
                           last=stats.last_time_all_plans())

@app.route("/statistics_move", methods=["POST"])
def statistics_move():
    users.check_csrf()
    move_name = request.form["move_name"]
    return render_template("statistics_move.html",
                           weights=stats.all_weigths_per_move(moves.get_move_id_with_name(move_name)),
                           move_name=move_name)
