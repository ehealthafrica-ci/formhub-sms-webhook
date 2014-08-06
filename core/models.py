from django.db import models
from django.utils import timezone

from django.core.exceptions import SuspiciousOperation, ValidationError
from django.conf import settings
from core.backends import sms_send_telerivet

class Messages(models.Model):
    
    #Content
    ########
    
    #The number the message will be sent to
    number = models.CharField(max_length=100)
    
    #The message that will be sent
    message = models.CharField(max_length=450)
    
    #When the message should be sent
    when_to_send = models.DateTimeField()
    
    #Sending
    ########
    
    #When the message was sent
    sent_when = models.DateTimeField(null=True, blank=True)
    
    #Send status
    sent_return_message = models.TextField(null=True, blank=True)
    
    #Trigger
    ########
    
    #The Json that triggered the send
    hook_json_message = models.TextField()
    
    #The IP that sent us the json
    hook_ip = models.GenericIPAddressField()
    
    #When was this message recieved and created
    hook_recieved = models.DateTimeField(auto_now_add=True)
    
    
    def send(self):
        
        if self.when_to_send > timezone.now():
            raise SuspiciousOperation("You can not send a message before it is timed")
        
        if len(self.message) >= 480:
            raise ValidationError("The text can not be longer than 480 chars.")

        sms_backend = getattr(settings, "SMS_BACKEND", sms_send_telerivet)
        
        response = sms_backend(self.number, self.message)
 
        self.sent_return_message = response
        self.sent_when = timezone.now()
        self.save()
        

    def __unicode__(self):
        return unicode(self.number) + ", " + unicode(self.message) + \
            ", " + unicode(self.when_to_send)
            