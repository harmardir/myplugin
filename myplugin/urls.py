from django.urls import path
from . import views

app_name = "myplugin"

urlpatterns = [
    path("units/", views.list_units, name="units"),
]
