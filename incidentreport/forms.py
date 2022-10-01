import datetime
from django import forms
from .models import UserReport, Incident, IncidentGeneral, AccidentCausationSub, CollisionTypeSub, IncidentPerson, IncidentVehicle, IncidentRemark, IncidentMedia
#from .validators import allow_only_images_validator


class DateInput(forms.DateInput):
    input_type = 'date'


class TimeInput(forms.TimeInput):
    input_type = 'time'


class UserReportForm(forms.ModelForm):
    date = forms.DateField(widget=DateInput(
        attrs={'class': 'form-control'}), initial=datetime.datetime.now())
    upload_photovideo = forms.FileField(
        widget=forms.FileInput(attrs={'class': 'form-control p-1'}))
    time = forms.TimeField(widget=TimeInput(
        attrs={'class': 'form-control'}), initial=datetime.datetime.now())
    location = forms.CharField(widget=forms.TextInput(
        attrs={'placeholder': 'Start typing...', 'required': 'required', 'class': 'form-control'}))
    description = forms.CharField(widget=forms.Textarea(
        attrs={'area': '3', 'class': 'form-control'}))

    # latitude = forms.CharField(widget=forms.TextInput(attrs={'readonly': 'readonly'}))
    # longitude = forms.CharField(widget=forms.TextInput(attrs={'readonly': 'readonly'}))
    class Meta:
        model = UserReport
        fields = ['location', 'description', 'upload_photovideo']

    def __init__(self, *args, **kwargs):
        # first call parent's constructor
        super(UserReportForm, self).__init__(*args, **kwargs)
        # there's a `fields` property now
        self.fields['upload_photovideo'].required = False
        self.fields['location'].widget.attrs['class'] = 'form-control'

    # def __init__(self, *args, **kwargs):
    #     super(UserReportForm, self).__init__(*args, **kwargs)
        # for field in self.fields:
        #     if field == 'latitude' or field == 'longitude':
        #         self.fields[field].widget.attrs['readonly'] = 'readonly'


class IncidentGeneralForm(forms.ModelForm):
    class Meta:
        model = IncidentGeneral
        fields = '__all__'

    # weather = forms.CharField(widget=forms.Select(
    #     choices=WEATHER_CHOICE, attrs={'class': 'form-control', }))
    # light = forms.CharField(widget=forms.Select(
    #     choices=LIGHT_CHOICE, attrs={'class': 'form-control', }))
    # severity = forms.CharField(widget=forms.Select(
    #     choices=SEVERITY_CHOICE, attrs={'class': 'form-control', }))

    def __init__(self, *args, **kwargs):
        super(IncidentGeneralForm, self).__init__(*args, **kwargs)
        self.fields['accident_factor'].widget.attrs['class'] = 'form-control'
        self.fields['accident_subcategory'].widget.attrs['class'] = 'form-control'
        self.fields['collision_type'].widget.attrs['class'] = 'form-control'
        self.fields['collision_subcategory'].widget.attrs['class'] = 'form-control'
        self.fields['weather'].widget.attrs['class'] = 'form-control'
        self.fields['light'].widget.attrs['class'] = 'form-control'
        self.fields['severity'].widget.attrs['class'] = 'form-control'
        self.fields['crash_type'].widget.attrs['class'] = 'form-control'
        self.fields['movement_code'].widget.attrs['class'] = 'form-control'
        
        self.fields['accident_subcategory'].queryset = AccidentCausationSub.objects.none()
        self.fields['collision_subcategory'].queryset = CollisionTypeSub.objects.none()

        if 'accident_factor' in self.data:
            try:
                accident_factor_id = int(self.data.get('accident_factor'))
                self.fields['accident_subcategory'].queryset = AccidentCausationSub.objects.filter(accident_factor_id=accident_factor_id).order_by('accident_factor')
            except (ValueError, TypeError):
                pass  # invalid input from the client; ignore and fallback to empty City queryset
        elif self.instance.pk:
            self.fields['accident_subcategory'].queryset = self.instance.accident_factor.accident_subcategory_set.order_by('subcategory')
            
        if 'collision_type' in self.data:
            try:
                collision_type_id = int(self.data.get('collision_type'))
                self.fields['collision_subcategory'].queryset = CollisionTypeSub.objects.filter(collision_type_id=collision_type_id).order_by('collision_type')
            except (ValueError, TypeError):
                pass  # invalid input from the client; ignore and fallback to empty City queryset
        elif self.instance.pk:
            self.fields['collision_subcategory'].queryset = self.instance.collision_type.collision_subcategory_set.order_by('subcategory')


