from django.urls import path
from .views import *
urlpatterns = [
    # path('', views.home,name="home"),
    path('sign-up', UserRegisterView.as_view()),
    path('login', LoginView.as_view()),
    path('home', BalanceView.as_view()),
]
