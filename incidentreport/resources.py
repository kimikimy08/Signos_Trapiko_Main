

from import_export import resources
from .models import UserReport, IncidentGeneral, IncidentRemark, IncidentPerson,IncidentVehicle

class UserReportResource(resources.ModelResource):
    class Meta:
        model = UserReport
        
class IncidentGeneraltResource(resources.ModelResource):
    class Meta:
        model = IncidentGeneral
        
class IncidentRemarkResources(resources.ModelResource):
    class Meta:
        model = IncidentRemark
        
class IncidentPeopleResources(resources.ModelResource):
    class Meta:
        model = IncidentPerson

class IncidentVehicleResources(resources.ModelResource):
    class Meta:
        model = IncidentVehicle