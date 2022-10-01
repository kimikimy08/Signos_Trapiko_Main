import datetime
from django import forms
from .models import UserReport, Incident, IncidentGeneral, AccidentCausationSub, CollisionTypeSub
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
                self.fields['accident_subcategory'].queryset = AccidentCausationSub.objects.filter(accident_factor_id=accident_factor_id).order_by('name')
            except (ValueError, TypeError):
                pass  # invalid input from the client; ignore and fallback to empty City queryset
        elif self.instance.pk:
            self.fields['accident_subcategory'].queryset = self.instance.accident_factor.accident_subcategory_set.order_by('name')
            
        if 'collision_type' in self.data:
            try:
                collision_type_id = int(self.data.get('collision_type'))
                self.fields['collision_subcategory'].queryset = CollisionTypeSub.objects.filter(collision_type_id=collision_type_id).order_by('name')
            except (ValueError, TypeError):
                pass  # invalid input from the client; ignore and fallback to empty City queryset
        elif self.instance.pk:
            self.fields['collision_subcategory'].queryset = self.instance.collision_type.collision_subcategory_set.order_by('name')
