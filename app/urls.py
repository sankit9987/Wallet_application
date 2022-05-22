from django.urls import path
from . import views
urlpatterns = [
    path('', views.home,name="home"),
    path('sign-up', views.User_sign_up,name="register"),
    path('login', views.User_login,name="login"),
    path('logout', views.user_logout,name="logout"),
]
