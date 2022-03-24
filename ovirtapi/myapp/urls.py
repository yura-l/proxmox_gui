from django.conf.urls.static import static
from django.urls import path, include

from . import views
from .views import *

urlpatterns = [

    path('', views.index, name='index'),
    path('create/', views.get_createvm, name='get_createvm'),
    path("accounts/", include("django.contrib.auth.urls")),
    path('login/', views.loginPage, name='login'),
    path('logout/', views.logout_User, name='logout'),
    path('vm/<str:uuid>/', views.get_vm, name='get_vm'),
    path('template/', views.get_template_vm, name='get_template_vm'),
    # path('vnc/', views.vnc, name='vnc'),
    path('vm/<str:uuid>/delete/', views.delete_vm, name='delete_vm'),
    path('vm/<str:uuid>/stop/', views.stop_vm, name='stop_vm'),
    # # path('console/', views.get_console, name='get_console'),
    # # path("see_request/", views.see_request),
    # # path("user_info/", views.user_info,  name='user_info'),
    #
    # # path('', views.index, name='index'),
]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)