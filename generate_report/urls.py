from django.contrib import admin  
from django.urls import path  
from generate_report import views  
 
urlpatterns = [  
    path('generate_report', views.generate_report, name='generate_report'),
    path('generate_report/export_users_xls', views.export_users_xls, name='export_users_xls'),
    path('generate_report/export_accidentcausation_xls', views.export_accidentcausation_xls, name='export_accidentcausation_xls'),
]  