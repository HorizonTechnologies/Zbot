icon = 'https://img.icons8.com/emoji/96/000000/penguin--v2.png'
def divider(slack_client,channel):
    slack_client.api_call(
                        "chat.postMessage",
                        channel=channel,
                        text= "",
                        icon_url=icon,
                                                
                        blocks= [
                                {
                                    "type": "divider"
                                    
                                }
                                ])
def reminder(slack_client, user):
    slack_client.api_call(
                  "chat.postMessage",
                  as_user=True,
                  channel= user,
                  icon_url=icon,
                  text=f"Hey <@{user}>!, :wave: Fill in what you've done today",
                  attachments=[{
                    "text": "",
                    "callback_id":  "workform",
                    "color": "#3AA3E3",
                    "attachment_type": "default",
                    "actions": [{
                      "name": "workform",
                      "text": "Submit Today\'s report",
                      "type": "button",
                      "value": "Work_data"
                    }]
                  }]
                )
    slack_client.api_call(
              "chat.postMessage",
              as_user=True,
              channel= user,
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