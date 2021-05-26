from django.urls import path
from .views import AccountCreateView, LoginView

urlpatterns = [
    path('accounts/', AccountCreateView.as_view()),
    path('login/', LoginView.as_view())
]