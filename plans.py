from db import db
import users
import stats
import moves


def name_valid(name):
    if name == "":
        return False
    plans = list_all()
    for plan in plans:
        plan_trimmed = str(plan).strip(",(')")
        if plan_trimmed == name:
            return False
    if len(name) < 3 or len(name) > 30:
        return False
    return True


def add_new(name):
    owner_id = users.user_id()
    try:
        sql = "INSERT INTO gymplans (name, owner_id) VALUES (:name, :owner_id)"
        db.session.execute(sql, {"name": name, "owner_id": owner_id})
        db.session.commit()
        return True
    except:
        return False


def list_all():
    owner_id = users.user_id()
    sql = "SELECT name FROM gymplans WHERE owner_id=:owner_id ORDER BY name"
    result = db.session.execute(sql, {"owner_id": owner_id})
    return result.fetchall()


def get_id_with_name(name):
    owner_id = users.user_id()
    sql = "SELECT id FROM gymplans WHERE name=:name AND owner_id=:owner_id"
    result = db.session.execute(sql, {"name": name, "owner_id": owner_id})
    plan_id = result.fetchone()[0]
    return plan_id


def get_id_with_moveinfo_id(moveinfo_id):
    sql = "SELECT plan_id FROM movesinplans WHERE moveinfo_id=:moveinfo_id"
    result = db.session.execute(sql, {"moveinfo_id": moveinfo_id})
    plan_id = result.fetchone()[0]
    return plan_id


def get_name_with_plan_id(plan_id):
    sql = "SELECT name FROM gymplans WHERE id=:id"
    result = db.session.execute(sql, {"id": plan_id})
    name = result.fetchone()[0]
    return name


def get_moves_in_plan(plan_id):
    sql = """SELECT m.name, mi.sets, mi.reps, mi.weights, mi.id 
             FROM moves m, moveinformations mi WHERE mi.id IN (SELECT moveinfo_id FROM movesinplans
             WHERE plan_id=:plan_id AND visible=TRUE) AND m.id=mi.move_id"""
    result = db.session.execute(sql, {"plan_id": plan_id})
    return result.fetchall()


def add_move_to_plan(plan_id, move_id, sets, reps, weights):
    try:
        sql = """INSERT INTO moveinformations (move_id, sets, reps, weights)
                 VALUES (:move_id, :sets, :reps, :weights) RETURNING id"""
        result = db.session.execute(
            sql, {"move_id": move_id, "sets": sets, "reps": reps, "weights": weights})
        moveinfo_id = result.fetchone()[0]
    except:
        return False
    try:
        sql2 = "INSERT INTO movesinplans (moveinfo_id, plan_id) VALUES (:moveinfo_id, :plan_id)"
        db.session.execute(
            sql2, {"moveinfo_id": moveinfo_id, "plan_id": plan_id})
        db.session.commit()
    except:
        return False
    return True


def move_already_in_plan(plan_id, move_id):
    sql = """SELECT COUNT(mi.move_id) FROM moveinformations mi, movesinplans mp
             WHERE mi.id=mp.moveinfo_id
             AND mp.plan_id=:plan_id AND mi.move_id=:move_id AND mp.visible=TRUE"""
    result = db.session.execute(sql, {"plan_id": plan_id, "move_id": move_id})
    count = result.fetchone()
    count_trim = str(count).strip("(,)")
    if int(count_trim) > 0:
        return False
    return True


def delete_move_from_plan(moveinfo_id):
    sql = "UPDATE movesinplans SET visible=FALSE WHERE moveinfo_id=:moveinfo_id"
    db.session.execute(sql, {"moveinfo_id": moveinfo_id})
    db.session.commit()
    return True


def count_moves_in_plan(plan_id):
    sql = "SELECT COUNT(*) FROM movesinplans WHERE plan_id=:plan_id AND visible=TRUE"
    result = db.session.execute(sql, {"plan_id": plan_id})
    return result.fetchone()[0]


def moves_and_last_weights(plan_id):
    move_list = get_moves_in_plan(plan_id)
    moves_and_weights = []
    for move in move_list:
        name = move[0]
        sets = move[1]
        reps = move[2]
        moveinformation_id = move[4]
        move_id = moves.get_move_id_with_moveinfo_id(moveinformation_id)
        last_documentation = stats.move_last_weight_and_day_with_move_id(
            move_id, plan_id)
        if last_documentation:
            date = last_documentation[0]
            date_to_print = f"kg kirjattu {date}"
            weight = int(last_documentation[1])
        else:
            date_to_print = ""
            weight = ""
        new_row = [name, sets, reps, weight, date_to_print, moveinformation_id]
        moves_and_weights.append(new_row)
    return moves_and_weights
