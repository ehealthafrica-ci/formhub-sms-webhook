from django.test import TestCase
from django.core.urlresolvers import reverse
from django.conf import settings
from core.models import Messages
from django.utils import timezone
from core.backends import sms_send_test
import time
from django.core.management import call_command
import json
import datetime
# Create your tests here.


test_post = '{"_id": 115628, "_attachments": [], "name": "testing", "_submission_time": "2014-08-05T17:14:25", "age": "21", "_uuid": "0efee5c4-6bcb-4f92-8abd-8f631eb0270a", "_bamboo_dataset_id": "", "_tags": [], "_geolocation": [null, null], "_xform_id_string": "tutorial_tutorial", "_userform_id": "a_tutorial_tutorial", "_status": "submitted_via_web", "meta/instanceID": "uuid:0efee5c4-6bcb-4f92-8abd-8f631eb0270a", "has_children": "0", "formhub/uuid": "17d3747ce512463988f596cd847d0fcf"}'

test_number = "+123"
test_text = "Someone with the age 21 was submitted"

def eval_json(json, request):
    
    #If the age is 21 send a message
    if "age" in json.keys() and json["age"] == "21":
        
        message = Messages()
        
        message.number = test_number
        message.message = test_text
        message.when_to_send = timezone.now()
        message.hook_ip = request.META.get('REMOTE_ADDR')
        message.hook_json_message = json
        message.save()
        
        return message


def eval_json_set_send_future(json, request):
    
    #If the age is 21 send a message
    if "age" in json.keys() and json["age"] == "21":
        
        message = Messages()
        
        message.number = test_number
        message.message = test_text
        message.when_to_send = timezone.now().replace(year=datetime.MAXYEAR)
        message.hook_ip = request.META.get('REMOTE_ADDR')
        message.hook_json_message = json
        message.save()
        
        return message


class TestHTTPServer(TestCase):
    
    def _delete_post_key(self):
        #Make sure we have security disabled
        if getattr(settings, "POST_KEY", False):
            del settings.POST_KEY

    
    def test_get_will_fail(self):
        """
        We should not be able to use get on the /submit url
        """
        response = self.client.get(reverse('submit'))
        self.assertEqual(response.status_code, 405)
        
    def test_post_without_api_key(self):
        """
        If we have a POST_KEY set it should require it
        """

        settings.POST_KEY = "abc"

        # No post key        
        response = self.client.post(reverse('submit'))
        self.assertEqual(response.status_code, 400) # 400 Bad Request
        
        # Bad post key
        response = self.client.post("%s?key=something" % reverse('submit'))
        self.assertEqual(response.status_code, 403) # 403 Forbidden

    def test_bad_post_keys(self):
        """
        We should only submit one JSON
        """
        self._delete_post_key()

        response = self.client.post(reverse('submit'), {"A":"A", "B":"B"})
        self.assertEqual(response.status_code, 400) # 400 Bad Request


    def test_bad_json(self):
        """
        Json has to be valid
        """
        
        self._delete_post_key()
            
        response = self.client.post(reverse('submit'), {"Something that is not JSON":""})
        self.assertEqual(response.status_code, 400) # 400 Bad Request

        
    def test_message_creation(self):
        """
        If a post is correct a message should be created
        """
        
        self._delete_post_key()
            
        # Set it to our eval_json, so people can modify the one in the code
        settings.EVAL_METHOD = eval_json

        self.assertEqual(Messages.objects.all().count(), 0) 

        response = self.client.post(reverse('submit'), {test_post:""})
        
        # We should have one more message
        self.assertEqual(Messages.objects.all().count(), 1) 


        #Check the message values
        
        mes = Messages.objects.all().first()
        
        self.assertEqual(mes.number, test_number)
        self.assertEqual(mes.message, test_text)

        #The return code should be ok
        self.assertEqual(response.status_code, 200)
        
        #The content should be the message that will be sent when
        self.assertEqual(response.content, unicode(Messages.objects.all()[0]))
        
    def test_message_creation_with_list(self):
        """
        If a post is correct a message should be created
        """
        
        self._delete_post_key()
            
        # Set it to our eval_json, so people can modify the one in the code
        settings.EVAL_METHOD = [eval_json, eval_json] 

        self.assertEqual(Messages.objects.all().count(), 0) 

        response = self.client.post(reverse('submit'), {test_post:""})
        
        # We should have one more message
        self.assertEqual(Messages.objects.all().count(), 2) 
        
        #The return code should be ok
        self.assertEqual(response.status_code, 200)

        #The content should be the message that will be sent when
        ret_list = []
        for m in Messages.objects.all():
            ret_list.append(unicode(m))
        
        self.assertEqual(response.content, unicode(ret_list))
        
        
    def test_message_sender(self):

        self._delete_post_key()

        # Set it to our eval_json, so people can modify the one in the code
        settings.EVAL_METHOD = eval_json

        #Set the proper send method
        settings.SMS_BACKEND = sms_send_test

        #Create a new post
        response = self.client.post(reverse('submit'), {test_post:""})

        #So it is now +1
        time.sleep(1)
        
        call_command('send_messages')
        
        self.assertEqual(Messages.objects.all().count(), 1) 
        
        mes = Messages.objects.all().first()

        #Check that the massage has been sent
        self.assertIsNotNone(mes.sent_when)
        
        #Check that the return is correct
        self.assertEqual(mes.sent_return_message, json.dumps({'phone': test_number, 'text': test_text}))
        
        #Check that the times are correct
        self.assertGreater(mes.sent_when, mes.when_to_send)
        
    def test_message_sender_future_nothing_sent(self):

        self._delete_post_key()

        # Set it to our eval_json, so people can modify the one in the code
        settings.EVAL_METHOD = eval_json_set_send_future

        #Set the proper send method
        settings.SMS_BACKEND = sms_send_test

        #Create a new post
        response = self.client.post(reverse('submit'), {test_post:""})

        
        call_command('send_messages')
        
        self.assertEqual(Messages.objects.all().count(), 1) 
        
        mes = Messages.objects.all().first()

        #Check that the massage has been sent
        self.assertIsNone(mes.sent_when)
        
        #Check that the return is correct
        self.assertIsNone(mes.sent_return_message)
        




        
        
        
        