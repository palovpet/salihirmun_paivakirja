from db import db
from flask import session

def get_moves():
    sql = "SELECT name FROM moves"
    result = db.session.execute(sql)
    return result.fetchall()

def show_plan(plan_id):
    sql = "SELECT m.name, mi.sets, mi.reps, mi.weights FROM moves m, moveinformations mi WHERE mi.id IN (SELECT id FROM movesinplans WHERE plan_id=:plan_id) AND m.id=mi.move_id"
    result = db.session.execute(sql, {"plan_id":plan_id})
    return result.fetchall()
    