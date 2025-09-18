from django.urls import path
from . import views

app_name = "myplugin"

urlpatterns = [
    path("courses/", views.courses_and_units_view, name="courses"),
]
