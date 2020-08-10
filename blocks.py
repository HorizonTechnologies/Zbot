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