from datetime import date
import moves
import users
from db import db

def moves_per_plan(plan_id):
    sql = """SELECT m.name, mi.sets, mi.reps, mi.weight, d.day, m.id
    FROM moves m, moveinformations mi, movesdone d WHERE mi.id IN
    (SELECT moveinfo_id FROM movesdone WHERE plan_id=:plan_id)
    AND m.id=mi.move_id AND d.moveinfo_id=mi.id ORDER BY m.name, d.day DESC"""
    result = db.session.execute(sql, {"plan_id": plan_id})
    list_moves_done = result.fetchall()
    moves_to_print = []
    previous = 0
    for move in list_moves_done:
        move_id = move[5]
        name = f"{move[0]} :"
        sets = f"{move[1]} sarjaa "
        reps = f"{move[2]} toistoa"
        weight = f": {move[3]} kg"
        day = str(move[4])
        if move_id == previous:
            row = ["", "", "", day, weight]
            moves_to_print.append(row)
        else:
            row = [name, sets, reps, day, weight]
            empty = ["", "", "", "", ""]
            if previous > 0:
                moves_to_print.append(empty)
                moves_to_print.append(empty)
            moves_to_print.append(row)
        previous = move_id
    return moves_to_print


def gymvisits_one_plan(plan_id):
    sql = "SELECT COUNT(DISTINCT day) FROM movesdone WHERE plan_id=:plan_id"
    result = db.session.execute(sql, {"plan_id": plan_id})
    count = result.fetchone()
    count_trimmed = str(count).strip(",(')")
    return count_trimmed


def first_time_one_plan(plan_id):
    sql = "SELECT MIN(day) FROM movesdone WHERE plan_id=:plan_id"
    result = db.session.execute(sql, {"plan_id": plan_id})
    day = result.fetchone()
    day_toprint = trim_date(day)
    return day_toprint


def first_time_all_plans():
    owner_id = users.user_id()
    sql = """SELECT MIN(day) FROM movesdone WHERE plan_id IN(SELECT id FROM gymplans
             WHERE owner_id=:owner_id)"""
    result = db.session.execute(sql, {"owner_id": owner_id})
    day = result.fetchone()
    day_toprint = trim_date(day)
    return day_toprint


def last_time_one_plan(plan_id):
    sql = "SELECT MAX(day) FROM movesdone WHERE plan_id=:plan_id"
    result = db.session.execute(sql, {"plan_id": plan_id})
    day = result.fetchone()
    day_toprint = trim_date(day)
    first = first_time_one_plan(plan_id)
    if first == day_toprint:
        return ""
    return f"ja viimeksi {day_toprint}"


def last_time_all_plans():
    owner_id = users.user_id()
    sql = """SELECT MAX(day) FROM movesdone WHERE plan_id IN
             (SELECT id FROM gymplans WHERE owner_id=:owner_id)"""
    result = db.session.execute(sql, {"owner_id": owner_id})
    day = result.fetchone()
    day_toprint = trim_date(day)
    first = first_time_all_plans()
    if first == day_toprint:
        return ""
    return f"ja viimeksi {day_toprint}"


def trim_date(day):
    day_trimmed = str(day).strip("datetime.date()")
    daylist = day_trimmed.split(",")
    year = daylist[0]
    month = daylist[1]
    day = daylist[2].strip(")")
    month_long = get_month_with_number(int(month))
    return f"{day} {month_long}ta {year}"


def move_last_documented(moveinformations_id, plan_id):
    move_id = moves.get_move_id_with_moveinfo_id(moveinformations_id)
    sql = """SELECT MAX(md.day) FROM movesdone md, movesinplans mp, moveinformations mi
             WHERE mi.id=mp.move_id AND md.plan_id=mp.plan_id
             AND mp.plan_id=:plan_id AND mi.move_id=:move_id"""
    result = db.session.execute(sql, {"move_id": move_id, "plan_id": plan_id})
    return result.fetchone()


def move_documented_today(moveinformations_id, day, plan_id):
    move_id = moves.get_move_id_with_moveinfo_id(moveinformations_id)
    sql = """SELECT COUNT(*) FROM movesdone md, moveinformations mi WHERE mi.id=md.moveinfo_id
             AND md.plan_id=:plan_id AND mi.move_id=:move_id AND md.day=:day"""
    result = db.session.execute(
        sql, {"plan_id": plan_id, "move_id": move_id, "day": day})
    count = int(result.fetchone()[0])
    return count > 0


