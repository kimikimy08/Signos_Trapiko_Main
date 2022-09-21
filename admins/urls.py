from django.urls import path, include
from . import views
from accounts import views as AccountViews

urlpatterns = [
    #path('', AccountViews.admin_dashboard, name='admin_dashboard'),
    path('profile', views.admin_profile, name='admin_profile'),
    
    #path('userReport/', views.a_userReport, name='a_userReport'),
    #path('userReport/pending/', views.a_userReport_pending, name='a_userReport_pending'),
    #path('userReport/approved/', views.a_userReport_approved, name='a_userReport_approved'),
    #path('userReport/rejected/', views.a_userReport_rejected, name='a_userReport_rejected'),
    
    #path('userAccount/delete_users/<user_id>', views.a_deleteUser, name="a_deleteUser"),
    #path('userAccount/', views.a_userAccount, name='a_userAccount'),
    #path('userAccount/member/', views.a_userAccount_member, name='a_userAccount_member'),
    #path('userAccount/admin/', views.a_userAccount_admin, name='a_userAccount_admin'),
    #path('userAccount/superadmin/', views.a_userAccount_superadmin, name='a_userAccount_superadmin'),
    
]