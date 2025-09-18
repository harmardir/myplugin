from django.shortcuts import render_to_response
from django.template import RequestContext

def hello_world(request):
    context = {"message": "Hello from MyPlugin (HTML)!"}
    return render_to_response("myplugin/hello.html", context, context_instance=RequestContext(request))