def move_last_weight_and_day_with_moveinformations_id(moveinformations_id, plan_id):
    move_id = moves.get_move_id_with_moveinfo_id(moveinformations_id)
    return move_last_weight_and_day_with_move_id(move_id, plan_id)


def move_last_weight_and_day_with_move_id(move_id, plan_id):
    sql = """SELECT md.day, mi.weight, mi.move_id FROM movesdone md, moveinformations mi
             WHERE md.moveinfo_id=mi.id AND md.plan_id=:plan_id AND mi.move_id=:move_id 
             ORDER BY md.id DESC LIMIT 1"""
    result = db.session.execute(sql, {"plan_id": plan_id, "move_id": move_id})
    return result.fetchone()


def max_weight_per_move():
    owner_id = users.user_id()
    sql = """SELECT MAX(mi.weight), m.name FROM moves m, moveinformations mi, movesdone md
            WHERE mi.id=md.moveinfo_id AND m.id=mi.move_id AND md.plan_id IN
            (SELECT id FROM gymplans WHERE owner_id=:owner_id) GROUP BY m.id ORDER BY m.id"""
    result = db.session.execute(sql, {"owner_id": owner_id})
    return result.fetchall()


def all_weigths_per_move(move_id):
    owner_id = users.user_id()
    sql = """SELECT mi.weight, md.day, g.name, mi.sets, mi.reps
             FROM moveinformations mi, movesdone md, gymplans g WHERE g.id=md.plan_id AND mi.id=md.moveinfo_id
             AND mi.move_id=:move_id AND md.plan_id IN
             (SELECT id FROM gymplans WHERE owner_id=:owner_id) ORDER BY md.day"""
    result = db.session.execute(
        sql, {"move_id": move_id, "owner_id": owner_id})
    return result.fetchall()


def print_monthly_workout_stats():
    owner_id = users.user_id()
    sql = """SELECT DATE_TRUNC('month', day) AS month, COUNT(DISTINCT day) FROM movesdone
             WHERE plan_id IN (SELECT id FROM gymplans
             WHERE owner_id=:owner_id) GROUP BY DATE_TRUNC('month', day)"""
    result = db.session.execute(sql, {"owner_id": owner_id})
    data_list = result.fetchall()
    list_to_print = []
    for data in data_list:
        month_split = str(data[0]).split("-")
        year = month_split[0]
        month_int = int(month_split[1])
        month = f"{get_month_with_number(month_int)}ssa"
        count = data[1]
        row = year, month, count
        list_to_print.append(row)
    return list_to_print


def print_yearly_workout_stats():
    owner_id = users.user_id()
    sql = """SELECT DATE_TRUNC('year', day) AS year, COUNT(DISTINCT day) FROM movesdone
             WHERE plan_id IN (SELECT id FROM gymplans WHERE owner_id=:owner_id)
             GROUP BY DATE_TRUNC('year', day)"""
    result = db.session.execute(sql, {"owner_id": owner_id})
    data_list = result.fetchall()
    list_to_print = []
    for data in data_list:
        month_split = str(data[0]).split("-")
        year = month_split[0]
        count = data[1]
        row = year, count
        list_to_print.append(row)
    return list_to_print


def gymvisits_all():
    owner_id = users.user_id()
    sql = """SELECT COUNT(DISTINCT day) FROM movesdone WHERE plan_id IN (SELECT id
             FROM gymplans WHERE owner_id=:owner_id)"""
    result = db.session.execute(sql, {"owner_id": owner_id})
    count = str(result.fetchone())
    count_trimmed = count.strip("(,)")
    return count_trimmed

def today_date():
    return date.today()

def get_month_with_number(number):
    if number == 1:
        return "tammikuu"
    if number == 2:
        return "helmikuu"
    if number == 3:
        return "maaliskuu"
    if number == 4:
        return "huhtikuu"
    if number == 5:
        return "toukokuu"
    if number == 6:
        return "kesäkuu"
    if number == 7:
        return "heinäkuu"
    if number == 8:
        return "elokuu"
    if number == 9:
        return "syyskuu"
    if number == 10:
        return "lokakuu"
    if number == 11:
        return "marraskuu"
    if number == 12:
        return "joulukuu"
