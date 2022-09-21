from django.urls import path, include
from . import views
from accounts import views as AccountViews

urlpatterns = [
    #path('', AccountViews.superDashboard, name='superadministration'),
    path('profiles/', views.super_profile, name='super_profile'),
    #path('profiles/edit_profile/', views.sa_profile_edit, name='sa_profile_edit'),
    
    #path('userReports/', views.sa_userReport, name='sa_userReport'),
    #path('userReports/pending/', views.sa_userReport_pending, name='sa_userReport_pending'),
    #path('userReports/approved/', views.sa_userReport_approved, name='sa_userReport_approved'),
    #path('userReports/rejected/', views.sa_userReport_rejected, name='sa_userReport_rejected'),
    
    #path('userAccounts/', views.sa_userAccount, name='sa_userAccount'),
    #path('userAccounts/member/', views.sa_userAccount_member, name='sa_userAccount_member'),
    #path('userAccounts/admin/', views.sa_userAccount_admin, name='sa_userAccount_admin'),
    #path('userAccounts/superadmin/', views.sa_userAccount_superadmin, name='sa_userAccount_superadmin'),
    #path('userAccounts/addUser/', views.sa_userAccount_addUser, name='sa_userAccount_addUser'),
    #path('userAccounts/delete_user/<user_id>', views.delete_user, name="delete_user"),
    #path('userAccounts/viewUser/', views.sa_userAccount_addUser, name='sa_userAccount_addUser'),
    #path('userAccounts/edit_user/<user_id>', views.edit_user, name='edit_user'),
    
]