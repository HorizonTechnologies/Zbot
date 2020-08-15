
icon = 'https://img.icons8.com/emoji/96/000000/penguin--v2.png'
import db
import datetime

conn = db.db()
import blocks

remindersblock = blocks.reminder


reminders = {}

def sendreminder(slack_client):
    x = datetime.datetime.now()
    currenttime = x.strftime("%H") +":"+x.strftime("%M")
  
    for time in reminders:
        if currenttime == time[1]:
            remindersblock(slack_client, time[0])
           




def setreminder(user, timetoset):
    global reminders
    
    try:
        cursor = conn.cursor()
        query = """select * from reminders where slack_id = %s"""
        cursor.execute(query,(user, ))
        count = cursor.rowcount
        
        #print(record)
      
        if count >=2:
            return "You can set a maximum of 2 reminders per day. Contact us \
if you need any help"
        #return record

        query = """ INSERT INTO reminders ( slack_id ,
                                            timetoset,
                                                 ts) VALUES (%s, %s, %s)"""
        insert = (user, timetoset, datetime.datetime.now())
        cursor.execute(query, insert)
        
        conn.commit()
        getreminders()
        return "Success"
        




        
    except:
        return "an error occured"
def getreminders():
    global reminders
    cursor = conn.cursor()
   
    try:
        query = """select slack_id, timetoset from reminders"""
        cursor.execute(query)
        record = cursor.fetchall()
        conn.commit()
        reminders =  record
        return record
    except:
        return ""

    
   
    

reminders = getreminders()

def deletereminder(_id):
    cursor = conn.cursor()
    _id = int(_id)
    
    
    query = """select * from reminders where id = %s"""
    cursor.execute(query,(_id, ))
    count = cursor.rowcount
    if count<1:
        return "Refresh the command"
    
    try:
        query = """DELETE FROM reminders WHERE id = %s"""
        cursor.execute(query,(_id,))
        count = cursor.rowcount
        conn.commit()
    except:
        return "Failed to insert"
    getreminders()
    return "Successfully deleted"


def unset(user):
    cursor = conn.cursor()
    try:
        query = """select timetoset,id from reminders where slack_id = %s"""
        cursor.execute(query, (user,))
        record = cursor.fetchall()
        count = cursor.rowcount
        conn.commit()
    except:
        return ""
    if count <1:
        return ""
    
    return record





def reminder(n,client):
    userslist = client.api_call("users.list")
    for s in userslist['members']:
        if s['is_bot']!= True:
            user = s['id']

            remindersblock(client, user)
            
            
                
            client.api_call(
                  "chat.postMessage",
                  as_user=True,
                  channel=s['id'],
                  icon_url=icon,
                  text=f"Hey <@{user}>!, :wave: Fill in what you've done today",
                  attachments=[{
                    "text": "",
                    "callback_id":  "workform",
                    "color": "#3AA3E3",
                    "attachment_type": "default",
                    "actions": [{
                      "name": "workform",
                      "text": "Submit Today\'s work",
                      "type": "button",
                      "value": "Work_data"
                    }]
                  }]
                )
            client.api_call(
              "chat.postMessage",
              as_user=True,
              channel=s['id'],
              icon_url=icon,
              text="Glad, I\'m here to help in submitting your work data",
              blocks= [
        {
            "type": "section",
            "text": {
                "type": "mrkdwn",
                "text": "Other quick actions"
            },
            "accessory": {
                "type": "static_select",
                "placeholder": {
                    "type": "plain_text",
                    "emoji": True,
                    "text": "Manage"
                },
                "options": [
                    {
                        "text": {
                            "type": "plain_text",
                            "emoji": True,
                            "text": "Request for a day-off"
                        },
                        "value": "dayoff"
                    }
                ]
            }
        }
    ]
            )

   
    
