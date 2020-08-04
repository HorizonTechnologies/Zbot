
def reminder(n,client):
    channels = register.channelslist()
    
    if n=='0':
        for channel in channels:
            client.api_call(
                      "chat.postMessage",
                  as_user=True,
                  channel=channel,
                  text="Hey!, :wave: Fill in what you've done today",
                  blocks= [
    {
        "type": "section",
        "name":"tharun",
        "text": {
            "type": "mrkdwn",
            "text": "Other quick actions"
        },
        "accessory": {
            "type": "static_select",
            "placeholder": {
                "type": "plain_text",
                "emoji": True,
                "text": "Manage Here"
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
            client.api_call(
                  "chat.postMessage",
                  as_user=True,
                  channel="D013ACB3V1A",
                  text="Hey TEST!, :wave: Fill in what you've done today",
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
              channel="D013ACB3V1A",
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
                        "value": "value-0"
                    },
                    {
                        "text": {
                            "type": "plain_text",
                            "emoji": True,
                            "text": "Continuing Yesterday's work"
                        },
                        "value": "value-1"
                    }
                ]
            }
        }
    ]
            )

            
            
    if n=='1':
        for channel in channels:
        
            client.api_call(
                  "chat.postMessage",
                  as_user=True,
                  channel=channel,
                  text="Hey TEST!, :wave: Fill in what you've done today",
                  attachments=[{
                    "text": "",
                    "callback_id": user_id + "workform",
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
    
    
    
