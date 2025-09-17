from django.shortcuts import render

def hello_world(request):
    context = {"message": "Hello from MyPlugin (HTML)!"}
    return render(request, "myplugin/hello.html", context)