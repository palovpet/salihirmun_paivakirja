import db
import users
from flask import session

def create_new_gymplan(name):
    owner_id = users.user_id()
    sql = "INSERT INTO gymplans (name, owner_id) VALUES (:name, :owner_id)"
    db.session.execute(sql, {"name":name, "owner_id":owner_id})
    db.session.commit()
    return True
