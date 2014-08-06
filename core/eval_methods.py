########################
# THIS IS AN EXAMPLE !!!
########################
#
# This is the eval method to check what to do. Please overwrite for your needs
# or set a method in settins.py with the same parameters
# 
from core.models import Messages
from django.utils import timezone

def eval_json(json, request):
    
    #If the age is 21 send a message
    if "age" in json.keys() and json["age"] == "21":
        
        message = Messages()
        
        message.number = "+234 818 629 5584"
        message.message = "Someone with the age 21 was submitted"
        message.when_to_send = timezone.now()
        message.hook_ip = request.META.get('REMOTE_ADDR')
        message.hook_json_message = json
        message.save()
        
        return message
    
    return