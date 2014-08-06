formhub-sms-webhook
===================

A webhook for formhub that quest sms to be sent if certain parameters in a form are set. This is quite a simple
little project. Basically there is a /submit URL that takes the JSON from formhub. It then uses a/many 
eval method(s) that then can do multiple things. In this example it sends a text message after a specified amount 
of time. But in theory it can pretty much do everything python/django can do. But the delay part is sort of the 
special feature. You need to call this manually, maybe through a cron job:

```
./manage.py send_messages
```

eHealth Africa Formhub can be found under : https://github.com/eHealthAfrica/formhub

