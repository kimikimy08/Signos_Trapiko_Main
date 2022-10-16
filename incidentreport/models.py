import os
from django.db import models
from accounts.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver
from PIL import Image


# class Barangay_district(models.Model):
#     name = models.CharField(max_length=250)
#     district = models.CharField(max_length=250)
class UserReport(models.Model):
    PENDING = 1
    APPROVED = 2
    REJECTED = 3
    STATUS = (
        (PENDING, 'Pending'),
        (APPROVED, 'Approved'),
        (REJECTED, 'Rejected')
    )
    
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    # barangay = models.ForeignKey(Barangay_district, on_delete=models.CASCADE, null=True)
    description = models.TextField(max_length=250, blank=True)
    address = models.CharField(max_length=250)
    country = models.CharField(max_length=50, blank=True, null=True)
    state = models.CharField(max_length=250, blank=True, null=True)
    city = models.CharField(max_length=50, blank=True, null=True)
    pin_code = models.CharField(max_length=6, blank=True, null=True)
    latitude = models.FloatField(max_length=20, blank=True, null=True)
    longitude = models.FloatField(max_length=20, blank=True, null=True)
    upload_photovideo = models.FileField(upload_to='incident_report/image', blank=True, null=True)
    date = models.DateField(auto_now_add=False, auto_now=False, blank=True, null=True)
    time = models.TimeField(auto_now_add=False, auto_now=False, blank=True, null=True)
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
    
    def save(self, *args, **kwargs):
        super(UserReport, self).save(*args, **kwargs)
        if self.upload_photovideo:
            if  ".jpg" in self.upload_photovideo.url or ".png" in self.upload_photovideo.url:
             #check if image exists before resize
                img = Image.open(self.upload_photovideo.path)

                if img.height > 1080 or img.width > 1920:
                    new_height = 720
                    new_width = int(new_height / img.height * img.width)
                    img = img.resize((new_width, new_height))
                    img.save(self.upload_photovideo.path)

    

