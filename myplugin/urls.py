# myplugin/urls.py
from django.urls import path
from . import views

app_name = "myplugin"


urlpatterns = [
    path("units/", views.unit_grid, name="unit_grid"),
    path("test/", views.test_template, name="test_template"), 
    path("", views.hello_world, name="hello"), # new test URL
]



