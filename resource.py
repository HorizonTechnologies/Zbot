#from db import conn
import db
import datetime

conn = db.db()

icon = 'https://img.icons8.com/emoji/96/000000/penguin--v2.png'



def show():
    try:
        cursor = conn.cursor()
        query = """select * from resources """
        cursor.execute(query)
        record = cursor.fetchall()
        #return record
        print(record)

        for res in record:
            print(res[0])
        return record
    except:
        print("err")

def showresources(slack_client, channel):
    slack_client.api_call(
            "chat.postMessage",
                                channel=channel,
                                text="",
                                icon_url=icon,
                                blocks= [
        {
            "type": "section",
            "text": {
                "type": "mrkdwn",
                "text": "Add a new resource"
            }
        },
        {
            "type": "actions",
            "elements": [
                {
                    "type": "button",
                    "text": {
                        "type": "plain_text",
                        "text": "Add Resource",
                        "emoji": True
                    },
                    "value": "resourceadd"
                }
            ]
        }
    ]          
                                )
    resource = show()
    for res in resource:
                    
                        
                        
        
        slack_client.api_call(
"chat.postMessage",
                    channel=channel,
                    text=res[1] +" - "+ res[2],
                    icon_url=icon,
            )
        slack_client.api_call(
                        "chat.postMessage",
                        channel=channel,
                        text=res,
                        icon_url=icon,
                        blocks= [
                                {
                                "type": "actions",
                                "elements": [
                                    
                                    {
                                        "type": "button",
                                        "text": {
                                            "type": "plain_text",
                                            "emoji": True,
                                            "text": "Update"
                                            
                                        },
                                        "style": "danger",
                                        "value": "resource"+str(res[0])
                                    },
                                    {
                                        "type": "button",
                                        "text": {
                                            "type": "plain_text",
                                            "emoji": True,
                                            "text": "Delete"
                                        },
                                        "style": "danger",
                                        "value": "resource"+str(res[0])
                                    }
                                ]
                                }
                                ]
                        
                        )

     
def insert(name, res, user):
    name = name.lower()
    res = res.lower()

    try:
        cursor = conn.cursor()
        query = """select * from resources where title = %s"""
        cursor.execute(query,(name, ))
        count = cursor.rowcount
        record = cursor.fetchall()
        
        #print(record)
        print(count)
        if count>=1:
            return "Duplicate title, Please choose a different title"
        #return record
        
        
        
    
        
        
        query = """ INSERT INTO resources ( slack_id,title, resource, ts) VALUES (%s,%s, %s, %s)"""
        
        insert = (user, name,res,datetime.datetime.now())
        
        cursor.execute(query, insert)

        conn.commit()
        count = cursor.rowcount
        
        return "successfully inserted "+ name+" - "+ res

    except:
        print("failed to insert")
               

def delete(_id):
    cursor = conn.cursor()
    _id = int(_id)
    
    
    query = """select * from resources where id = %s"""
    cursor.execute(query,(_id, ))
    count = cursor.rowcount
    if count<1:
        return "No record found, Refresh the resources"
    record = cursor.fetchone()
    
    query = """DELETE FROM resources WHERE id = %s"""
    cursor.execute(query,(_id,))
    count = cursor.rowcount
    conn.commit()
    return record[1]+" - "+record[2]+ "Successfully deleted"
    print(count)


  
