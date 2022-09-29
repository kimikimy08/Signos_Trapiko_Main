from django.urls import path, include
from . import views
from accounts import views as AccountViews

urlpatterns = [
    #path('', AccountViews.member_dashboard, name='member_dashboard'),
    path('profile/', views.member_profile, name='member_profile'),
    path('profiles/edit', views.member_profile_edit, name='member_profile_edit'),
]