class AccidentCausation(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
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
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
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
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    crash_type = models.CharField(max_length=250, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.crash_type

class IncidentGeneral(models.Model):
    WEATHER = (
        ('Clear Night', 'Clear Night'),
        ('Cloudy', 'Cloudy'),
        ('Day', 'Day'),
        ('Fog', 'Fog'),
        ('Hail', 'Hail'),
        ('Partially cloudy day', 'Partially cloudy day'),
        ('Partially cloudy night', 'Partially cloudy night'),
        ('Rain', 'Rain'),
        ('Rain', 'Rain'),
        ('Wind', 'Wind'),
    )
    
    LIGHT = (
        ('Dawn', 'Dawn'),
        ('Day', 'Day'),
        ('Dusk', 'Dusk'),
        ('Night', 'Night'),
    )
    
    SEVERITY = (
        ('Damage to Property', 'Damage to Property'),
        ('Fatal', 'Fatal'),
        ('Non-Fatal', 'Non-Fatal'),
    )
    
    user = models.ForeignKey(User, on_delete=models.CASCADE, editable=False, null=True, blank=True)
    user_report = models.OneToOneField(UserReport, on_delete=models.CASCADE)
    accident_factor = models.ForeignKey(AccidentCausation, on_delete=models.SET_NULL, blank=True, null=True)
    accident_subcategory = models.ForeignKey(AccidentCausationSub, on_delete=models.SET_NULL, blank=True, null=True)
    collision_type = models.ForeignKey(CollisionType, on_delete=models.SET_NULL, blank=True, null=True)
    collision_subcategory = models.ForeignKey(CollisionTypeSub, on_delete=models.SET_NULL, blank=True, null=True)
    crash_type = models.ForeignKey(CrashType, on_delete=models.SET_NULL, blank=True, null=True)
    weather =  models.CharField(choices=WEATHER, max_length=250,blank=True, null=True)
    light =  models.CharField(choices=LIGHT,max_length=250, blank=True, null=True)
    severity = models.CharField(choices=SEVERITY, max_length=250, blank=True, null=True)
    movement_code = models.CharField(max_length=250, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    


    # @receiver(post_save, sender=UserReport)
    # def create_user_report_general(sender, instance, created, **kwargs):
    #     if created:
    #         IncidentGeneral.objects.create(user_report=instance)
    
    # post_save.connect(create_user_report_general, sender=UserReport) 

class IncidentPerson(models.Model):
    GENDER = (
        ('Female', 'Female'),
        ('Male', 'Male'),
    )
    
    INVOLVEMENT = (
        ('Pedestrian', 'Pedestrian'),
        ('Witness', 'Witness'),
        ('Passenger', 'Passenger'),
        ('Driver', 'Driver'),
    )
    
    ID_PRESENTED = (
        ("Driver's License", "Driver's License"),
        ('Government', 'Government'),
        ('Passport', 'Passport'),
        ('School Id', 'School Id'),
        ('Others', 'Others'),
    )
    
    INJURY = (
        ("Fatal", "Fatal"),
        ('Minor', 'Minor'),
        ('Not Injured', 'Not Injured'),
        ('Serious', 'Serious'),
    )
    
    DRIVER_ERROR = (
        ("Bad Overtaking", "Bad Overtaking"),
        ('Bad Turning', 'Bad Turning'),
        ('Fatigued / Asleep', 'Fatigued / Asleep'),
        ('Inattentive', 'Inattentive'),
        ('No Signal', 'No Signal'),
        ('Too Close', 'Too Close'),
        ('Too Fast', 'Too Fast'),
        ('Using Cellphone', 'Using Cellphone'),
    )
    
    ALCOHOL_DRUGS = (
        ("Alcohol Suspected", "Alcohol Suspected"),
        ('Drugs suspected', 'Drugs suspected'),
    )
    
    SEATBELT_HELMET = (
        ("Seat belt/Helmet Worn", "Seat belt/Helmet Worn"),
        ('Not worn', 'Not worn'),
        ('Not worn correctly', 'Not worn correctly'),
    )
    
    incident_general = models.ForeignKey(IncidentGeneral, on_delete=models.CASCADE)
    incident_first_name = models.CharField(max_length=250, blank=True)
    incident_middle_name = models.CharField(max_length=250, blank=True)
    incident_last_name = models.CharField(max_length=250, blank=True)
    incident_age = models.CharField(max_length=250, blank=True)
    incident_gender =  models.CharField(choices=GENDER,max_length=250, blank=True, null=True)
    incident_address = models.CharField(max_length=250, blank=True)
    incident_involvement =  models.CharField(choices=INVOLVEMENT, max_length=250,blank=True, null=True)
    incident_id_presented =  models.CharField(choices=ID_PRESENTED, max_length=250,blank=True, null=True)
    incident_id_number = models.CharField(max_length=250, blank=True)
    incident_injury =  models.CharField(choices=INJURY, max_length=250,blank=True, null=True)
    incident_driver_error =  models.CharField(choices=DRIVER_ERROR,max_length=250, blank=True, null=True)
    incident_alcohol_drugs =  models.CharField(choices=ALCOHOL_DRUGS, max_length=250,blank=True, null=True)
    incident_seatbelt_helmet =  models.CharField(choices=SEATBELT_HELMET,max_length=250, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)



class IncidentVehicle(models.Model):
    CLASSIFICATION = (
        ('Diplomat', 'Diplomat'),
        ('Government', 'Government'),
        ('Private', 'Private'),
        ('Public / For Hire`', 'Public / For Hire`'),
    )
    
    VEHICLE_TYPE = (
        ('Ambulance', 'Ambulance'),
        ('Animal', 'Animal'),
        ('Armored Car', 'Armored Car'),
        ('Bicycle', 'Bicycle'),
        ('Bus', 'Bus'),
        ('Car', 'Car'),
        ('Electric Bike', 'Electric Bike'),
        ('Habal-habal', 'Habal-habal'),
        ('Heavy Equipment', 'Heavy Equipment'),
        ('Horse-Driven Carriage (Tartanilla)', 'Horse-Driven Carriage (Tartanilla)'),
        ('Jeepney', 'Jeepney'),
        ('Motorcycle', 'Motorcycle'),
        ('Pedestrian', 'Pedestrian'),
        ('Pedicab', 'Pedicab'),
        ('Push-Cart', 'Push-Cart'),
        ('SUV', 'SUV'),
        ('Taxi (metered)', 'Taxi (metered)'),
        ('Tricycle (Articulated)', 'Tricycle (Articulated)'),
        ('Truck (Fire)', 'Truck (Fire)'),
        ('Truck (Pick-up)', 'Truck (Pick-up)'),
        ('Truck (Rigid)', 'Truck (Rigid)'),
        ('Truck (Unknown)', 'Truck (Unknown)'),
        ('Van', 'Van'),
        ('Water Vessel', 'Water Vessel'),
        ('Others', 'Others'),
    )
    
    MANEUVER = (
        ("Left-turn", "Left-turn"),
        ('Right-turn', 'Right-turn'),
        ('U-turn', 'U-turn'),
        ('Cross Traffic', 'Cross Traffic'),
        ('Merging', 'Merging'),
        ('Diverging', 'Diverging'),
        ('Overtaking', 'Overtaking'),
        ('Going Ahead', 'Going Ahead'),
        ('Reversing', 'Reversing'),
        ('Sudden Start', 'Sudden Start'),
        ('Sudden Stop', 'Sudden Stop'),
        ('Parked Off Road', 'Parked Off Road'),
        ('Parked On Road', 'Parked On Road'),
    )
    
    DAMAGE = (
        ("None", "None"),
        ('Front', 'Front'),
        ('Left', 'Left'),
        ('Multiple', 'Multiple'),
        ('Rear', 'Rear'),
        ('Right', 'Right'),
        ('Roof', 'Roof'),
    )
    
    DEFECT = (
        ("None", "None"),
        ('Breaks', 'Breaks'),
        ('Lights', 'Lights'),
        ('Multiple', 'Multiple'),
        ('Steering', 'Steering'),
        ('Tires', 'Tires'),
    )
    
    LOADING = (
        ("Legal", "Legal"),
        ('Overloaded', 'Overloaded'),
        ('Unsafe Load', 'Unsafe Load'),
        ('Others', 'Others'),
    )
    incident_general = models.ForeignKey(IncidentGeneral, on_delete=models.CASCADE)
    classification = models.CharField(choices=CLASSIFICATION, max_length=250, blank=True, null=True)
    vehicle_type = models.CharField(choices=VEHICLE_TYPE, max_length=250, blank=True, null=True)
    brand = models.CharField(max_length=250, blank=True)
    plate_number = models.CharField(max_length=250, blank=True)
    engine_number = models.CharField(max_length=250, blank=True)
    chassis_number = models.CharField(max_length=250, blank=True)
    insurance_details = models.TextField(max_length=250, blank=True)
    maneuver = models.CharField(choices=MANEUVER, max_length=250,blank=True, null=True)
    damage =models.CharField(choices=DAMAGE,max_length=250, blank=True, null=True)
    defect = models.CharField(choices=DEFECT,max_length=250, blank=True, null=True)
    loading = models.CharField(choices=LOADING,max_length=250, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __int__(self):
        return self.id

class IncidentMedia(models.Model):
    incident_general = models.ForeignKey(IncidentGeneral, on_delete=models.CASCADE)
    media_description = models.TextField(max_length=250, blank=True)
    incident_upload_photovideo = models.ImageField(default='user.jpeg', upload_to='incident_report/image')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __int__(self):
        return self.id
    
    

class IncidentRemark(models.Model):
    incident_general = models.OneToOneField(IncidentGeneral, on_delete=models.CASCADE)
    responder =  models.CharField(max_length=250, blank=True)
    action_taken = models.TextField(max_length=250, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.responder
    
    # @receiver(post_save, sender=IncidentGeneral)
    # def create_user_report_remark(sender, instance, created, **kwargs):
    #     if created:
    #         IncidentRemark.objects.create(incident_general=instance)
    
    # post_save.connect(create_user_report_remark, sender=IncidentGeneral) 


class Incident(models.Model):
    incident_general = models.OneToOneField(IncidentGeneral, on_delete=models.CASCADE)
    user_report = models.OneToOneField(UserReport, on_delete=models.CASCADE, blank=True, null=True)
    incident_general = models.ForeignKey(IncidentGeneral, on_delete=models.SET_NULL, blank=True, null=True)
    incident_person = models.ForeignKey(IncidentPerson, on_delete=models.SET_NULL, blank=True, null=True)
    incident_vehicle = models.ForeignKey(IncidentVehicle, on_delete=models.SET_NULL, blank=True, null=True)
    incident_media = models.ForeignKey(IncidentMedia, on_delete=models.SET_NULL, blank=True, null=True)
    incident_remark = models.ForeignKey(IncidentRemark, on_delete=models.SET_NULL, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    modified_at = models.DateTimeField(auto_now=True)