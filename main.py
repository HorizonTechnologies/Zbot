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
import blocks
import time
import requests
import custom



from dotenv import load_dotenv

load_dotenv()


botname = custom.botname
Companyname = custom.companyname
icon = custom.icon
preveventid = ""
prevtext=""
usersdata = {}

#report questions to ask
chainmessages = custom.reportquestions




SLACK_BOT_TOKEN = os.getenv("SLACK_BOT_TOKEN")
SLACK_SIGNIN_SECRET = os.getenv("SLACK_SIGNIN_SECRET")
SLACK_VERIFICATION_TOKEN = os.getenv("SLACK_VERIFICATION_TOKEN")

context=(os.getenv("certificate"),os.getenv("private_key"))


# Slack client 
slack_client = SlackClient(SLACK_BOT_TOKEN)

# Flask web server for incoming traffic from Slack
app = Flask(__name__)

slack_events_adapter = SlackEventAdapter(
                                            SLACK_SIGNIN_SECRET,
                                            "/slack/events", 
                                            app
                                        )


#greetings and commands list
greetings = ['Hello! ', 'Hey','Glad', 'Hai']
commands = ['hello','hello','help','joke']

#schduling messages

schedule.every().day.at(custom.time1).do(remind.reminder,'0',slack_client)

schedule.every().day.at(custom.time2).do(remind.reminder,'0',slack_client)
schedule.every(3).seconds.do(remind.sendreminder, slack_client)



def _reminders():
    """
    Loop to check the pending remainders 
    """
    while True:
        time.sleep(55)
        schedule.run_pending()

  
#getting bot info
response = slack_client.api_call("auth.test")


botid = response['user_id']




