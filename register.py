from db import conn

db = conn()
def register(code, user, channel):
    print("run")
    check = db.child("test").get()
    for l in check:
        s = l.val()
        if 'slackid' in s.keys():
            if s['slackid'] == user:
                return "already registered. Contact us if you are facing any problem"
    for l in check:
        s = l.val()
        if 'slacktoken' in s.keys():
            
            if str(s['slacktoken']) == code:
                if 'slackid' in s.keys():
                    print("yes")
                    return "someting went wrong. Contact admin "
                else:
                    key = l.key()
                    
                    db.child("test").child(key).update({"slackid":user})
                    db.child("slack").child("channelslist").push({
                        'userid': user,
                        'channelid':channel,
                        })
    
                    return "success"
        
            
    
def channelslist():
    check = db.child("slack").child("channelslist").get()
    check = check.val().values()
    channels=[]
    for channel in check:
        channels.append(channel['channelid'])
    return channels
                

def studentslist():
    check = db.child("test").get()
    studentsid = []
    for l in check:
        s = l.val()
        if 'slackid' in s.keys():
            studentsid.append(s['slackid'])
        #studentsid.append(key.key())
    return studentsid

