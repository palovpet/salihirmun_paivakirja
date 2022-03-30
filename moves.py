from db import db
from flask import session

def get_moves():
    sql = "SELECT name FROM moves"
    result = db.session.execute(sql)
    return result.fetchall()

def show_plan(id):
    sql = "SELECT M.name, I.sets, I.reps, I.weights FROM moves M, moveinformations I, movesinplans P WHERE M.id=I.id AND I.id=P.move_id AND P.plan_id=:id"
    result = db.session.execute(sql, {"id":id})
    moves = result.fetchall()
    return moves