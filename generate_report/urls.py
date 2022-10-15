from django.contrib import admin  
from django.urls import path  
from generate_report import views  
 
urlpatterns = [  
    path('generate_report', views.generate_report, name='generate_report'),
    path('generate_report/export_users_xls', views.export_users_xls, name='export_users_xls'),
    path('generate_report/export_accidentcausation_xls', views.export_accidentcausation_xls, name='export_accidentcausation_xls'),
    path('generate_report/export_classification_xls', views.export_classification_xls, name='export_classification_xls'),
     path('generate_report/export_collision_xls', views.export_collision_xls, name='export_collision_xls'),
]  