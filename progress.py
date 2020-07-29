import datetime
import time
from db import conn



datetoday = datetime.date.today()
tomorrow =datetoday + datetime.timedelta(1)
yesterday =datetoday + datetime.timedelta(-1)

db = conn()

def getid(user):
    check = db.child("test").get()
    if check.val()!=None:
        for l in check:
            s = l.val()
            for k in s.keys():
                if s[k] == user:
                    key = l.key()
                    return key

def insert(user, work,d):
    if d==0:
        date = str(datetoday)
    else:
        date = str(tomorrow)
    try:
        key = getid(user)
        db.child("test").child(key).child("progress").child(date).push({user : work})
    except:
        print("failed to insert")
    
    

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
dayoff('new1')    

    

def showprogress(user):
    key = getid(user)
    date = str(datetoday)
    check = db.child("test").child(key).child("progress").child(date).get()
    todayplan = []
    
        
    if check.val()!=None:
        data = check.val().values()
        
        for l in data:
            try:
                todayplan.append(l[user])
            except:
                n=0
    
    date = str(yesterday)
    check = db.child("test").child(key).child("progress").child(date).get()
    yesterdayplan = []
    if (check.val())!=None:
        data = check.val().values()
        
        for l in data:
            try:
                yesterdayplan.append(l[user])
            except:
                n=0
        

    date = str(tomorrow)
    check = db.child("test").child(key).child("progress").child(date).get()
    tomplan = []
    if (check.val())!=None:
        data = check.val().values()
        
        for l in data:
            try:
                tomplan.append(l[user])
            except:
                n=0
                
    print(todayplan, yesterdayplan, tomplan)
    return todayplan,yesterdayplan, tomplan            
    

                
