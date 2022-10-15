# Generated by Django 4.0.4 on 2022-10-15 07:53

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='AccidentCausation',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('category', models.CharField(max_length=250)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('user', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='AccidentCausationSub',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('sub_category', models.CharField(blank=True, max_length=250)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('accident_factor', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='incidentreport.accidentcausation')),
            ],
        ),
        migrations.CreateModel(
            name='CollisionType',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('category', models.CharField(max_length=250)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('user', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='CollisionTypeSub',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('sub_category', models.CharField(blank=True, max_length=250)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('collision_type', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='incidentreport.collisiontype')),
            ],
        ),
        migrations.CreateModel(
            name='CrashType',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('crash_type', models.CharField(blank=True, max_length=250)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('user', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='IncidentGeneral',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('weather', models.CharField(blank=True, choices=[('Clear Night', 'Clear Night'), ('Cloudy', 'Cloudy'), ('Day', 'Day'), ('Fog', 'Fog'), ('Hail', 'Hail'), ('Partially cloudy day', 'Partially cloudy day'), ('Partially cloudy night', 'Partially cloudy night'), ('Rain', 'Rain'), ('Rain', 'Rain'), ('Wind', 'Wind')], max_length=250, null=True)),
                ('light', models.CharField(blank=True, choices=[('Dawn', 'Dawn'), ('Day', 'Day'), ('Dusk', 'Dusk'), ('Night', 'Night')], max_length=250, null=True)),
                ('severity', models.CharField(blank=True, choices=[('Damage to Property', 'Damage to Property'), ('Fatal', 'Fatal'), ('Non-Fatal', 'Non-Fatal')], max_length=250, null=True)),
                ('movement_code', models.CharField(blank=True, max_length=250)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('accident_factor', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='incidentreport.accidentcausation')),
                ('accident_subcategory', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='incidentreport.accidentcausationsub')),
                ('collision_subcategory', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='incidentreport.collisiontypesub')),
                ('collision_type', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='incidentreport.collisiontype')),
                ('crash_type', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='incidentreport.crashtype')),
                ('user', models.ForeignKey(blank=True, editable=False, null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='UserReport',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('description', models.TextField(blank=True, max_length=250)),
                ('address', models.CharField(max_length=250)),
                ('country', models.CharField(blank=True, max_length=50, null=True)),
                ('state', models.CharField(blank=True, max_length=250, null=True)),
                ('city', models.CharField(blank=True, max_length=50, null=True)),
                ('pin_code', models.CharField(blank=True, max_length=6, null=True)),
                ('latitude', models.FloatField(blank=True, max_length=20, null=True)),
                ('longitude', models.FloatField(blank=True, max_length=20, null=True)),
                ('upload_photovideo', models.FileField(blank=True, null=True, upload_to='incident_report/image')),
                ('date', models.DateField(blank=True, null=True)),
                ('time', models.TimeField(blank=True, null=True)),
                ('status', models.PositiveSmallIntegerField(blank=True, choices=[(1, 'Pending'), (2, 'Approved'), (3, 'Rejected')], null=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('user', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='IncidentVehicle',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('classification', models.CharField(blank=True, choices=[('Diplomat', 'Diplomat'), ('Government', 'Government'), ('Private', 'Private'), ('Public / For Hire`', 'Public / For Hire`')], max_length=250, null=True)),
                ('vehicle_type', models.CharField(blank=True, choices=[('Ambulance', 'Ambulance'), ('Animal', 'Animal'), ('Armored Car', 'Armored Car'), ('Bicycle', 'Bicycle'), ('Bus', 'Bus'), ('Car', 'Car'), ('Electric Bike', 'Electric Bike'), ('Habal-habal', 'Habal-habal'), ('Heavy Equipment', 'Heavy Equipment'), ('Horse-Driven Carriage (Tartanilla)', 'Horse-Driven Carriage (Tartanilla)'), ('Jeepney', 'Jeepney'), ('Motorcycle', 'Motorcycle'), ('Pedestrian', 'Pedestrian'), ('Pedicab', 'Pedicab'), ('Push-Cart', 'Push-Cart'), ('SUV', 'SUV'), ('Taxi (metered)', 'Taxi (metered)'), ('Tricycle (Articulated)', 'Tricycle (Articulated)'), ('Truck (Fire)', 'Truck (Fire)'), ('Truck (Pick-up)', 'Truck (Pick-up)'), ('Truck (Rigid)', 'Truck (Rigid)'), ('Truck (Unknown)', 'Truck (Unknown)'), ('Van', 'Van'), ('Water Vessel', 'Water Vessel'), ('Others', 'Others')], max_length=250, null=True)),
                ('brand', models.CharField(blank=True, max_length=250)),
                ('plate_number', models.CharField(blank=True, max_length=250)),
                ('engine_number', models.CharField(blank=True, max_length=250)),
                ('chassis_number', models.CharField(blank=True, max_length=250)),
                ('insurance_details', models.TextField(blank=True, max_length=250)),
                ('maneuver', models.CharField(blank=True, choices=[('Left-turn', 'Left-turn'), ('Right-turn', 'Right-turn'), ('U-turn', 'U-turn'), ('Cross Traffic', 'Cross Traffic'), ('Merging', 'Merging'), ('Diverging', 'Diverging'), ('Overtaking', 'Overtaking'), ('Going Ahead', 'Going Ahead'), ('Reversing', 'Reversing'), ('Sudden Start', 'Sudden Start'), ('Sudden Stop', 'Sudden Stop'), ('Parked Off Road', 'Parked Off Road'), ('Parked On Road', 'Parked On Road')], max_length=250, null=True)),
                ('damage', models.CharField(blank=True, choices=[(1, 'None'), (2, 'Front'), (3, 'Left'), (4, 'Multiple'), (5, 'Rear'), (6, 'Right'), (7, 'Roof')], max_length=250, null=True)),
                ('defect', models.CharField(blank=True, choices=[(1, 'None'), (2, 'Breaks'), (3, 'Lights'), (4, 'Multiple'), (5, 'Steering'), (6, 'Tires')], max_length=250, null=True)),
                ('loading', models.CharField(blank=True, choices=[(1, 'Legal'), (2, 'Overloaded'), (3, 'Unsafe Load'), (4, 'Others')], max_length=250, null=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('incident_general', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='incidentreport.incidentgeneral')),
            ],
        ),
        migrations.CreateModel(
            name='IncidentRemark',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('responder', models.CharField(blank=True, max_length=250)),
                ('action_taken', models.TextField(blank=True, max_length=250)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('incident_general', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='incidentreport.incidentgeneral')),
            ],
        ),
        migrations.CreateModel(
            name='IncidentPerson',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('incident_first_name', models.CharField(blank=True, max_length=250)),
                ('incident_middle_name', models.CharField(blank=True, max_length=250)),
                ('incident_last_name', models.CharField(blank=True, max_length=250)),
                ('incident_age', models.CharField(blank=True, max_length=250)),
                ('incident_gender', models.CharField(blank=True, choices=[('Female', 'Female'), ('Male', 'Male')], max_length=250, null=True)),
                ('incident_address', models.CharField(blank=True, max_length=250)),
                ('incident_involvement', models.CharField(blank=True, choices=[('Pedestrian', 'Pedestrian'), ('Witness', 'Witness'), ('Passenger', 'Passenger'), ('Driver', 'Driver')], max_length=250, null=True)),
                ('incident_id_presented', models.CharField(blank=True, choices=[("Driver's License", "Driver's License"), ('Government', 'Government'), ('Passport', 'Passport'), ('School Id', 'School Id'), ('Others', 'Others')], max_length=250, null=True)),
                ('incident_id_number', models.CharField(blank=True, max_length=250)),
                ('incident_injury', models.CharField(blank=True, choices=[('Fatal', 'Fatal'), ('Minor', 'Minor'), ('Not Injured', 'Not Injured'), ('Serious', 'Serious')], max_length=250, null=True)),
                ('incident_driver_error', models.CharField(blank=True, choices=[('Bad Overtaking', 'Bad Overtaking'), ('Bad Turning', 'Bad Turning'), ('Fatigued / Asleep', 'Fatigued / Asleep'), ('Inattentive', 'Inattentive'), ('No Signal', 'No Signal'), ('Too Close', 'Too Close'), ('Too Fast', 'Too Fast'), ('Using Cellphone', 'Using Cellphone')], max_length=250, null=True)),
                ('incident_alcohol_drugs', models.CharField(blank=True, choices=[('Alcohol Suspected', 'Alcohol Suspected'), ('Drugs suspected', 'Drugs suspected')], max_length=250, null=True)),
                ('incident_seatbelt_helmet', models.CharField(blank=True, choices=[('Seat belt/Helmet Worn', 'Seat belt/Helmet Worn'), ('Not worn', 'Not worn'), ('Not worn correctly', 'Not worn correctly')], max_length=250, null=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('incident_general', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='incidentreport.incidentgeneral')),
            ],
        ),
        migrations.CreateModel(
            name='IncidentMedia',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('media_description', models.TextField(blank=True, max_length=250)),
                ('incident_upload_photovideo', models.ImageField(default='user.jpeg', upload_to='incident_report/image')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('incident_general', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='incidentreport.incidentgeneral')),
            ],
        ),
        migrations.AddField(
            model_name='incidentgeneral',
            name='user_report',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='incidentreport.userreport'),
        ),
        migrations.CreateModel(
            name='Incident',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('modified_at', models.DateTimeField(auto_now=True)),
                ('incident_general', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='incidentreport.incidentgeneral')),
                ('incident_media', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='incidentreport.incidentmedia')),
                ('incident_person', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='incidentreport.incidentperson')),
                ('incident_remark', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='incidentreport.incidentremark')),
                ('incident_vehicle', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='incidentreport.incidentvehicle')),
                ('user_report', models.OneToOneField(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='incidentreport.userreport')),
            ],
        ),
    ]
