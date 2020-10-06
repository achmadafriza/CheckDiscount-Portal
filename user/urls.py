"""PortalAPI URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.urls import path, include
from django.contrib.auth import views as auth_views

from . import views
from .forms import LoginForm

app_name = 'user'

urlpatterns = [
    path('login/', auth_views.LoginView.as_view(template_name="user/login.html", form_class=LoginForm), name="login"),
    path('register/', views.register, name="register"),
    path('logout/', auth_views.LogoutView.as_view(template_name="user/logout.html"), name="logout"),
    path('redirect/', views.redirect_by_permission, name="redirect"),
    path('otp/', views.checkOTP, name='otp')
    # Need to implement forgot password, change password, change profile
]
