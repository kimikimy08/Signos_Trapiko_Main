from django.urls import path, include
from . import views

urlpatterns = [
    path('registration', views.registration, name='registration'),
    path('login', views.login, name='login'),
    path('logout', views.logout, name='logout'),
    path('myAccount', views.myAccount, name='myAccount'),
    path('activate/<uidb64>/<token>', views.activate, name='activate'),
    
    path('dashboard/', views.member_dashboard, name='member_dashboard'),
    path('adashboard/', views.admin_dashboard, name='admin_dashboard'),
    path('sdashboard/', views.superadmin_dashboard, name='superadmin_dashboard'),
]