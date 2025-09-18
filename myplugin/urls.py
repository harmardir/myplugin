from django.urls import path
from . import views

app_name = "myplugin"

urlpatterns = [
    path("units/", views.units_list, name="units_list"),
    path("unit/<path:usage_key_str>/", views.render_unit, name="render_unit"),
]
