from django.db import models
from accounts.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver

class UserReport(models.Model):
    PENDING = 1
    APPROVED = 2
    REJECTED = 3
    STATUS = (
        (PENDING, 'Pending'),
        (APPROVED, 'Approved'),
        (REJECTED, 'Rejected')
    )
    user = models.ForeignKey(User, on_delete=models.SET_DEFAULT, default='Anonymous')
    description = models.TextField(max_length=250, blank=True)
    location = models.CharField(max_length=250)
    upload_photovideo = models.ImageField(default='user.jpeg', upload_to='incident_report/image')
    date = models.DateField(auto_now_add=True)
    time = models.TimeField(auto_now_add=True)
    status = models.PositiveSmallIntegerField(choices=STATUS, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def get_status(self):
        if self.status == 1:
            incident_status = 'Pending'
        elif self.status == 2:
            incident_status = 'Approved'
        elif self.status == 3:
            incident_status = 'Rejected'
        return incident_status

    def __str__(self):
        return self.user.username
    

class AccidentCausation(models.Model):
    category = models.CharField(max_length=250)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.category

class AccidentCausationSub(models.Model):
    accident_factor = models.ForeignKey(AccidentCausation, on_delete=models.CASCADE)
    sub_category = models.CharField(max_length=250, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.sub_category


class CollisionType(models.Model):
    category = models.CharField(max_length=250)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.category

class CollisionTypeSub(models.Model):
    collision_type = models.ForeignKey(CollisionType, on_delete=models.CASCADE)
    sub_category = models.CharField(max_length=250, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.sub_category

class CrashType(models.Model):
    crash_type = models.CharField(max_length=250, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.crash_type

class IncidentGeneral(models.Model):
    WEATHER = (
        (1, 'Clear Night'),
        (2, 'Cloudy'),
        (3, 'Day'),
        (4, 'Fog'),
        (5, 'Hail'),
        (6, 'Partially cloudy day'),
        (7, 'Partially cloudy night'),
        (8, 'Rain'),
        (9, 'Rain'),
        (10, 'Wind'),
    )
    
    LIGHT = (
        (1, 'Dawn'),
        (2, 'Day'),
        (3, 'Dusk'),
        (4, 'Night'),
    )
    
    SEVERITY = (
        (1, 'Damage to Property'),
        (2, 'Fatal'),
        (3, 'Non-Fatal'),
    )
    
    user_report = models.OneToOneField(UserReport, on_delete=models.CASCADE, primary_key=True)
    accident_factor = models.OneToOneField(AccidentCausation, on_delete=models.CASCADE)
    collision_type = models.OneToOneField(CollisionType, on_delete=models.CASCADE)
    crash_type = models.OneToOneField(CrashType, on_delete=models.CASCADE)
    weather = models.PositiveSmallIntegerField(choices=WEATHER, blank=True, null=True)
    light = models.PositiveSmallIntegerField(choices=LIGHT, blank=True, null=True)
    severity = models.PositiveSmallIntegerField(choices=SEVERITY, blank=True, null=True)
    movement_code = models.CharField(max_length=250, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    @receiver(post_save, sender=UserReport)
    def create_user_report_general(sender, instance, created, **kwargs):
        if created:
            IncidentGeneral.objects.get_or_create(user_report=instance)
    
    post_save.connect(create_user_report_general, sender=UserReport) 

class IncidentPerson(models.Model):
    GENDER = (
        (1, 'Female'),
        (2, 'Male'),
    )
    
    INVOLVEMENT = (
        (1, 'Pedestrian'),
        (2, 'Witness'),
        (3, 'Passenger'),
        (4, 'Driver'),
    )
    
    ID_PRESENTED = (
        (1, "Driver's License"),
        (2, 'Government'),
        (3, 'Passport'),
        (4, 'School Id'),
        (5, 'Others'),
    )
    
    INJURY = (
        (1, "Fatal"),
        (2, 'Minor'),
        (3, 'Not Injured'),
        (4, 'Serious'),
    )
    
    DRIVER_ERROR = (
        (1, "Bad Overtaking"),
        (2, 'Bad Turning'),
        (3, 'Fatigued / Asleep'),
        (4, 'Inattentive'),
        (5, 'No Signal'),
        (6, 'Too Close'),
        (7, 'Too Fast'),
        (8, 'Using Cellphone'),
    )
    
    ALCOHOL_DRUGS = (
        (1, "Alcohol Suspected"),
        (2, 'Drugs suspected'),
    )
    
    SEATBELT_HELMET = (
        (1, "Seat belt/Helmet Worn"),
        (2, 'Not worn'),
        (3, 'Not worn correctly'),
    )
    incident_general = models.ManyToManyField(IncidentGeneral, blank=True, null=True)
    incident_first_name = models.CharField(max_length=250, blank=True)
    incident_middle_name = models.CharField(max_length=250, blank=True)
    incident_last_name = models.CharField(max_length=250, blank=True)
    incident_age = models.CharField(max_length=250, blank=True)
    incident_gender = models.PositiveSmallIntegerField(choices=GENDER, blank=True, null=True)
    incident_address = models.CharField(max_length=250, blank=True)
    incident_involvement = models.PositiveSmallIntegerField(choices=INVOLVEMENT, blank=True, null=True)
    incident_id_presented = models.PositiveSmallIntegerField(choices=ID_PRESENTED, blank=True, null=True)
    incident_id_number = models.CharField(max_length=250, blank=True)
    incident_injury = models.PositiveSmallIntegerField(choices=INJURY, blank=True, null=True)
    incident_driver_error = models.PositiveSmallIntegerField(choices=DRIVER_ERROR, blank=True, null=True)
    incident_alcohol_drugs = models.PositiveSmallIntegerField(choices=ALCOHOL_DRUGS, blank=True, null=True)
    incident_seatbelt_helmet = models.PositiveSmallIntegerField(choices=SEATBELT_HELMET, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)



class IncidentVehicle(models.Model):
    CLASSIFICATION = (
        (1, 'Diplomat'),
        (2, 'Government'),
        (3, 'Private'),
        (4, 'Public / For Hire`'),
    )
    
    VEHICLE_TYPE = (
        (1, 'Ambulance'),
        (2, 'Animal'),
        (3, 'Armored Car'),
        (4, 'Bicycle'),
        (5, 'Bus'),
        (6, 'Car'),
        (7, 'Electric Bike'),
        (8, 'Habal-habal '),
        (9, 'Heavy Equipment'),
        (10, 'Horse-Driven Carriage (Tartanilla)'),
        (11, 'Jeepney'),
        (12, 'Motorcycle'),
        (13, 'Pedestrian'),
        (14, 'Pedicab'),
        (15, 'Push-Cart'),
        (16, 'SUV'),
        (17, 'Taxi (metered)'),
        (18, 'Tricycle (Articulated)'),
        (19, 'Truck (Fire)'),
        (20, 'Truck (Pick-up)'),
        (21, 'Truck (Rigid)'),
        (22, 'Truck (Unknown)'),
        (23, 'Van'),
        (24, 'Water Vessel'),
        (25, 'Others'),
    )
    
    MANEUVER = (
        (1, "Left-turn"),
        (2, 'Right-turn'),
        (3, 'U-turn'),
        (4, 'Cross Traffic'),
        (5, 'Merging'),
        (6, 'Diverging'),
        (7, 'Overtaking'),
        (8, 'Going Ahead'),
        (9, 'Reversing'),
        (10, 'Sudden Start'),
        (11, 'Sudden Stop'),
        (12, 'Parked Off Road'),
        (13, 'Parked On Road'),
    )
    
    DAMAGE = (
        (1, "None"),
        (2, 'Front'),
        (3, 'Left'),
        (4, 'Multiple'),
        (5, 'Rear'),
        (6, 'Right'),
        (7, 'Roof'),
    )
    
    DEFECT = (
        (1, "None"),
        (2, 'Breaks'),
        (3, 'Lights'),
        (4, 'Multiple'),
        (5, 'Steering'),
        (6, 'Tires'),
    )
    
    LOADING = (
        (1, "Legal"),
        (2, 'Overloaded'),
        (3, 'Unsafe Load'),
        (4, 'Others'),
    )

    
    incident_general = models.ManyToManyField(IncidentGeneral, blank=True, null=True)
    classification = models.PositiveSmallIntegerField(choices=CLASSIFICATION, blank=True, null=True)
    vehicle_type = models.PositiveSmallIntegerField(choices=VEHICLE_TYPE, blank=True, null=True)
    brand = models.CharField(max_length=250, blank=True)
    plate_number = models.CharField(max_length=250, blank=True)
    engine_number = models.CharField(max_length=250, blank=True)
    chassis_number = models.CharField(max_length=250, blank=True)
    insurance_details = models.TextField(max_length=250, blank=True)
    maneuver = models.PositiveSmallIntegerField(choices=MANEUVER, blank=True, null=True)
    damage = models.PositiveSmallIntegerField(choices=DAMAGE, blank=True, null=True)
    defect = models.PositiveSmallIntegerField(choices=DEFECT, blank=True, null=True)
    loading = models.PositiveSmallIntegerField(choices=LOADING, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __int__(self):
        return self.id

class IncidentMedia(models.Model):
    
    description = models.TextField(max_length=250, blank=True)
    incident_upload_photovideo = models.ImageField(default='user.jpeg', upload_to='incident_report/image')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.description

class IncidentRemark(models.Model):
    incident_general = models.ManyToManyField(IncidentGeneral, blank=True, null=True)
    responder =  models.CharField(max_length=250, blank=True)
    action_taken = models.TextField(max_length=250, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.responder