class IncidentPersonForm(forms.ModelForm):
    class Meta:
        model = IncidentPerson
        fields = '__all__'

    def __init__(self, *args, **kwargs):
        super(IncidentPersonForm, self).__init__(*args, **kwargs)
        self.fields['incident_first_name'].widget.attrs['class'] = 'form-control'
        self.fields['incident_middle_name'].widget.attrs['class'] = 'form-control'
        self.fields['incident_last_name'].widget.attrs['class'] = 'form-control'
        self.fields['incident_age'].widget.attrs['class'] = 'form-control'
        self.fields['incident_gender'].widget.attrs['class'] = 'form-control'
        self.fields['incident_address'].widget.attrs['class'] = 'form-control'
        self.fields['incident_involvement'].widget.attrs['class'] = 'form-control'
        self.fields['incident_id_presented'].widget.attrs['class'] = 'form-control'
        self.fields['incident_id_number'].widget.attrs['class'] = 'form-control'
        self.fields['incident_injury'].widget.attrs['class'] = 'form-control'
        self.fields['incident_driver_error'].widget.attrs['class'] = 'form-control'
        self.fields['incident_alcohol_drugs'].widget.attrs['class'] = 'form-control'
        self.fields['incident_seatbelt_helmet'].widget.attrs['class'] = 'form-control'
        
class IncidentVehicleForm(forms.ModelForm):
    class Meta:
        model = IncidentVehicle
        fields = '__all__'

    def __init__(self, *args, **kwargs):
        super(IncidentVehicleForm, self).__init__(*args, **kwargs)
        self.fields['classification'].widget.attrs['class'] = 'form-control'
        self.fields['vehicle_type'].widget.attrs['class'] = 'form-control'
        self.fields['brand'].widget.attrs['class'] = 'form-control'
        self.fields['plate_number'].widget.attrs['class'] = 'form-control'
        self.fields['engine_number'].widget.attrs['class'] = 'form-control'
        self.fields['chassis_number'].widget.attrs['class'] = 'form-control'
        self.fields['insurance_details'].widget.attrs['class'] = 'form-control'
        self.fields['maneuver'].widget.attrs['class'] = 'form-control'
        self.fields['damage'].widget.attrs['class'] = 'form-control'
        self.fields['defect'].widget.attrs['class'] = 'form-control'
        self.fields['loading'].widget.attrs['class'] = 'form-control'

class IncidentMediaForm(forms.ModelForm):
    class Meta:
        model = IncidentMedia
        fields = '__all__'

    def __init__(self, *args, **kwargs):
        super(IncidentMediaForm, self).__init__(*args, **kwargs)
        self.fields['description'].widget.attrs['class'] = 'form-control'
        self.fields['incident_upload_photovideo'].widget.attrs['class'] = 'form-control'


class IncidentRemarksForm(forms.ModelForm):
    class Meta:
        model = IncidentRemark
        fields = '__all__'

    def __init__(self, *args, **kwargs):
        super(IncidentRemarksForm, self).__init__(*args, **kwargs)
        self.fields['responder'].widget.attrs['class'] = 'form-control'
        self.fields['action_taken'].widget.attrs['class'] = 'form-control'
     