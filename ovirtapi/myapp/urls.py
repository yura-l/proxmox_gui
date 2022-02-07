from django.urls import path, include

from . import views
from .views import *

urlpatterns = [

    path('', views.index, name='index'),
    path("profile/", views.profile,  name='profile'),
    path("accounts/", include("django.contrib.auth.urls")),
    path('login/', views.loginPage, name='login'),
    path('logout/', views.logout_User, name='logout'),
    # # path('users<str:pk>/', views.get_userid, name='get_userid'),
    path('create/', views.get_createvm, name='get_createvm'),
    # path('vnc/', views.vnc, name='vnc'),
    # # path('delete/users<str:pk>/<str:vm>', views.delete_vm, name='delete_vm'),
    # # path('console/', views.get_console, name='get_console'),
    # # path("see_request/", views.see_request),
    # # path("user_info/", views.user_info,  name='user_info'),
    #
    # # path('', views.index, name='index'),
]
