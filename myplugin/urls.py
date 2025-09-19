# myapp/urls.py
from django.urls import path
from . import views

urlpatterns = [
    path("units/", views.unit_grid, name="unit_grid"),
]
