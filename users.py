import secrets
from flask import session, abort, request
from werkzeug.security import check_password_hash, generate_password_hash
from db import db

def login(username, password):
    sql = "SELECT id, password FROM users WHERE username=:username"
    result = db.session.execute(sql, {"username": username})
    user = result.fetchone()
    if not user:
        return False
    if not check_password_hash(user.password, password):
        return False
    session["user_id"] = user[0]
    session["user_name"] = username
    session["csrf_token"] = secrets.token_hex(16)
    return True

def check_csrf():
    if session["csrf_token"] != request.form["csrf_token"]:
        abort(403)


def logout():
    del session["user_id"]


def signin(username, password):
    if not username_and_password_valid(username, password):
        return False
    hash_value = generate_password_hash(password)
    try:
        sql = "INSERT INTO users (username,password) VALUES (:username,:password)"
        db.session.execute(
            sql, {"username": username, "password": hash_value})
        db.session.commit()
    except:
        return False
    return True


def username_and_password_valid(string1, string2):
    return len(string1) <= 20 and len(string2) <= 20 and len(string1) >= 3 and len(string2) >= 3


def user_id():
    return session.get("user_id", 0)


def get_count_plans():
    owner_id = user_id()
    sql = "SELECT COUNT(*) FROM gymplans WHERE owner_id=:owner_id"
    result = db.session.execute(sql, {"owner_id": owner_id})
    return result.fetchone()[0]
