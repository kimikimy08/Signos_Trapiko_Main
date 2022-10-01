from django.urls import path, include
from . import views
from accounts import views as AccountViews

urlpatterns = [
    path('userReport', views.user_report, name='user_report'),
    path('userReport/pending', views.user_report_pending, name='user_report_pending'),
    path('userReport/approved', views.user_report_approved, name='user_report_approved'),
    path('userReport/rejected', views.user_report_rejected, name='user_report_rejected'),
    
    path('userReports', views.user_reports, name='user_reports'),
    path('userReports/pending', views.user_reports_pending, name='user_reports_pending'),
    path('userReports/approved', views.user_reports_approved, name='user_reports_approved'),
    path('userReports/rejected', views.user_reports_rejected, name='user_reports_rejected'),
    
    path('myReport', views.my_report, name='my_report'),
    path('myReport/pending', views.my_report_pending, name='my_report_pending'),
    path('myReport/approved', views.my_report_approved, name='my_report_approved'),
    path('myReport/rejected', views.my_report_rejected, name='my_report_rejected'),
    path('myReport/add', views.my_report_add, name='my_report_add'),
    path('myReport/view/<int:id>', views.my_report_view, name='my_report_view'),
    path('myReport/edit/<int:id>', views.my_report_edit, name='my_report_edit'),
    path('myReport/delete/<int:id>', views.my_report_delete, name='my_report_delete'),
    
    path('incidentReport/general', views.incident_report_general, name='incident_report_general'),
    
    path('ajax/load-accident/', views.load_accident, name='ajax_load_accident'), # AJAX
    path('ajax/load-collision/', views.load_collision, name='ajax_load_collision'), # AJAX
]