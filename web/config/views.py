## @file web/views.py
#  @brief main server interface to client

"""
main interface to server
"""

import django.http
import json
import traceback

from django.shortcuts import render_to_response
from django.template import RequestContext
from django.http import HttpResponse

#all modules should be imported here

import fiberMode.views

## for test working server
def index(request):
    """for test working server"""
    #return django.http.HttpResponse("MyApp server" )
    return render_to_response('tresc.html', {}, context_instance=RequestContext(request))

def ajax(request, module, function):
    """dispatch ajax requests"""
    try:   
        #print x, str(function), globals()[str(module)], request.GET
        fun = getattr(getattr(globals()[str(module)], 'views'), str(function))
        x = fun(request.GET)
        data = json.dumps(x)
        return django.http.StreamingHttpResponse(data, content_type='application/json')
    except Exception as e:
        return django.http.HttpResponseNotFound("myapp ajax error: " + str(traceback.format_exc()) )
    except:
        return django.http.HttpResponseNotFound("myapp ajax system error " )
