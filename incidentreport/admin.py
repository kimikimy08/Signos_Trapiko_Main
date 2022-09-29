from django.contrib import admin
from .models import UserReport,IncidentPerson, AccidentCausation, CollisionType, CrashType,IncidentGeneral, IncidentVehicle,IncidentMedia,IncidentRemark

# Register your models here.
admin.site.register(UserReport)
admin.site.register(AccidentCausation)
admin.site.register(CollisionType)
admin.site.register(CrashType)
admin.site.register(IncidentGeneral)
admin.site.register(IncidentPerson)
admin.site.register(IncidentVehicle)
admin.site.register(IncidentMedia)
admin.site.register(IncidentRemark)

