
from flask import Flask, request, make_response, Response
import os
import json
from slackeventsapi import SlackEventAdapter
import progress 
from slackclient import SlackClient
from threading import Thread
import random
import schedule
import resource as resourcemodule

import progress 
import remind
import register
import customremind
import time
import requests


from dotenv import load_dotenv

load_dotenv()


icon = 'https://img.icons8.com/emoji/96/000000/penguin--v2.png'
preveventid = ""
prevtext=""
usersdata = {}
SLACK_BOT_TOKEN = os.getenv("SLACK_BOT_TOKEN")
SLACK_SIGNIN_SECRET = os.getenv("SLACK_SIGNIN_SECRET")
SLACK_VERIFICATION_TOKEN = os.getenv("SLACK_VERIFICATION_TOKEN")

#context=('/home/admin/cloudflare.cer.pem','/home/admin/cloudflare.privkey.pem')


# Slack client 
slack_client = SlackClient(SLACK_BOT_TOKEN)

# Flask web server for incoming traffic from Slack
app = Flask(__name__)
try:
    slack_events_adapter = SlackEventAdapter(SLACK_SIGNIN_SECRET, "/slack/events", app)
except:
    print("error")


#greetings and commands list
greetings = ['Hello! ', 'Hey','Glad', 'Hai']
commands = ['hello','hello ','help ','joke']

#schduling messages

schedule.every().day.at("11:00").do(remind.reminder,'0',slack_client)

schedule.every().day.at("20:00").do(remind.reminder,'0',slack_client)
schedule.every(1).seconds.do(remind.reminder,'0',slack_client)

def _reminders():
    """
    Loop to check the pending remainders 
    """
    while True:
        time.sleep(10)
        schedule.run_pending()

  
#getting bot info
response = slack_client.api_call("auth.test")


botid = response['user_id']




#interactions HTTP POST Route
@app.route("/slack/message_actions", methods=["POST"])
def _message_actions():
    """
    /slack/message_actions end point to receive HTTP POST Requests from Slack
    
    After Analysing the type of payload received whether a button click, dialogue,
    interactive message, dialogue submission repective response will be sent back to
    the user provoked the action
    """
    
    message_action = json.loads(request.form["payload"])
    
    
                                
    user_id = message_action["user"]["id"]
    channel_id = message_action['channel']['id']
    
    if message_action["type"] == "interactive_message":
        print(message_action["trigger_id"])
        # Add the message_ts to the user's order info
        for actions in message_action['actions']:
            if actions['name']=="workform":
     
        # Show the ordering dialog to the user
                chainmessages = ['What have you done today?',
                     "What are your next plans",
                     "Need help with anything"]
                slack_client.api_call(
                        "chat.postMessage",
                        channel= channel_id,
                        text =chainmessages[0],
                        icon_url=icon,
                        attachments=[]
                        )
                open_dialog = slack_client.api_call(
                    "dialg.open",
                    trigger_id=message_action["trigger_id"],
                    dialog={
                        "title": "Daily Syncup",
                        "submit_label": "Submit",
                        "callback_id": user_id + "workform",
                        
                        
                        "elements": [
                {
                    "type": "text",
                    "label": "What have you done?",
                    "name": "todayplan"
                },
                {
                    "type": "text",
                    "label": "What are your tomorrow plans?",
                    "name": "yesterdaywork"
                },
                
            ]
                    } 
                )

        

       
    elif message_action["type"]=="block_actions":
        action = message_action.get('actions')
        
        actiontype = action[0]['type']
        
        if actiontype=='button':
            text = action[0]['text']['text']
            value = action[0]['value']
            if text=="Delete":
                if value.startswith('resource'):
                    del_id = value[8:]
                    val = resourcemodule.delete(del_id)
                 
                    slack_client.api_call(
                        "chat.postMessage",
                        channel= channel_id,
                        text =val,
                        icon_url=icon,
                        attachments=[]
                        )
                    
            if value == 'resourceadd':
                open_dialog = slack_client.api_call(
                    "dialog.open",
                    trigger_id=message_action["trigger_id"],
                    dialog={
                        "title": "Add a resource",
                        "submit_label": "Submit",
                        "callback_id":'resourceadd',
                        
                        
                        "elements": [
                {
                    "type": "text",
                    "label": "name",
                    "name": "resource"
                },
                {
                    "type": "text",
                    "label": "links/description",
                    "name": "link"
                },
                
            ]
                    } 
                )
                
            if text == 'Update':
                if value.startswith('resource'):
                    del_id = value[8:]
                    open_dialog = slack_client.api_call(
                    "dialog.open",
                    trigger_id=message_action["trigger_id"],
                    dialog={
                        "title": "Daily Syncup",
                        "submit_label": "Submit",
                        "callback_id":'update'+del_id,
                        
                        
                        "elements": [
                {
                    "type": "text",
                    "label": "name",
                    "name": "resource"
                },
                {
                    "type": "text",
                    "label": "links/description",
                    "name": "link"
                },
                
            ]
                    } 
                )

                    update_id=value[8:]
                    
              
                
            
        if actiontype=='static_select':
            option = action[0]['selected_option']['value']
           
            if option == 'dayoff':
                val = progress.dayoff(user_id)
                slack_client.api_call(
                    "chat.postMessage",
                    channel= channel_id,
                    icon_url=icon,
                    text=val,
                    attachments=[]
                )
            if option == "pending":
                slack_client.api_call(
                    "chat.postMessage",
                    channel= channel_id,
                    icon_url=icon,
                    text=":thumbsup: Great! Go ahead",
                    attachments=[]
                )
            
        
    elif message_action["type"] == "dialog_submission":
        
        formdata = message_action['submission']
  
        callbackid= message_action['callback_id']
        
        if callbackid.startswith('updateresource'):
            update_id = callbackid[14:]
            resourcemodule.update(update_id,formdata['resource'],formdata['link'] )
            val = 'Under Construction'
        elif callbackid.startswith('resourceadd'):
            formdata = message_action['submission']
            val = resourcemodule.insert(formdata['resource'],formdata['link'])
        elif callbackid.startswith('workdata'):
            todaywork = formdata['todayplan']
            yesterdaywork = formdata['submission']['yesterdaywork']
            
        #inserting into  ( '0'- today and '1'-yesterdays)
            progress.insert(user_id,todaywork, 0)
            progress.insert(user_id,yesterdaywork, 1)
            val = message_action['submission']['todayplan'] +" \n  You have done '"+message_action['submission']['yesterdaywork']+"' yesterday"
        
        slack_client.api_call(
            "chat.postMessage",
            channel= channel_id,
            icon_url=icon,
            text="",
            
            attachments=[{
                    "text": val,
                    "color": "#3AA3E3",
                    "attachment_type": "default",
                    
                  }]
        )

    return make_response("", 200)



