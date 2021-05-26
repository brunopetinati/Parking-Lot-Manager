from django.urls import path
from .views import PricingView

urlpatterns = [
    path('pricings/', PricingView.as_view()),
]