#interactions HTTP POST Route
@app.route("/slack/message_actions", methods=["POST"])
def _message_actions():
    """
    /slack/message_actions end point to receive HTTP POST Requests from Slack
    
    After Analysing the type of payload received whether a button click,
    dialogue,
    interactive message,
    dialogue submission repective response will be sent back to
    the user provoked the action
    """
    
    message_action = json.loads(request.form["payload"])
    
    
                              
    user_id = message_action["user"]["id"]
    channel_id = message_action['channel']['id']
    
    if message_action["type"] == "interactive_message":
        
        # Add the message_ts to the user's order info
        for actions in message_action['actions']:
            if actions['name']=="workform":
     
        # Show the ordering dialog to the user
                slack_client.api_call(
                    "chat.postMessage",
                    channel= channel_id,
                    icon_url=icon,
                    text= f"Hey <@{user_id}> Let's Start",
                    attachments=[]
                )
                slack_client.api_call(
                        "chat.postMessage",
                        channel= channel_id,
                        text =chainmessages[0],
                        icon_url=icon,
                        attachments=[]
                
                        )
                

        

       
    elif message_action["type"]=="block_actions":
        action = message_action.get('actions')
        
        actiontype = action[0]['type']

        if actiontype == 'channels_select':
            channel = action[0]['selected_channel']
            
            
        
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
                        text ="",
                        icon_url=icon,
                        attachments=[{
                    "text": val,
                    "color": "#3AA3E3",
                    "attachment_type": "default",
                    
                        }]
                        )
                if value.startswith('timer'):
                    del_id= value[5:]
                    val = remind.deletereminder(del_id)
                    slack_client.api_call(
                        "chat.postMessage",
                        channel= channel_id,
                        text ="",
                        icon_url=icon,
                        attachments=[{
                    "text": val,
                    "color": "#3AA3E3",
                    "attachment_type": "default",
                    
                        }]
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
                blocks.divider(slack_client,channel_id)
            if option == "resources":
                
                resourcemodule.showresources(slack_client, channel_id)
                blocks.divider(slack_client,channel_id)
            if option == 'report':
                
                slack_client.api_call(
                    "chat.postMessage",
                    channel= channel_id,
                    icon_url=icon,
                    text= f":thumbsup: <@{user_id}> Please let us \
know your progress",
                    attachments=[]
                )
                slack_client.api_call(
                    "chat.postMessage",
                    channel= channel_id,
                    icon_url=icon,
                    text= chainmessages[0],
                    attachments=[]
                )
                
                

            if option == 'joke':
                
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
                blocks.divider(slack_client,channel_id)
            if option == 'show':
                
                progress.report(user_id, channel_id, slack_client)
                blocks.divider(slack_client,channel_id)
            return make_response("", 200)

            
        
    elif message_action["type"] == "dialog_submission":
        
        formdata = message_action['submission']
  
        callbackid= message_action['callback_id']
        
        if callbackid.startswith('updateresource'):
            update_id = callbackid[14:]
            resourcemodule.update(  update_id,
                                    formdata['resource'],
                                    formdata['link'] 
                                )
            val = 'Under Construction'
        elif callbackid.startswith('resourceadd'):
            formdata = message_action['submission']
            val = resourcemodule.insert(
                                        formdata['resource'],
                                        formdata['link'],
                                        user_id
                                        )
        
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
    The payload received will be sent to anotherfunction by a different thread,
    then HTTP 200 Reponse will be sent back to the slack
    """
    global preveventid
     
    #threading a new process to handle the messages
    Thread(target=_handling_message,args=(event_data,),daemon=True).start()
   
    #returning the post request with HTTP 200
    return make_response("", 200)
        
def quickactions(channel):
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
                                        "text": "What do you want?"
                                    },
                                    "accessory": {
                                        "type": "static_select",
                                        "placeholder": {
                                            "type": "plain_text",
                                            "text": "Quick actions",
                                            "emoji": True
                                        },
                                        "options": [
                                            {
                                                "text": {
                                                    "type": "plain_text",
                                                    "text": "Report",
                                                    "emoji": True
                                                },
                                                "value": "report"
                                            },
                                            {
                                                "text": {
                                                    "type": "plain_text",
                                                    "text": "Resources",
                                                    "emoji": True
                                                },
                                                "value": "resources"
                                            },
                                            {
                                                "text": {
                                                    "type": "plain_text",
                                                    "text": "Request a dayoff",
                                                    "emoji": True
                                                },
                                                "value": "dayoff"
                                            },
                                            {
                                                "text": {
                                                    "type": "plain_text",
                                                    "text": "Your day reports",
                                                    "emoji": True
                                                },
                                                "value": "show"
                                            },
                                            {
                                                "text": {
                                                    "type": "plain_text",
                                                    "text": "joke",
                                                    "emoji": True
                                                },
                                                "value": "joke"
                                            }
                                        ]
                                    }
                                }
                            ])

                            

def verification(token):
    if token != os.getenv('SLACK_VERIFICATION_TOKEN'):
        print('error')
        return True
    else:
        return False
    
def _handling_message(event_data):
    """
    Handling messages according to the command/message received 
    The event_data arguement is the payload for the message event,
    according to the message
     recieved respective action will be performed
    """
    if verification(event_data['token']):
        return make_response("", 200)
        
    
    global prevtext
    data = event_data["event"]
    channel_id = data["channel"]
    
    
    
    if data.get("subtype") is None and data.get("user") != botid:
        user_id = data['user']
        if data['text']=='stop':
            prevtext =""
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
                            
                            progress.insert2(user_id, usersdata[user_id],0)
                            
                            val =""
                            for response in usersdata[user_id]:
                                val = val+  "*"+response+"*" +"\n \
"+ usersdata[user_id][response]+"\n"
                                
                                
                                slack_client.api_call(
                                "chat.postMessage",
                                                channel=channel_id,
                                                text= "",
                                                icon_url=icon,
                                                
                                                attachments=[{
                                                "text": response +"\n "+
                                                usersdata[user_id][response] ,
                                                
                                                "color": "#3AA3E3",
                                                "attachment_type": "default",
                                                
                                                }]
                                            )
                                
                            
                            
                            channel = os.getenv("channel")
                            
                            slack_client.api_call(
                                "chat.postMessage",
                                channel= channel,
                                text="hj",

                            )
                            text=f":bell: <@{user_id}> has submitted a report!"
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
                                                            "text": text
                                                            }
                                                    },
                                                    {
                                                    "type": "section",
                                                    "text": {
                                                            "type": "mrkdwn",
                                                            "text": val
                                                            }
                                                    }]
                                            )
                            
                                                
                            #channels = adminactions.getchannel()
                            
                            
                            
                            
    try:  
        prevtext = data['text']
    except:
        print("")
   
    if data.get("subtype") is None and data.get("user") != botid:
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
           
        if message in commands or data['text'].startswith("register "):
           
            
           
            
            
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
                #code = message[9:]
                #val = register.register(code, user_id, channel_id)
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
                                "text": "Great to see you here! \
                                      You're successfully registered "
                            }
                        },
                        {
                            "type": "section",
                            "text": {
                                "type": "mrkdwn",
                                "text": "• Don't forget to SyncUp your daily \
                                    progress \n • Go through all of the \
                                    resources \n Type `Help` to know me better"
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
               
                val = f"Welcome <@{user_id}>, I am your Horizon Zbot to help \
                you in managing your progress. \n Kindly Register with your \
                Unique slackid to get started \n Enter 'register <unique id>' \
                \n 1. Use commands like 'today','next' to save your todays and \
                tomorrows work data \n 2. Type 'show' to display your todays \
                and tomorrows plans \n 3.Type 'Resources' to know about all \
                the resources that we are in "                
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
                                        "text": "Hey there 👋 I'm Your "\
+botname+" . I'm here to help you create and manage tasks in Slack" 

                                            }
                                    },
                                
                                {
                                    "type": "section",
                                    "text": {
                                        "type": "mrkdwn",
                                        "text": "*1️⃣ `Submit` command*. Type \
`submit` To submit your today's report"
                                    }
                                },
                                {
                                    "type": "section",
                                    "text": {
                                        "type": "mrkdwn",
                                        "text": "*2️⃣ `Show` command*. Type \
`Show` command to display your today"
                                    }
                                },
                                {
                                    "type": "section",
                                    "text": {
                                        "type": "mrkdwn",
                                        "text": "*3️⃣ `Resources` command*. \
Type `resources` to display the resources of the "+Companyname\
+" that you will be working on"
                                    }
                                },
                                {
                                    "type": "section",
                                    "text": {
                                        "type": "mrkdwn",
                                        "text": "*4️⃣ `set` and `unset` \
commands*. To let the "+ botname+" know when should it remind you \n Use \
`set 18:30` to set the reminder and `unset` to edit. "                                    
}
                                },
                                {
                                    "type": "section",
                                    "text": {
                                        "type": "mrkdwn",
                                        "text": "5️⃣ Zbot is really friendly, \
type `joke`, zbot will send a funny joke to you. More features are on the way"
                                    }
                                }
                            ] )             
                quickactions(channel_id)
        
        elif dat.startswith("today") or dat.startswith("next") or  \
            dat.startswith("show") or dat.startswith("register ") or  \
            dat.startswith("resource add") or dat.startswith("resources") or \
            dat.startswith("resource delete ") or dat.startswith("submit") or \
            dat.startswith("remind ") or dat.startswith("set") or\
            dat.startswith("unset")    :
            """
            
            if user_id not in studentslist:
                    
                val ="Sorry! Please register as a student to use all of the bot\
                features.\n Type 'register <unique id>' to register. \n Type \
                    Help to know more"
                slack_client.api_call(
            "chat.postMessage",
                        channel=channel_id,
                        text=val,
                        icon_url=icon,
                        
                        )
            """
            if dat =="submit":
                user = data['user']
                channel = data['channel']
                slack_client.api_call(
            "chat.postMessage",
                    channel=channel_id,
                    text=f":thumbsup: <@{user}> Please let us \
know your progress",
                    icon_url=icon,
                        )
                slack_client.api_call(
            "chat.postMessage",
                    channel=channel_id,
                    text="What have you done today?",
                    icon_url=icon,
                        )
                
                

                
        
        
            
            
                
            
                
            elif dat.startswith("show"):
                #colors = ['#EBB713', '#F91C3E', 
                # '#16A085', '#212F3D', '#F1C40F']
                user = data['user']
                progress.report(user, channel_id, slack_client)
                    
                           
                       
                
            
                
        
            elif dat.startswith("resource add"):
                
                res="add"
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
                
                resourcemodule.showresources(slack_client, channel_id)
            
            
            elif dat.startswith("set"):

                
                time=dat.split()[1] 
                

                hour = time[0]
                minute = time[2:4]
                
                if len(time)==5:
                    hour = time[0:2]
                    minute = time[3:5]
                
                
                
               
                try:
                    hour = int(hour)
                    minute = int(minute)
                    if hour!=0 and hour <24 and minute <=60:
                        timer = str(hour)+":"+str(minute)

                        val = remind.setreminder(user_id, timer)
                    else:  
                        val = "Please set valid time format like 'set 20:30'"
                        return
                    
                    
                    
                except:
                    val="Please set time in 24Hours Format. Like 'set 20:30'"
                
                

                slack_client.api_call(
                        "chat.postMessage",
                        text = val,
                        icon_url = icon,
                        channel = channel_id

                )
            elif dat.startswith("unset"):
                timers = remind.unset(user_id)
                print("w")
                order = 0
                if timers =="":
                    slack_client.api_call(
                            "chat.postMessage",
                                channel=channel_id,
                                text="You haven't set a reminder yet! `set \
19:30` to set one",
                                icon_url=icon,
                        )

                for timer in timers:
                    order = order +1       
                                    
                    slack_client.api_call(
                            "chat.postMessage",
                                channel=channel_id,
                                text=str(order)+". "+ timer[0],
                                icon_url=icon,
                        )
                    slack_client.api_call(
                            "chat.postMessage",
                            channel=channel_id,
                            text="",
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
                                            "value": "timer"+str(timer[1])
                                        },
                                        {
                                            "type": "button",
                                            "text": {
                                                "type": "plain_text",
                                                "emoji": True,
                                                "text": "Delete"
                                            },
                                            "style": "danger",
                                            "value": "timer"+str(timer[1])
                                        }
                                    ]
                                    }
                                    ]
                            
                            )



                    
                    
                    

                    




                
                
                
                            
                   
            
    
    

                
            
          
     

if __name__ == "__main__":
    """
    This is the main function
    We are running the reminders() in a different thread to have both actions \
         performed independently
    
    """
    port = int(os.getenv("local_port"))
    
    host = os.getenv("local_host")
    Thread(target=_reminders,daemon=True).start()
  
    app.run(host=host, port=int(port), ssl_context=context)
