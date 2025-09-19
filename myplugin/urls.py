from django.urls import path
from .views import UnitListView, UnitContentView

urlpatterns = [
    path('course/<str:course_id>/units/', UnitListView.as_view(), name="unit-list"),
    path('unit/<str:unit_id>/content/', UnitContentView.as_view(), name="unit-content"),
]