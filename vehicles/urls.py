from django.urls import path
from .views import VehicleEntryView, VehicleExitView

urlpatterns = [
    path('vehicles/', VehicleEntryView.as_view()),
    path('vehicles/<int:vehicle_id>', VehicleExitView.as_view())
]