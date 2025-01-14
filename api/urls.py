"""project URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
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
from django.conf import settings
from django.contrib import admin
from django.urls import include, path, re_path
from django.http import HttpResponse

from .views import main_spa

from django.contrib.auth import views as auth_views
from . import views
from django.views.generic import TemplateView


urlpatterns = [
    path('', views.main_spa, name='home'),
    path('user/login/', views.login_view, name='login'),
    path('user/logout/', views.logout_view, name='logout'),
    path('user/signup/', views.signup_view, name='signup'),
    path('api/profile/', views.profile_api, name='profile_api'),
    path('api/password/', views.password_change, name='password_change'),
    path('api/hobbies/', views.hobby_api, name='hobby_api'),
    path('api/similar-users/', views.similar_users_view, name='similar_users'),
<<<<<<< HEAD
    path('api/csrf-token/', views.get_csrf_token, name='get-csrf-token'),
=======
    
    re_path(
        r"^(?!user|api|admin).*$",
        TemplateView.as_view(template_name="api/spa/index.html"),
        name="spa",
    ),
>>>>>>> fea7924fd3e378ae6e410507d5d038ae358a8e6b
]
