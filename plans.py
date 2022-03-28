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
