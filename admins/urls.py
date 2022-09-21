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
    
    path('userAccount/delete/<user_id>', views.admin_user_account_delete, name="admin_user_account_delete"),
    path('userAccount/', views.admin_user_account, name='admin_user_account'),
    path('userAccount/member/', views.admin_user_account_member, name='admin_user_account_member'),
    path('userAccount/admin/', views.admin_user_account_admin, name='admin_user_account_admin'),
    path('userAccount/superadmin/', views.admin_user_account_superadmin, name='admin_user_account_superadmin'),
    
]