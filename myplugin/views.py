'''
from django.http import JsonResponse

def hello_world(request):
    return JsonResponse({"message": "Hello from MyPlugin!"})
'''

from django.shortcuts import render

def hello_world(request):
    context = {"message": "Hello from MyPlugin (HTML)!"}
    return render(request, "myplugin/hello.html", context)