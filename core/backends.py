from django.core.exceptions import ValidationError
from django.utils.html import escape


import json
import requests

def sms_send_textit(to, message):

    post_url = "https://api.textit.in/api/v1/sms.json"

    params = {
            'phone': to,
            'text': escape(message)
        }
    
    if len(params["text"]) >= 480:
        raise ValidationError("The text can not be longer than 480 chars.")
    
    data = json.dumps(params)
    
    from django.conf import settings
    api_token = getattr(settings, "TEXTIT_AUT")

    headers = {
        'accept': 'application/json',
        'content-type': 'application/json',
        'Authorization': 'Token ' + str(api_token),
    }
    
    response = requests.post(post_url,
                             data=data,
                             headers=headers)
    
    return response.json()



import telerivet

def sms_send_telerivet(to, message):
    from django.conf import settings

    # from https://telerivet.com/dashboard/api
    API_KEY = getattr(settings, "API_KEY") 
    PROJECT_ID = getattr(settings, "PROJECT_ID")

    if len(message) >= 480:
        raise ValidationError("The text can not be longer than 480 chars.")

    
    tr = telerivet.API(API_KEY)
    
    project = tr.initProjectById(PROJECT_ID)
    
    sent_msg = project.sendMessage(
        to_number = to,
        content = message
    )
    
    return sent_msg

def sms_send_test(to, message):

    params = {
            'phone': to,
            'text': escape(message)
            }
        
    return json.dumps(params)

