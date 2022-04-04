from db import db
from flask import session

def list_all():
    sql = "SELECT name FROM moves"
    result = db.session.execute(sql)
    return result.fetchall()
    
def get_id(name):
    sql = "SELECT id FROM moves WHERE name=:name"
    result = db.session.execute(sql, {"name":name})
    id = result.fetchone()[0]
    return id

def accepted_values(sets, reps, weight):
    if sets == "" or reps == "" or weight == "":
        return False
    return True

def get_moveinfo(moveinformations_id):
    sql = "SELECT move_id, sets, reps, weights FROM moveinformations WHERE id=:moveinformations_id"
    result = db.session.execute(sql, {"moveinformations_id":moveinformations_id})
    return result.fetchone()
 
def document_moveinformation(weight, moveinformations_id, plan_id, date):
    weights = weight
    moveinfo = get_moveinfo(moveinformations_id)
    move_id = moveinfo[0]
    sets = moveinfo[1]
    reps = moveinfo[2]
    sql = "INSERT INTO moveinformations (move_id, sets, reps, weights) VALUES (:move_id, :sets, :reps, :weights) RETURNING id"
    result = db.session.execute(sql, {"move_id":move_id, "sets":sets, "reps":reps, "weights":weights})
    id_of_added_move = result.fetchone()[0]
    db.session.commit()
    document_movedone(id_of_added_move, plan_id, date)
    return True

def document_movedone(move_id, plan_id, day):
    print("?")
    sql = "INSERT INTO movesdone (move_id, plan_id, day) VALUES (:move_id, :plan_id, :day)"
    db.session.execute(sql, {"move_id":move_id, "plan_id":plan_id, "day":day})
    db.session.commit()
    return True
