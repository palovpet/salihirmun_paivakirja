from db import db
from flask import session, request, abort
from werkzeug.security import check_password_hash, generate_password_hash

def login(username, password):
    sql = "SELECT id, password FROM users WHERE username=:username"
    result = db.session.execute(sql, {"username":username})
    user = result.fetchone()
    if not user:
        return False
    else:
        if check_password_hash(user.password, password):
            session["user_id"] = user[0]
            session["user_name"] = username
            return True
        else:
            return False

def logout():
    del session["user_id"]

def signin(username, password):
    hash_value = generate_password_hash(password)
    try:
        sql = "INSERT INTO users (username,password) VALUES (:username,:password)"
        db.session.execute(sql, {"username":username, "password":hash_value})
        db.session.commit()
    except:
        return False
    return login(username, password)

def user_id():
    return session.get("user_id",0)

def get_count_plans():
    owner_id = user_id()
    sql = "SELECT COUNT(*) FROM gymplans WHERE owner_id=:owner_id"
    result = db.session.execute(sql, {"owner_id":owner_id})
    return result.fetchone()[0]
