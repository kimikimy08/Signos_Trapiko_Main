from django.urls import path, include
from . import views

urlpatterns = [
    #path('', AccountViews.member_dashboard, name='member_dashboard'),
    path('inbox/sent_messages/', views.sent_message, name='sent_message'),
    path('inbox/sent_message/', views.a_sent_message, name='a_sent_message'),
]