#Responding to message events
@slack_events_adapter.on("message")
def _handle_message(event_data):

    """
    Receiving message events from the slack
    The payload received will be sent to another function by a different thread, then HTTP 200 
    Reponse will be sent back to the slack
    """
    global preveventid
    print(event_data)
    print(event_data['event_id'])
    if preveventid == event_data['event_id']:
        return make_response("", 200)
    else:
        preveventid = event_data['event_id']
        
    #threading a new process to handle the messages
        Thread(target=_handling_message,args=(event_data,),daemon=True).start()
       
        #returning the post request with HTTP 200
        return make_response("", 200)
        
    
def verification(token):
    if token != os.getenv('SLACK_VERIFICATION_TOKEN'):
        print('error')
        return True
    else:
        return False
    
def _handling_message(event_data):
    """
    Handling messages according to the command/message received 
    The event_data arguement is the payload for the message event, according to the message
     recieved respective action will be performed
    """
    if verification(event_data['token']):
        return make_response("", 200)
        

    global prevtext
    data = event_data["event"]
    channel_id = data["channel"]
    
    print(data['text'])
    
    chainmessages = ['What have you done today?',
                     "What are your next plans",
                     "Need help with anything"]
    if data.get("subtype") is None and data.get("user") != botid:
        user_id = data['user']
        if prevtext in chainmessages:
                if prevtext == chainmessages[0]:
                    usersdata[user_id]={}
                n = 0
                usersdata[user_id][prevtext] = data['text']
                for message in chainmessages:
                    if prevtext != message:
                        n=n+1
                    else:
                        val = 'Good! Keep Going'
                        if n != len(chainmessages)-1:
                            val = chainmessages[n+1]
                           
                            slack_client.api_call(
                            "chat.postMessage",
                                            channel=channel_id,
                                            text= val,
                                            icon_url=icon,
                                            )
                        if n == len(chainmessages)-1:
                            print(usersdata[user_id])
                            progress.insert2(user_id, usersdata[user_id],0)
                            print(usersdata)
                            for response in usersdata[user_id]:
                                
                                slack_client.api_call(
                                "chat.postMessage",
                                                channel=channel_id,
                                                text= "",
                                                icon_url=icon,
                                                
                                                    attachments=[{
                                                    "text": response +"\n "+usersdata[user_id][response] ,
                                                    "color": "#3AA3E3",
                                                    "attachment_type": "default",
                                                    
                                                  }]
                                                )
                            
       
    prevtext = data['text']
   
    if data.get("subtype") is None:
        data = event_data["event"]
        
        
        message = data['text']
        user_id = data['user']
  
        
        
        _id = "<@"+botid+">"
        
        #checking whether the message is in DM or in channel
        if(data['channel_type'] == 'im'):
           
            message = message.lower()
            dat = message
        else:
        
            if (message.startswith(_id)):
                word = message.split()
           
                if _id in word:
                    word.remove(_id)
                    message = ' '.join(word)
                
                message = message.lower() 
                dat = message
            else:
                message=""
           
        if message in commands or dat.startswith("register "):
           
            
            work = message
            
            
            if message == 'joke':
                url ="https://official-joke-api.appspot.com/random_joke"
             
                try:
                    data = requests.get(url = url)
                    data =data.content
                    data = json.loads(data)
                   
                    slack_client.api_call(
                "chat.postMessage",
                                channel=channel_id,
                                text= data['setup']+" "+ data['punchline'],
                                icon_url=icon,
                                )
                except:
                    slack_client.api_call(
                "chat.postMessage",
                                channel=channel_id,
                                text= "Failed to load",
                                icon_url=icon,
                                )
                    
                                
            if message.startswith("register "):
                
                user = data['user']
                code = message[9:]
                val = register.register(code, user_id, channel_id)
                if val==None:
                    val = "Please check your code and try again"
                    slack_client.api_call(
            "chat.postMessage",
                            channel=channel_id,
                            text= val,
                            icon_url=icon,
                            )
                elif val == "success":
                    slack_client.api_call(
            "chat.postMessage",
                            channel=channel_id,
                            text= val,
                            icon_url=icon,
                            blocks= [
                            {
                                "type": "section",
                                "text": {
                                "type": "mrkdwn",
                                "text": f"Hi <@{user_id}> :smiley:"
                            }
                        },
                        {
                            "type": "section",
                            "text": {
                                "type": "mrkdwn",
                                "text": "Great to see you here!  You're successfully registered "
                            }
                        },
                        {
                            "type": "section",
                            "text": {
                                "type": "mrkdwn",
                                "text": "• Don't forget to SyncUp your daily progress \n • Go through all of the resources \n Type `Help` to know me better"
                            }
                        }
                    ])
                else:
                    slack_client.api_call(
            "chat.postMessage",
                            channel=channel_id,
                            text= val,
                            icon_url=icon,)
                    
            if dat == "hello":
                greet = random.choice(greetings)
                val = greet + f" <@{user_id}>"
                slack_client.api_call(
        "chat.postMessage",
                channel=channel_id,
                text=val,
                icon_url=icon,
                
                )
                
            
            
                    
                    
                    
            if dat == "help":
                val = f"Welcome <@{user_id}>, I am your Horizon Zbot to help you in managing your progress. \n Kindly Register with your Unique slackid to get started \n Enter 'register <unique id>' \n 1. Use commands like 'today','next' to save your todays and tomorrows work data \n 2. Type 'show' to display your todays and tomorrows plans \n 3.Type 'Resources' to know about all the resources that we are in "                
                slack_client.api_call(
        "chat.postMessage",
                channel=channel_id,
                text=val,
                icon_url=icon,
                blocks =  [
    {
        "type": "section",
        "text": {
            "type": "mrkdwn",
            "text": "Hey there 👋 I'm Your Horizonslackbot . I'm here to help you create and manage tasks in Slack.\n You can quickly get started with this bot by registering yourselves. \n Use `register <unique code>` to use all of this bot features"
        }
    },
    {
        "type": "section",
        "text": {
            "type": "mrkdwn",
            "text": "*1️⃣ `Today` command*. Type `Today` followed by the short description of your work and it will be saved"
        }
    },
    {
        "type": "section",
        "text": {
            "type": "mrkdwn",
            "text": "*2️⃣ `Next` command*. Type `Next` followed by the short description of your work and it will be saved"
        }
    },
    {
        "type": "section",
        "text": {
            "type": "mrkdwn",
            "text": "*3️⃣ `Show` command*. Type `Show` command to display your today and tomorrow work data"
        }
    },
    {
        "type": "section",
        "text": {
            "type": "mrkdwn",
            "text": "*4️⃣ `Resources` command*. Type `resources` to display the resources of the HorizonTech that you will be working on"
        }
    }
] )
       
        
        elif dat.startswith("today") or dat.startswith("next") or dat.startswith("show") or dat.startswith("register ") or dat.startswith("resource add") or dat.startswith("resources") or dat.startswith("resource delete ") or dat.startswith("submit") or dat.startswith("remind "):
            
            if dat =="submit":
                user = data['user']
                channel = data['channel']
                slack_client.api_call(
            "chat.postMessage",
                    channel=channel_id,
                    text="Lets Start",
                    icon_url=icon,
                        )
                slack_client.api_call(
            "chat.postMessage",
                    channel=channel_id,
                    text="What have you done today?",
                    icon_url=icon,
                        )
                '''
                slack_client.api_call(
                  "chat.postMessage",
                  as_user=True,
                  icon_url=icon,
                  channel=channel_id,
                  text="Hey TEST!, :wave: Fill in what you've done today",
                  attachments=[{
                    "text": "",
                    "callback_id":  "workform",
                    "color": "#3AA3E3",
                    "attachment_type": "default",
                    "actions": [{
                      "name": "workform",
                      "text": "Report",
                      "type": "button",
                      "value": "Work_data"
                    }]
                  }]
                )
                slack_client.api_call(
              "chat.postMessage",
              as_user=True,
              channel=channel_id,
              
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
                    },
                    
                ]
            }
        }
    ]
            )'''
                

                
        
        
            elif dat.startswith("remind "):
                user = data['user']
                channel = data['channel']
                val = customremind.remind(dat, user, channel)
                slack_client.api_call(
            "chat.postMessage",
                    channel=channel_id,
                    text=val,
                    icon_url=icon,
                        )
            elif dat.startswith("today"):
                
                work = dat[5:]
                if work and work.strip():
                    val = "Great! work You've done. Your work"+ " '"+ work +"' "+" was submitted. Submit any others if you want to."
                    progress.insert(user_id, work,0)
                else :
                    val = "please type something"
                slack_client.api_call(
                    "chat.postMessage",
                    channel=channel_id,
                    text=val,
                    icon_url=icon,
                    )
                #the work data is stored a string the the 'Work' var
                
            elif dat.startswith("next"):
                userid = data['user']
               
                work = dat[4:]
                
                if work and work.strip():
                    val = "Nice! Go on with work. Meanwhile set a remainder of the work or Type Show to check your planned works"
                    progress.insert(userid, work,1)
                else :
                    val = "Please enter details of the work. "
                slack_client.api_call(
            "chat.postMessage",
                    channel=channel_id,
                    text=val,
                    icon_url=icon,
                    )
                #the work data is stored in a string the the 'Work' var
            elif dat.startswith("show"):
                colors = ['#EBB713', '#F91C3E', '#16A085', '#212F3D', '#F1C40F']
                user = data['user']
                report = progress.show(user)
                
                for response in report:
                    val =""
                    
                    for res in response:
                        for temp in res:
                            val = val+ " *"+temp+"* " + "\n" + res[temp]
                            val = val+"\n"
                            print(temp)
                    slack_client.api_call(
                                    "chat.postMessage",
                                    channel=channel_id,
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
                                    channel=channel_id,
                                    text= "",
                                    icon_url=icon,
                                                            
                                    blocks= [
		{
			"type": "divider",
			
                        }]
                                )
                    
                           
                       
                
            
                
        
            elif dat.startswith("resource add"):
                
                
                slack_client.api_call(
            "chat.postMessage",
                                channel=channel_id,
                                text=res,
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
                
                
                
            elif dat.startswith("resources"):
                print("show resource command running")
                print("test")
                resource = resourcemodule.show()
                slack_client.api_call(
            "chat.postMessage",
                                channel=channel_id,
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
                
                for res in resource:
                    
                        
                        
                    
                    slack_client.api_call(
            "chat.postMessage",
                                channel=channel_id,
                                text=res[1] +" - "+ res[2],
                                icon_url=icon,
            )
                    slack_client.api_call(
                "chat.postMessage",
                                    channel=channel_id,
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
                            
                   
            
    
    
        
        
        
                
                
            
            
     

if __name__ == "__main__":
    """
    This is the main function
    We are running the reminders() in a different thread to have both actions performed independently
    
    """
    Thread(target=_reminders,daemon=True).start()
    app.run(port=3001)
    #app.run(host='0.0.0.0', port=8443, ssl_context=context)
