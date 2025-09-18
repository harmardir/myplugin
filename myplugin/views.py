from openedx.core.djangoapps.plugin_api.views import render_to_mako

def hello_world(request):
    context = {"message": "Hello from MyPlugin (HTML)!"}
    return render_to_mako("myplugin/hello.html", context)
