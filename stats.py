from db import db
from flask import session
import users
import datetime

def move_stats(plan_id):
    sql = "SELECT m.name, mi.sets, mi.reps, mi.weights, d.day FROM moves m, moveinformations mi, movesdone d WHERE mi.id IN (SELECT move_id FROM movesdone WHERE plan_id=:plan_id) AND m.id=mi.move_id AND d.move_id=mi.id ORDER BY m.name" 
    result = db.session.execute(sql, {"plan_id":plan_id})
    return result.fetchall()

def gymvisits_one(plan_id):
    sql = "SELECT COUNT(DISTINCT day) FROM movesdone WHERE plan_id=:plan_id"
    result = db.session.execute(sql, {"plan_id":plan_id})
    count = result.fetchone()
    count_trimmed = str(count).strip(",(')")  
    return count_trimmed

def first_time_one(plan_id):
    sql = "SELECT MIN(day) FROM movesdone WHERE plan_id=:plan_id"
    result = db.session.execute(sql, {"plan_id":plan_id})
    date = result.fetchone()  
    date_toprint = trim_date(date)  
    return date_toprint

def last_time_one(plan_id):
    sql = "SELECT MAX(day) FROM movesdone WHERE plan_id=:plan_id"
    result = db.session.execute(sql, {"plan_id":plan_id})
    date = result.fetchone()  
    date_toprint = trim_date(date)  
    return date_toprint

def trim_date(date):
    date_trimmed = str(date).strip("datetime.date()")
    datelist = date_trimmed.split(",")
    year = datelist[0]
    month = datelist[1]
    day = datelist[2].strip(")")
    month_long = get_month_with_number(int(month))  
    return f"{day} {month_long} {year}"


def get_month_with_number(x):
    if x == 1:
        return "tammikuuta"
    if x == 2:
        return "helmikuuta"
    if x == 3:
        return "maaliskuuta"
    if x == 4:
        return "huhtikuuta"
    if x == 5:
        return "toukokuuta"
    if x == 6:
        return "kesäkuuta"
    if x == 7:
        return "heinäkuuta"
    if x == 8:
        return "elokuuta"
    if x == 9:
        return "syyskuuta"
    if x == 10:
        return "lokakuuta"
    if x == 11:
        return "marraskuuta"
    if x == 12:
        return "joulukuuta"




