import datetime
from django import forms
from .models import UserReport
#from .validators import allow_only_images_validator

class DateInput(forms.DateInput):
    input_type = 'date'
    
class TimeInput(forms.TimeInput):
    input_type = 'time'

class UserReportForm(forms.ModelForm):
    date = forms.DateField(widget=DateInput(attrs={'class': 'form-control'}), initial=datetime.datetime.now())
    upload_photovideo = forms.FileField(widget=forms.FileInput(attrs={'class': 'form-control p-1'}))
    time = forms.TimeField(widget=TimeInput(attrs={'class': 'form-control'}), initial=datetime.datetime.now())
    location = forms.CharField(widget=forms.TextInput(attrs={'placeholder': 'Start typing...', 'required': 'required', 'class': 'form-control'}))
    description = forms.CharField(widget=forms.Textarea(attrs={'area': '3', 'class': 'form-control'}))
    
    # latitude = forms.CharField(widget=forms.TextInput(attrs={'readonly': 'readonly'}))
    # longitude = forms.CharField(widget=forms.TextInput(attrs={'readonly': 'readonly'}))
    class Meta:
        model = UserReport
        fields = ['location', 'description', 'upload_photovideo']

    # def __init__(self, *args, **kwargs):
    #     super(UserReportForm, self).__init__(*args, **kwargs)
        # for field in self.fields:
        #     if field == 'latitude' or field == 'longitude':
        #         self.fields[field].widget.attrs['readonly'] = 'readonly'

