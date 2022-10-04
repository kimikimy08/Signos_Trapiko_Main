from django.urls import path, include
from . import views
from accounts import views as AccountViews
from .views_inc import FormView, CancelView
from .views import FORMS

urlpatterns = [
    path('userReport', views.user_report, name='user_report'),
    path('userReport/pending', views.user_report_pending, name='user_report_pending'),
    path('userReport/approved', views.user_report_approved, name='user_report_approved'),
    path('userReport/rejected', views.user_report_rejected, name='user_report_rejected'),
    
    path('userReports', views.user_reports, name='user_reports'),
    path('userReports/pending', views.user_reports_pending, name='user_reports_pending'),
    path('userReports/approved', views.user_reports_approved, name='user_reports_approved'),
    path('userReports/rejected', views.user_reports_rejected, name='user_reports_rejected'),
    path('userReports/delete/<int:id>', views.user_report_delete, name='user_report_delete'),
   
    
    path('myReport', views.my_report, name='my_report'),
    path('myReport/pending', views.my_report_pending, name='my_report_pending'),
    path('myReport/approved', views.my_report_approved, name='my_report_approved'),
    path('myReport/rejected', views.my_report_rejected, name='my_report_rejected'),
    path('myReport/add', views.my_report_add, name='my_report_add'),
    path('myReport/view/<int:id>', views.my_report_view, name='my_report_view'),
    path('myReport/edit/<int:id>', views.my_report_edit, name='my_report_edit'),
    path('myReport/delete/<int:id>', views.my_report_delete, name='my_report_delete'),
    
    path('incidentReport/general', views.incident_report_general, name='incident_report_general'),
    path('incidentReport/people', views.incident_report_people, name='incident_report_people'),
    path('incidentReport/vehicle', views.incident_report_vehicle, name='incident_report_vehicle'),
    path('incidentReport/media', views.incident_report_media, name='incident_report_media'),
    path('incidentReport/remarks', views.incident_report_remarks, name='incident_report_remarks'),
    path('incidentReport/formsubmission', views.multistepformsubmission.as_view(FORMS), name='multistepformsubmission'),
    path('incidentReport/general/view/<int:id>', views.incident_report_general_view, name='incident_report_general_view'),
    path('incidentReport/people/view/<int:id>', views.incident_report_people_view, name='incident_report_people_view'),
    path('incidentReport/vehicle/view/<int:id>', views.incident_report_vehicle_view, name='incident_report_vehicle_view'),
    path('incidentReport/media/view/<int:id>', views.incident_report_media_view, name='incident_report_media_view'),
    path('incidentReport/remarks/view/<int:id>', views.incident_report_remarks_view, name='incident_report_remarks_view'),
    path('incidentReport/general/edit/<int:id>', views.incident_report_general_edit, name='incident_report_general_edit'),
    path('incidentReport/people/edit/<int:id>', views.incident_report_people_edit, name='incident_report_people_edit'),
    # path('incidentReport/vehicle/edit/<int:id>', views.incident_report_vehicle_edit, name='incident_report_vehicle_edit'),
    # path('incidentReport/media/edit/<int:id>', views.incident_report_media_edit, name='incident_report_media_edit'),
    # path('incidentReport/remarks/edit/<int:id>', views.incident_report_remarks_edit, name='incident_report_remarks_edit'),
    
    path('ajax/load-accident/', views.load_accident, name='ajax_load_accident'), # AJAX
    path('ajax/load-collision/', views.load_collision, name='ajax_load_collision'), # AJAX
    
    path('', FormView, {'step': None}),
    path('step/<int:step>', FormView),
    path('cancel', CancelView),
]