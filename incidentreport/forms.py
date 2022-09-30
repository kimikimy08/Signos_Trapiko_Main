import datetime
from django import forms
from .models import UserReport, IncidentGeneral
#from .validators import allow_only_images_validator

class DateInput(forms.DateInput):
    input_type = 'date'
    
class TimeInput(forms.TimeInput):
    input_type = 'time'

class UserReportForm(forms.ModelForm):
    date = forms.DateField(widget=DateInput(attrs={'class': 'form-control'}), initial=datetime.datetime.now())
    upload_photovideo = forms.FileField(widget=forms.FileInput(attrs={'class': 'form-control p-1'} ) )
    time = forms.TimeField(widget=TimeInput(attrs={'class': 'form-control'}), initial=datetime.datetime.now())
    location = forms.CharField(widget=forms.TextInput(attrs={'placeholder': 'Start typing...', 'required': 'required', 'class': 'form-control'}))
    description = forms.CharField(widget=forms.Textarea(attrs={'area': '3', 'class': 'form-control'}))
    
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

    # def __init__(self, *args, **kwargs):
    #     super(UserReportForm, self).__init__(*args, **kwargs)
        # for field in self.fields:
        #     if field == 'latitude' or field == 'longitude':
        #         self.fields[field].widget.attrs['readonly'] = 'readonly'

class IncidentGeneralForm(forms.ModelForm):
    class Meta:
        model = IncidentGeneral
        fields = ['accident_factor', 'collision_type', 'crash_type', 'weather', 'light', 'severity', 'movement_code']

    WEATHER_CHOICE = (
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
    
    LIGHT_CHOICE = (
        (1, 'Dawn'),
        (2, 'Day'),
        (3, 'Dusk'),
        (4, 'Night'),
    )
    
    SEVERITY_CHOICE = (
        (1, 'Damage to Property'),
        (2, 'Fatal'),
        (3, 'Non-Fatal'),
    )
    
    weather = forms.CharField(widget=forms.Select(choices=WEATHER_CHOICE, attrs={ 'class': 'form-control', }))
    light = forms.CharField(widget=forms.Select(choices=LIGHT_CHOICE, attrs={ 'class': 'form-control', }))
    severity = forms.CharField(widget=forms.Select(choices=SEVERITY_CHOICE, attrs={ 'class': 'form-control', }))

    def __init__(self, *args, **kwargs):
        super(IncidentGeneralForm, self).__init__(*args, **kwargs)