from django.urls import path, include
from . import views

urlpatterns = [
    #path('', AccountViews.member_dashboard, name='member_dashboard'),
    path('inbox/sent_message/', views.sent_message, name='sent_message'),
]
