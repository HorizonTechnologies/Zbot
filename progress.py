import datetime
import time
from db import conn
import json


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
data={
        'q1':{
            'ans1', 'ans2'},
        'q2':{'ans2'},
        'q3':{'ans3',"can't say"}
        }

data = {'What have you done today?': 'nope', 'What are your next plans': 'nope', 'Need help with anything': 'nope'}


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
        
def insert1(user, data,d):
    print(data)
    question = "What have you done today?"
    
   
    todaydata = data[question]
   

   
    date = str(datetoday)
    
    key = getid(user)
    try:
        if question in data.keys():
            db.child("test").child(key).child("progress").child(date).push({user: todaydata})
        db.child("test").child(key).child("standup").child(date).push(data)
    except:
        return "Failed"


def showprogress(user):
    key = getid(user)
    days = ['today','yesterday','tomorrow']
    progress = {}
    dates = [str(datetoday), str(yesterday),str(tomorrow)]
    n = 0
   
    #for date in dates:
    date = str(datetoday)
    check = db.child("test").child(key).child("standup").child(date).get()
    if check.val()!=None:
        print('w')
        data = check.val().values()
        temp =[]
        for l in data:
            
            for s in l:
                
                if 'tomorrow' in s:
                    
                    temp.append(l[s])
                    progress['tomorrow']=temp
                    n=n+1
        
    
      
    return progress
