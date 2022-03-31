from db import db
import users
from flask import session

def create_new_gymplan(name):
    owner_id = users.user_id()
    try:
        sql = "INSERT INTO gymplans (name, owner_id) VALUES (:name, :owner_id)"
        db.session.execute(sql, {"name":name, "owner_id":owner_id})
        db.session.commit()
        return True
    except:
        return False

def get_list():
    owner_id = users.user_id()
    sql = "SELECT name FROM gymplans WHERE owner_id=:owner_id ORDER BY name"
    result = db.session.execute(sql, {"owner_id":owner_id})
    return result.fetchall()

def get_id(name):
    sql = "SELECT id FROM gymplans WHERE name=:name"
    result = db.session.execute(sql, {"name":name})
    id = result.fetchone()[0]
    return id

def get_name(id):
    sql = "SELECT name FROM gymplans WHERE id=:id"
    result = db.session.execute(sql, {"id":id})
    name = result.fetchone()[0]
    return name

def get_moves_in_plan(plan_id):
    sql = "SELECT m.name, mi.sets, mi.reps, mi.weights, mi.id FROM moves m, moveinformations mi WHERE mi.id IN (SELECT id FROM movesinplans WHERE plan_id=:plan_id AND visible=TRUE) AND m.id=mi.move_id"
    result = db.session.execute(sql, {"plan_id":plan_id})
    return result.fetchall()

def add_move(plan_id, move_id, sets, reps, weights):
    sql = "INSERT INTO moveinformations (move_id, sets, reps, weights) VALUES (:move_id, :sets, :reps, :weights) RETURNING id"
    result = db.session.execute(sql, {"move_id":move_id, "sets":sets, "reps":reps, "weights":weights})
    move_id = result.fetchone()[0]
    sql2 = "INSERT INTO movesinplans (move_id, plan_id) VALUES (:move_id, :plan_id)"
    db.session.execute(sql2, {"move_id":move_id, "plan_id":plan_id})
    db.session.commit()
    return True

def delete_move(move_id):
    sql = "UPDATE movesinplans SET visible=FALSE WHERE move_id=:move_id"
    db.session.execute(sql, {"move_id":move_id})
    db.session.commit()
    return True

def get_plan_id_with_moveinfo_id(id):
    sql = "SELECT plan_id FROM movesinplans WHERE id=:id"
    result = db.session.execute(sql, {"id":id})
    id = result.fetchone()[0]
    return id

def get_count_moves(plan_id):
    sql = "SELECT COUNT(*) FROM movesinplans WHERE plan_id=:plan_id AND visible=TRUE"
    result = db.session.execute(sql, {"plan_id":plan_id})
    return result.fetchone()[0]