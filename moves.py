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