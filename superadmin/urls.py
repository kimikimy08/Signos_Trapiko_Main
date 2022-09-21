from django.urls import path, include
from . import views
from accounts import views as AccountViews

urlpatterns = [
    path('', AccountViews.superadmin_dashboard, name='superadmin'),
    path('profiles', views.super_profile, name='super_profile'),
    #path('profiles/edit_profile/', views.sa_profile_edit, name='sa_profile_edit'),
    
    #path('userReports/', views.sa_userReport, name='sa_userReport'),
    #path('userReports/pending/', views.sa_userReport_pending, name='sa_userReport_pending'),
    #path('userReports/approved/', views.sa_userReport_approved, name='sa_userReport_approved'),
    #path('userReports/rejected/', views.sa_userReport_rejected, name='sa_userReport_rejected'),
    
    path('userAccounts', views.super_user_account, name='super_user_account'),
    path('userAccounts/member', views.super_user_account_member, name='super_user_account_member'),
    path('userAccounts/admin', views.super_user_account_admin, name='super_user_account_admin'),
    path('userAccounts/superadmin', views.super_user_account_superadmin, name='super_user_account_superadmin'),
    path('userAccounts/add/', views.super_user_account_add, name='super_user_account_add'),
    path('userAccounts/delete/<user_id>', views.super_user_account_delete, name="super_user_account_delete"),
    #path('userAccounts/viewUser/', views.sa_userAccount_addUser, name='sa_userAccount_addUser'),
    #path('userAccounts/edit_user/<user_id>', views.edit_user, name='edit_user'),
    
]