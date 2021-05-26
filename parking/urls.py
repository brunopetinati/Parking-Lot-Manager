from django.urls import path
from .views import ParkingView

urlpatterns = [
    path('levels/', ParkingView.as_view()),
]