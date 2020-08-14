import datetime
import time
import db
import json


datetoday = datetime.date.today()
tomorrow =datetoday + datetime.timedelta(1)
yesterday =datetoday + datetime.timedelta(-1)

conn = db.db()


icon = 'https://img.icons8.com/emoji/96/000000/penguin--v2.png'





def insert2(userid,data,d):
    
    try:
    
        cursor = conn.cursor()
        data = json.dumps(data)
        query = """ INSERT INTO standup1 ( slack_id,
                                             report,
                                             ts
                                        ) VALUES (%s, %s, %s)"""
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
    conn.commit()

    return record
    





def dayoff(user):
   
    try:
        cursor = conn.cursor()
        query = """select * from dayoff where slack_id = %s"""
        cursor.execute(query,(user, ))
        count = cursor.rowcount
        
        #print(record)
        
        if count>=1:
            return "You've already requested for a dayoff, today"
        #return record

        query = """ INSERT INTO dayoff ( slack_id , ts) VALUES (%s, %s)"""
        insert = (user, datetime.datetime.now())
        cursor.execute(query, insert)
        conn.commit()
        return "You've requested for a dayoff"
    except:
        return "an error occured"


    


def report(user,channel,slack_client):
    report = show(user)
    slack_client.api_call(
            "chat.postMessage",
            channel = channel,
            icon_url=icon,
            text = f" Great Work! <@{user}> "
    )
    slack_client.api_call(
                        "chat.postMessage",
                        channel=channel,
                        text= "Your responses",
                        icon_url=icon,
                        blocks = [
                            {
                                "type":"section",
                                "text":{
                                    "type":"mrkdwn",
                                    "text": f"`"\
+str(datetime.datetime.now().strftime("%D"))+"` You've submitted *"+ \
str(len(report))+"* report's today" 

                                    
                                }
                            }
                        ]
    )
                
    for response in report:
        val =""
        
        for res in response:
            for temp in res:
                val = val+ " *"+temp+"* " + "\n" + res[temp]
                val = val+"\n"
                
        slack_client.api_call(
                        "chat.postMessage",
                        channel=channel,
                        text= "Your responses",
                        icon_url=icon,
                                                
                        blocks= [
                                {
                                "type": "section",
                                "text": {
                                    "type": "mrkdwn",
                                    "text": val
                                },
                                            }]
                                                    )
        slack_client.api_call(
                        "chat.postMessage",
                        channel=channel,
                        text= "",
                        icon_url=icon,
                                                
                        blocks= [
                                {
                                    "type": "divider",
                                    
                                }]
                    )