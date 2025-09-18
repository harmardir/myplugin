from django.urls import path
from . import views

app_name = "myplugin"

urlpatterns = [
    path("unit/<path:usage_key_str>/", views.render_unit, name="render_unit"),
    path("unit/<path:usage_key_str>/json/", views.render_unit_json, name="render_unit_json"),
]
