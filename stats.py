from sqlalchemy import null
from db import db
from flask import session

def move_stats(plan_id):
    sql = "SELECT m.name, mi.sets, mi.reps, mi.weights, d.day, m.id FROM moves m, moveinformations mi, movesdone d WHERE mi.id IN (SELECT move_id FROM movesdone WHERE plan_id=:plan_id) AND m.id=mi.move_id AND d.move_id=mi.id ORDER BY m.name, d.day DESC" 
    result = db.session.execute(sql, {"plan_id":plan_id})
    list_moves_done = result.fetchall()
    printable = []
    edel = 0;
    for move in list_moves_done:   
        mid = move[5] 
        name = f"{move[0]} :"
        sets = f"{move[1]} sarjaa "
        reps = f"{move[2]} toistoa"
        weight = f": {move[3]} kg"
        date = str(move[4])
        if mid == edel:
            row = ["", "", "", date, weight]
            printable.append(row)
            edel = mid
        else:
            row = [name, sets, reps, date, weight]
            empty = ["", "", "", "", ""]
            if (edel > 0):
                printable.append(empty)
                printable.append(empty)
            printable.append(row)
            edel = mid
   
    return printable
    

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

#not in use 
def workout_stats_per_one(plan_id):
    data = extract_workout_stats_per_one(plan_id)
    return data

#not in use
def extract_workout_stats_per_one(plan_id):
    sql = "SELECT EXTRACT (DAY from day) AS DAY, EXTRACT (MONTH FROM day) AS MONTH, EXTRACT (YEAR FROM day) AS YEAR FROM movesdone WHERE plan_id=:plan_id GROUP BY DAY"
    result = db.session.execute(sql, {"plan_id":plan_id})
    results = result.fetchall()

    data = []

    for r in results:
        day = int(r[0])
        month = int(r[1])
        year = int(r[2])
        data.append([day,month,year])
    return data

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




