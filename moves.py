from db import db


def list_all():
    sql = "SELECT name FROM moves"
    result = db.session.execute(sql)
    return result.fetchall()


def get_move_id_with_name(name):
    sql = "SELECT id FROM moves WHERE name=:name"
    result = db.session.execute(sql, {"name": name})
    move_id = result.fetchone()[0]
    return move_id


def get_move_id_with_moveinfo_id(moveinfo_id):
    sql = "SELECT move_id FROM moveinformations WHERE id=:moveinfo_id"
    result = db.session.execute(sql, {"moveinfo_id": moveinfo_id})
    return result.fetchone()[0]


def sets_and_reps_valid(sets, reps):
    if sets == "" or reps == "":
        return False
    if int(sets) < 1 or int(reps) < 1:
        return False
    return True


def weight_valid(weight):
    if int(weight) < 0:
        return False
    return True


def get_moveinfo(moveinfo_id):
    sql = "SELECT move_id, sets, reps, weight FROM moveinformations WHERE id=:moveinfo_id"
    result = db.session.execute(sql, {"moveinfo_id": moveinfo_id})
    return result.fetchone()


def document_moveinfo(weight, moveinfo_id, plan_id, date):
    weight = weight
    moveinfo = get_moveinfo(moveinfo_id)
    move_id = moveinfo[0]
    sets = moveinfo[1]
    reps = moveinfo[2]
    try:
        sql = """INSERT INTO moveinformations (move_id, sets, reps, weight)
                 VALUES (:move_id, :sets, :reps, :weight) RETURNING id"""
        result = db.session.execute(
            sql, {"move_id": move_id, "sets": sets, "reps": reps, "weight": weight})
        moveinfo_id = result.fetchone()[0]
        db.session.commit()
    except:
        return False
    return document_movedone(moveinfo_id, plan_id, date)


def document_movedone(moveinfo_id, plan_id, day):
    try:
        sql = """INSERT INTO movesdone (moveinfo_id, plan_id, day) 
                VALUES (:moveinfo_id, :plan_id, :day)"""
        db.session.execute(
            sql, {"moveinfo_id": moveinfo_id, "plan_id": plan_id, "day": day})
        db.session.commit()
    except:
        return False
    return True
