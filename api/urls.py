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
from django.urls import include, path
from django.http import HttpResponse

from .views import main_spa

from django.contrib.auth import views as auth_views
from . import views


urlpatterns = [
    path('', views.main_spa, name='home'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('signup/', views.signup_view, name='signup'),
    path('api/profile/', views.profile_api, name='profile_api'),
    path('api/password/', views.password_change, name='password_change'),
    path('api/hobbies/', views.hobby_api, name='hobby_api'),
    path('api/users/similar_with_filters/', views.similar_users_with_filters_view, name='similar_users_with_filters'),
    path('api/friends_view/', views.friends_view, name='friends_view'),
    path('api/get_friend_requests/', views.get_friend_requests, name='get_friend_requests'),
    path('api/send_request/', views.send_request, name='send_request'),
    path('api/accept_request/', views.accept_request, name='accept_request'),
    path('api/reject_request/', views.reject_request, name='reject_request'),
    path('api/csrf-token/', views.get_csrf_token, name='get-csrf-token'),
    path('friends/', views.main_spa, name='friends'),
    path('otherusers/',views.main_spa, name = 'otherusers'),
    path('api/profile/add_hobby', views.add_hobby_to_profile, name='add_hobby_to_profile'),
]
