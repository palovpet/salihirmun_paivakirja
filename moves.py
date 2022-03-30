from db import db
from flask import session

def get_moves():
    sql = "SELECT name FROM moves"
    result = db.session.execute(sql)
    return result.fetchall()
    
def get_move_id(name):
    sql = "SELECT id FROM moves WHERE name=:name"
    result = db.session.execute(sql, {"name":name})
    id = result.fetchone()[0]
    return id