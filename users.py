from flask import session
from werkzeug.security import check_password_hash, generate_password_hash
from db import db

def login(username, password):
    sql = "SELECT id, password FROM users WHERE username=:username"
    result = db.session.execute(sql, {"username": username})
    user = result.fetchone()
    if not user:
        return False
    if check_password_hash(user.password, password):
        session["user_id"] = user[0]
        session["user_name"] = username
        return True
    return False


def logout():
    del session["user_id"]


def signin(username, password):
    if username_and_password_valid(username) and username_and_password_valid(password):
        hash_value = generate_password_hash(password)
        try:
            sql = "INSERT INTO users (username,password) VALUES (:username,:password)"
            db.session.execute(
                sql, {"username": username, "password": hash_value})
            db.session.commit()
        except:
            return False
        return login(username, password)
    return False


def username_and_password_valid(string):
    return len(string) < 20 and len(string) > 3


def user_id():
    return session.get("user_id", 0)


def get_count_plans():
    owner_id = user_id()
    sql = "SELECT COUNT(*) FROM gymplans WHERE owner_id=:owner_id"
    result = db.session.execute(sql, {"owner_id": owner_id})
    return result.fetchone()[0]
