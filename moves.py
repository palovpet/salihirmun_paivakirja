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
 
def document(weight, moveinformations_id):
    weights = weight
    moveinfo = get_moveinfo(moveinformations_id)
    move_id = moveinfo[0]
    sets = moveinfo[1]
    reps = moveinfo[2]
    #tallenna tietokantaan
    return True


