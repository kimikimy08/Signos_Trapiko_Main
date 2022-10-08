from django.contrib import admin
from .models import UserReport,IncidentPerson, AccidentCausation, CollisionType, CrashType,IncidentGeneral, IncidentVehicle,IncidentMedia,IncidentRemark, AccidentCausationSub, CollisionTypeSub

class CustomIncidentGeneralAdmin(admin.ModelAdmin):
    list_display = ('accident_factor', 'severity')
    # list_display_links = ('user', 'birthdate')
    
# Register your models here.
admin.site.register(UserReport)
admin.site.register(AccidentCausation)
admin.site.register(AccidentCausationSub)
admin.site.register(CollisionType)
admin.site.register(CollisionTypeSub)
admin.site.register(CrashType)
admin.site.register(IncidentGeneral, CustomIncidentGeneralAdmin)
admin.site.register(IncidentPerson)
admin.site.register(IncidentVehicle)
admin.site.register(IncidentMedia)
admin.site.register(IncidentRemark)

