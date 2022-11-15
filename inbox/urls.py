from django.urls import path, include
from . import views

urlpatterns = [
    #path('', AccountViews.member_dashboard, name='member_dashboard'),
    # path('inbox/sent_messages/', views.sent_message, name='sent_message'),
    # path('inbox/sent_message/', views.a_sent_message, name='a_sent_message'),
    path('inbox/', views.inbox, name='inbox'),
    path('a_inbox/', views.a_inbox, name='a_inbox'),
    path('inbox/<username>/', views.Directs, name='directs'),
    path('a_inbox/<username>/', views.a_Directs, name='a_directs'),
     path('send/', views.send_direct, name='send_direct'),
    path('a_send/', views.a_send_direct, name='a_send_direct'),
    path('new_message/', views.user_search, name='user_search'),
    path('a_new_message/', views.a_user_search, name='a_user_search'),
    path('new_message/<username>', views.new_message, name='new_message'),
    path('a_new_message/<username>', views.a_new_message, name='a_new_message'),
]
