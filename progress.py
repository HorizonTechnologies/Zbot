import datetime
import time
import db
import json


datetoday = datetime.date.today()
tomorrow =datetoday + datetime.timedelta(1)
yesterday =datetoday + datetime.timedelta(-1)

conn = db.db()








def insert2(userid,data,d):
    if d==0:
        date = str(datetoday)
    else:
        date = str(tomorrow)
    try:
    
        cursor = conn.cursor()
        data = json.dumps(data)
        query = """ INSERT INTO standup1 ( slack_id, report, ts) VALUES (%s, %s, %s)"""
        insert = (userid,data,datetime.datetime.now())
        cursor.execute(query, insert)

        
        count = cursor.rowcount
        conn.commit()
        print (count, "Record inserted successfully into mobile table")

    except:
        print("failed to insert")


def show(user):
    cursor = conn.cursor()
    query = """select report from standup1 where slack_id = %s and ts > %s """
    cursor.execute(query, (user, datetoday, ))
    record = cursor.fetchall()
    return record
    print(record)


def dayoff(user):
    date = str(datetoday)
    
    check = db.child("dayoffs").child(date).get()
    if check.val()!=None:
        
        data = check.val().values()
        if user in data:
            print('err')
           
            return "You've already requested!"
            
        else:
            db.child("dayoffs").child(date).push(user)


