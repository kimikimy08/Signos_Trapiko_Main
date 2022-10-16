from django.urls import path, include
from . import views
from accounts import views as AccountViews
from .views_inc import FormView, CancelView

urlpatterns = [
    path('userReport', views.user_report, name='user_report'),
    path('userReport/pending', views.user_report_pending, name='user_report_pending'),
    path('userReport/approved', views.user_report_approved, name='user_report_approved'),
    path('userReport/rejected', views.user_report_rejected, name='user_report_rejected'),
    # path('userReport/today', views.user_report_today, name='user_report_today'),
    
    path('userReports', views.user_reports, name='user_reports'),
    path('userReports/pending', views.user_reports_pending, name='user_reports_pending'),
    path('userReports/approved', views.user_reports_approved, name='user_reports_approved'),
    path('userReports/rejected', views.user_reports_rejected, name='user_reports_rejected'),
    path('userReports/today', views.user_reports_today, name='user_reports_today'),
    path('userReports/delete/<int:id>', views.user_report_delete, name='user_report_delete'),
   
    
    path('myReport', views.my_report, name='my_report'),
    path('myReport/pending', views.my_report_pending, name='my_report_pending'),
    path('myReport/approved', views.my_report_approved, name='my_report_approved'),
    path('myReport/rejected', views.my_report_rejected, name='my_report_rejected'),
    # path('myReport/add', views.my_report_add, name='my_report_add'),
    path('myReport/view/<int:id>', views.my_report_view, name='my_report_view'),
    path('myReport/edit/<int:id>', views.my_report_edit, name='my_report_edit'),
    path('myReport/delete/<int:id>', views.my_report_delete, name='my_report_delete'),
    
    path('incidentReport/general', views.incident_report_general, name='incident_report_general'),
    path('incidentReport/people', views.incident_report_people, name='incident_report_people'),
    path('incidentReport/vehicle', views.incident_report_vehicle, name='incident_report_vehicle'),
    path('incidentReport/media', views.incident_report_media, name='incident_report_media'),
    path('incidentReport/remarks', views.incident_report_remarks, name='incident_report_remarks'),
    # path('incidentReport/formsubmission', views.multistepformsubmission.as_view(FORMS), name='multistepformsubmission'),
    # path('incidentReport/formsubmissions', views.incident_form_super, name='incident_form_super'),
    # path('incidentReport/formsubmission', views.incident_form_admin, name='incident_form_admin'),
    path('incidentReport/incident', views.incident_form_member, name='incident_form_member'),


    
    path('attributes_builder/accident_factor', views.attributes_builder_accident_admin, name='attributes_builder_accident_admin'),
    path('attributes_builder/accident_factor_sub/<int:id>', views.attributes_builder_accident_sub_admin, name='attributes_builder_accident_sub_admin'),
    path('attributes_builder/crash', views.attributes_builder_crash_admin, name='attributes_builder_crash_admin'),
    path('attributes_builder/collision_type', views.attributes_builder_collision_admin, name='attributes_builder_collision_admin'),
    path('attributes_builder/collision_type_sub/<int:id>', views.attributes_builder_collision_sub_admin, name='attributes_builder_collision_sub_admin'),
    path('attributes_builder/accident_factor/add', views.attributes_builder_accident_add_admin, name='attributes_builder_accident_add_admin'),
    path('attributes_builder/accident_factor/edit/<int:id>', views.attributes_builder_accident_edit_admin, name='attributes_builder_accident_edit_admin'),
    path('attributes_builder/accident_factor/delete/<int:id>', views.attributes_builder_accident_delete_admin, name='attributes_builder_accident_delete_admin'),
    path('attributes_builder/accident_factor_sub/add', views.attributes_builder_accident_add_sub_admin, name='attributes_builder_accident_add_sub_admin'),
    path('attributes_builder/accident_factor_sub/edit/<int:id>', views.attributes_builder_accident_edit_sub_admin, name='attributes_builder_accident_edit_sub_admin'),
    path('attributes_builder/accident_factor_sub/delete/<int:id>', views.attributes_builder_accident_delete_sub_admin, name='attributes_builder_accident_delete_sub_admin'),
    path('attributes_builder/collision_type/add', views.attributes_builder_collision_add_admin, name='attributes_builder_collision_add_admin'),
    path('attributes_builder/collision_type/edit/<int:id>', views.attributes_builder_collision_edit_admin, name='attributes_builder_collision_edit_admin'),
    path('attributes_builder/collision_type/delete/<int:id>', views.attributes_builder_collision_delete_admin, name='attributes_builder_collision_delete_admin'),
    path('attributes_builder/collision_type_sub/add', views.attributes_builder_collision_add_sub_admin, name='attributes_builder_collision_add_sub_admin'),
    path('attributes_builder/collision_type_sub/edit/<int:id>', views.attributes_builder_collision_edit_sub_admin, name='attributes_builder_collision_edit_sub_admin'),
    path('attributes_builder/collision_type_sub/delete/<int:id>', views.attributes_builder_collision_delete_sub_admin, name='attributes_builder_collision_delete_sub_admin'),
    path('attributes_builder/crash_type/add', views.attributes_builder_crash_add_admin, name='attributes_builder_crash_add_admin'),
    path('attributes_builder/crash_type/edit/<int:id>', views.attributes_builder_crash_edit_admin, name='attributes_builder_crash_edit_admin'),
    path('attributes_builder/crash_type/delete/<int:id>', views.attributes_builder_crash_delete_admin, name='attributes_builder_crash_delete_admin'),
    
    path('attributes_builders/accident_factor', views.attributes_builder_accident, name='attributes_builder_accident'),
    path('attributes_builders/accident_factor_sub/<int:id>', views.attributes_builder_accident_sub, name='attributes_builder_accident_sub'),
    path('attributes_builders/crash', views.attributes_builder_crash, name='attributes_builder_crash'),
    path('attributes_builders/collision_type', views.attributes_builder_collision, name='attributes_builder_collision'),
    path('attributes_builders/collision_type_sub/<int:id>', views.attributes_builder_collision_sub, name='attributes_builder_collision_sub'),
    path('attributes_builders/accident_factor/add', views.attributes_builder_accident_add, name='attributes_builder_accident_add'),
    path('attributes_builders/accident_factor/edit/<int:id>', views.attributes_builder_accident_edit, name='attributes_builder_accident_edit'),
    path('attributes_builders/accident_factor/delete/<int:id>', views.attributes_builder_accident_delete, name='attributes_builder_accident_delete'),
    path('attributes_builders/accident_factor_sub/add', views.attributes_builder_accident_add_sub, name='attributes_builder_accident_add_sub'),
    path('attributes_builders/accident_factor_sub/edit/<int:id>', views.attributes_builder_accident_edit_sub, name='attributes_builder_accident_edit_sub'),
    path('attributes_builders/accident_factor_sub/delete/<int:id>', views.attributes_builder_accident_delete_sub, name='attributes_builder_accident_delete_sub'),
    path('attributes_builders/collision_type/add', views.attributes_builder_collision_add, name='attributes_builder_collision_add'),
    path('attributes_builders/collision_type/edit/<int:id>', views.attributes_builder_collision_edit, name='attributes_builder_collision_edit'),
    path('attributes_builders/collision_type/delete/<int:id>', views.attributes_builder_collision_delete, name='attributes_builder_collision_delete'),
    path('attributes_builders/collision_type_sub/add', views.attributes_builder_collision_add_sub, name='attributes_builder_collision_add_sub'),
    path('attributes_builders/collision_type_sub/edit/<int:id>', views.attributes_builder_collision_edit_sub, name='attributes_builder_collision_edit_sub'),
    path('attributes_builders/collision_type_sub/delete/<int:id>', views.attributes_builder_collision_delete_sub, name='attributes_builder_collision_delete_sub'),
    path('attributes_builders/crash_type/add', views.attributes_builder_crash_add, name='attributes_builder_crash_add'),
    path('attributes_builders/crash_type/edit/<int:id>', views.attributes_builder_crash_edit, name='attributes_builder_crash_edit'),
    path('attributes_builders/crash_type/delete/<int:id>', views.attributes_builder_crash_delete, name='attributes_builder_crash_delete'),
    
    
    path('ajax/load-accident/', views.load_accident, name='ajax_load_accident'), # AJAX
    path('ajax/load-collision/', views.load_collision, name='ajax_load_collision'), # AJAX
    
    
    
    path('incidentreport', views.a_incidentreports, name='a_incidentreports'),
    path('incidentreport/additional', views.a_incidentreports_additional, name='a_incidentreports_additional'),
    
    
    path('incidentreports', views.sa_incidentreports, name='sa_incidentreports'),
    path('incidentreports/additional', views.sa_incidentreports_additional, name='sa_incidentreports_additional'),
    
    path('incidentReports/general/view/<int:id>', views.incident_report_general_view, name='incident_report_general_view'),
    path('incidentReports/people/view/<int:id>', views.incident_report_people_vehicle_main, name='incident_report_people_vehicle_main'),
    path('incidentReports/vehicle/view/<int:id>', views.incident_report_vehicle_main, name='incident_report_vehicle_main'),
    path('incidentReports/media/view/<int:id>', views.incident_report_media_main, name='incident_report_media_main'),
    path('incidentReports/people/view/<int:id>/<int:people_id>', views.incident_report_people_vehicle_view, name='incident_report_people_vehicle_view'),
    path('incidentReports/vehicle/view/<int:id>/<int:vehicle_id>', views.incident_report_vehicle_view, name='incident_report_vehicle_view'),
    path('incidentReports/media/view/<int:id>/<int:media_id>', views.incident_report_media_view, name='incident_report_media_view'),
    path('incidentReports/remarks/view/<int:id>', views.incident_report_remarks_view, name='incident_report_remarks_view'),
    path('incidentReports/general/edit/<int:id>', views.incident_report_general_edit, name='incident_report_general_edit'),
    path('incidentReports/people/edit/<int:id>/<int:people_id>', views.incident_report_people_edit, name='incident_report_people_edit'),
    path('incidentReports/vehicle/edit/<int:id>/<int:vehicle_id>', views.incident_report_vehicle_edit, name='incident_report_vehicle_edit'),
    path('incidentReports/media/edit/<int:id>/<int:media_id>', views.incident_report_media_edit, name='incident_report_media_edit'),
    path('incidentReports/remarks/edit/<int:id>', views.incident_report_remarks_edit, name='incident_report_remarks_edit'),
    
    path('incidentReport/general/view/<int:id>', views.a_incident_report_general_view, name='a_incident_report_general_view'),
    path('incidentReport/people/view/<int:id>', views.a_incident_report_people_vehicle_main, name='a_incident_report_people_vehicle_main'),
    path('incidentReport/vehicle/view/<int:id>', views.a_incident_report_vehicle_main, name='a_incident_report_vehicle_main'),
    path('incidentReport/media/view/<int:id>', views.a_incident_report_media_main, name='a_incident_report_media_main'),
    path('incidentReport/people/view/<int:id>/<int:people_id>', views.a_incident_report_people_vehicle_view, name='a_incident_report_people_vehicle_view'),
    path('incidentReport/vehicle/view/<int:id>/<int:vehicle_id>', views.a_incident_report_vehicle_view, name='a_incident_report_vehicle_view'),
    path('incidentReport/media/view/<int:id>/<int:media_id>', views.a_incident_report_media_view, name='a_incident_report_media_view'),
    path('incidentReport/remarks/view/<int:id>', views.a_incident_report_remarks_view, name='a_incident_report_remarks_view'),
    path('incidentReport/general/edit/<int:id>', views.a_incident_report_general_edit, name='a_incident_report_general_edit'),
    path('incidentReport/people/edit/<int:id>/<int:people_id>', views.a_incident_report_people_edit, name='a_incident_report_people_edit'),
    path('incidentReport/vehicle/edit/<int:id>/<int:vehicle_id>', views.a_incident_report_vehicle_edit, name='a_incident_report_vehicle_edit'),
    path('incidentReport/media/edit/<int:id>/<int:media_id>', views.a_incident_report_media_edit, name='a_incident_report_media_edit'),
    path('incidentReport/remarks/edit/<int:id>', views.a_incident_report_remarks_edit, name='a_incident_report_remarks_edit'),
    

]