import datetime
from datetime import timedelta
import time
import os
from db import conn
import register
db = conn()

icon = 'https://img.icons8.com/emoji/96/000000/penguin--v2.png'

def getchannelid(user):
    check = db.child("slack").child("channelslist").get()
    if check.val()!= None:
        check = check.val().values()
        for channel in check:
            if channel['userid'] == user:
                return channel['channelid']
    
def check(client):
        dt = datetime.datetime.now()
        datetoday = datetime.date.today()
        
        check = db.child("reminders").child(datetoday).get()
        check = check.val().values()
        for remind  in check :
            ti = str(dt.hour)+":"+str(dt.minute)
            if remind['time'] == ti:
                channelid = remind['channel']
                
                val = "Remainder : "+ remind['message']
                client.chat_postMessage(
                            channel=channelid,
                            text= val,
                            icon_url=icon,
                            )
    

def remind(msg, user, channel):
    
    dt = datetime.datetime.now()

    datetoday = datetime.date.today()
    tomorrow =datetoday + datetime.timedelta(1)
    yesterday =datetoday + datetime.timedelta(-1)
        
    msg = msg.lower()
    word = msg.split()
    
    if len(word)>= 5 :
        if word[1] != 'me':
            if word[1]=='all':
                channel = "all"
        
            else:
                user = word[1][2:13]
                user = user.upper()
            
                studentslist = register.studentslist()
             
                if user in studentslist:
                    channel = getchannelid(user)
                else:
                    return "user not found. Type Help for more"
            
        if word[2] in ['after', 'in']:
            num = int(word[3])
            if len(word)<6:
                info = ""
            else:
                n=5
                info =[]
                while(n<len(word)):
                    print(word[n])
                    info.append(word[n])
                    n= n+1
                info = ' '.join(info)
            if num in range(60):
                if word[4] in ['days', 'day', 'hour', 'hours','minutes', 'minute']:
                    if word[4] in ['days', 'day']:
                        
                        insertdate = datetoday + datetime.timedelta(num)
                        inserttime = str(dt.hour)+":"+str(dt.minute)
                    if word[4] in ['minutes', 'minute']:
                        insertdate = datetoday
                        time = dt + timedelta(minutes = num)
                        inserttime = str(time.hour)+":"+str(time.minute)
                    if word[4] in ['hour','hours']:
                        insertdate = datetoday
                        time = dt +timedelta(hours = num)
                        inserttime = str(time.hour)+":"+str(time.minute)
                    
                    db.child("reminders").child(insertdate).push({
                        "time" : inserttime,
                        "message": info,
                        "channel" : channel,
                        "user": user,
                        })
                    return "You will be reminded on " + inserttime + " "+ str(insertdate)
                else:
                    return "Failed to set the reminder"
            else:
                return "Dont plan for too long"
        else:
            return "Failed to set the reminder"
    else:
        return "Failed to set the reminder"
"""
    elif word[2]=='at':
        
        print(word)
        
        for l in ['am', 'pm']:
            if l in word:
                print(l)

        num = word[3]
        if len(word[3])==5:
            num = word[3][:2]
        elif len(word[3])==4:
            num = word[3][:1]
        print(num)
        if word[4] in ('tomorrow'):
            insertdate = datetoday + datetime.timedelta(num)
            inserttime = str(dt.hour)+":"+str(dt.minute)
            
            
        print(word[2])
        n=0
    else :
        return false
    print("done")
    """
