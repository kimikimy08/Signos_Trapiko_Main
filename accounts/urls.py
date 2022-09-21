from django.urls import path, include
from . import views

urlpatterns = [
    path('registration', views.registration, name='registration'),
    path('login', views.login, name='login'),
    path('logout', views.logout, name='logout'),
    path('myAccount', views.myAccount, name='myAccount'),
    path('activate/<uidb64>/<token>', views.activate, name='activate'),
    
    path('dashboard/', views.memberDashboard, name='memberDashboard'),
    path('adashboard/', views.adminDashboard, name='adminDashboard'),
    path('sdashboard/', views.superDashboard, name='superDashboard'),
]