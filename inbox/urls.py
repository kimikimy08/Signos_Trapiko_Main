from django.urls import path, include
from . import views
from accounts import views as AccountViews
# from .views import GeneratePdf

urlpatterns = [
    #path('', AccountViews.member_dashboard, name='member_dashboard'),
    path('', views.notifications, name='notifications'),

]
