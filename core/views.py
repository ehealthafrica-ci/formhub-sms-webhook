from django.http.response import HttpResponse, HttpResponseForbidden,\
    HttpResponseBadRequest
from django.views.decorators.http import require_GET, require_POST
from django.views.decorators.csrf import csrf_exempt
from django.conf import settings
import json
from core.eval_methods import eval_json


@require_GET
def home(request):  # @UnusedVariable
    return HttpResponse("Hello, world. This is the webhook root. Nothing much to see here.")


@require_POST
@csrf_exempt
def submit(request):
    
    # If a post_key is specified in the settings we use
    # it as a "security" measure
    post_key = getattr(settings, "POST_KEY", None)   
    
    if post_key:
        if "key" in request.GET:
            if request.GET["key"] != post_key:
                #The request has a key but it doesn't match
                return HttpResponseForbidden()
        else:
            #The post key is specified in the settings but not in the URL
            return HttpResponseBadRequest()


    #Because the post is not indexed we have to check the key
    if len(request.POST.keys()) != 1:
        return HttpResponseBadRequest()
    
    #Check if it really json
    try:
        json_object = json.loads(request.POST.keys()[0])
    except ValueError, e:
        #The json is not valid
        return HttpResponseBadRequest()

    eval_method = getattr(settings, "EVAL_METHOD", eval_json)   
    
    if isinstance(eval_method ,list):
        return_string_list = []
        for e in eval_method:
            return_string_list.append(unicode(e(json_object, request)))
            return_string = unicode(return_string_list)
    else:
        #call the eval method below
        return_string = unicode(eval_method(json_object, request))

    return HttpResponse(return_string)

