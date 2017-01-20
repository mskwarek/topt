# @file web/views.py
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

# all modules should be imported here

import fiberMode.views


# for test working server
def index(request):
    return render_to_response('tresc.html', {}, RequestContext(request))


def ajax(request, module, function):
    """dispatch ajax requests"""
    try:   
        #print x, str(function), globals()[str(module)], request.GET
        fun = getattr(getattr(globals()[str(module)], 'views'), str(function))
        x = fun(request.GET)
        data = json.dumps(x)
        return django.http.StreamingHttpResponse(data, 'application/json')
    except Exception as e:
        return django.http.HttpResponseNotFound("myapp ajax error: " + str(traceback.format_exc()) )
    except:
        return django.http.HttpResponseNotFound("myapp ajax system error " )
