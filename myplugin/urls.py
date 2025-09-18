from django.urls import path
from . import views

urlpatterns = [
    path("unit/<path:usage_key_str>/", views.render_unit, name="render_unit"),
]
