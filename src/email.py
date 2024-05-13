import os
from loguru import logger
from mailjet_rest import Client

def sendEmail(alerts):    
    api_key = os.environ['MJ_APIKEY_PUBLIC']
    api_secret = os.environ['MJ_APIKEY_PRIVATE']
    mailjet = Client(auth=(api_key, api_secret), version='v3.1')
    data = {
    'Messages': [
        {
        "From": {
            "Email": "dinukafindmyphone@gmail.com",
            "Name": "SwinTIP Flood Monitoring System"
        },
        "To": [
            {
            "Email": "",
            "Name": ""
            }
        ],
        "Subject": "SwinTIP Flood Alert!",
        "TextPart": "New flood alert!",
        "HTMLPart": "Hello!<br/><br/>Please be aware of the following flood alerts.<br/><br/>"+alerts
        }
    ]
    }
    result = mailjet.send.create(data=data)
    logger.info(result.json())