from django import forms
from .models import User, UserProfile
from django.core.validators import RegexValidator, MinLengthValidator

class DateInput(forms.DateInput):
    input_type = 'date'
    

class UserForm(forms.ModelForm):
    first_name = forms.CharField(widget=forms.TextInput(attrs={'placeholder': 'Jones', 'style': 'width: 150px; '}))
    middle_name = forms.CharField(widget=forms.TextInput(attrs={'placeholder': 'A', 'style': 'width: 150px; '}))
    last_name = forms.CharField(widget=forms.TextInput(attrs={'placeholder': 'Smith', 'style': 'width: 150px; '}))
    mobile_number = forms.CharField(max_length=15, validators=[RegexValidator(
        '^\+[0-9]{1,3}\.?\s?\d{8,13}', message="Phone number must not consist of space and requires country code. eg : +639171234567")],widget=forms.TextInput(attrs={'placeholder': '09123456789', 'style': 'width: 305px; '}),
                                    error_messages={'unique': ("Mobile Number already exists.")})
    
    email = forms.CharField(widget=forms.TextInput(attrs={'placeholder': 'jonesmith@gmail.com', 'style': 'width: 460px; '}),
                            error_messages={'unique': ("Email already exists.")},)
    username = forms.CharField(widget=forms.TextInput(attrs={'placeholder': 'Jones_Smith31', 'style': 'width: 460px; '}),
                               error_messages={'unique': ("Username already exists.")},)
    password = forms.CharField(widget=forms.PasswordInput(attrs={'placeholder': '********', 'style': 'width: 460px; '}))
    #password = forms.CharField(validators=[MinLengthValidator(8),RegexValidator('^(?=.*[A-Z])(?=.*[!@#$&*])(?=.*[0-9])(?=.*[a-z])$', message="Password should be a combination of Alphabets and Numbers")], widget=forms.PasswordInput(attrs={'placeholder': '********', 'style': 'width: 460px; '}))
    confirm_password = forms.CharField(widget=forms.PasswordInput(attrs={'placeholder': '********', 'style': 'width: 460px;' }))
    class Meta:
        model = User
        fields = ['first_name', 'middle_name', 'last_name', 'username', 'email', 'mobile_number', 'password']
        
    
        
    def clean(self):
        clean_data = super(UserForm, self).clean()
        password = clean_data.get('password')
        confirm_password = clean_data.get('confirm_password')
        
        
        
        if password != confirm_password:
            raise forms.ValidationError(
                "Password and Confirm Password does not match!"
            )
    
    def save(self):
        self.clean()
        user = self.Meta.model(
            username = self.cleaned_data['username'], 
            email = self.cleaned_data['email'], 
        )
        user.set_password(self.cleaned_data['password2'])
        user.save()
        return user

class MemberForm(forms.ModelForm):
    birthdate = forms.DateField(widget=DateInput)
    class Meta:
        model = UserProfile
        fields = ['birthdate', 'upload_id']

class UserManagementForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['first_name', 'middle_name', 'last_name', 'username', 'email', 'mobile_number', 'password']


    first_name = forms.CharField(widget=forms.TextInput(attrs={'placeholder': 'Jones', 'class': 'form-control ', }))
    middle_name = forms.CharField(widget=forms.TextInput(attrs={'placeholder': 'A', 'class': 'form-control', }))
    last_name = forms.CharField(widget=forms.TextInput(attrs={'placeholder': 'Smith', 'class': 'form-control',}))
    mobile_number = forms.CharField(max_length=15, validators=[RegexValidator(
        '^\+[0-9]{1,3}\.?\s?\d{8,13}', message="Phone number must not consist of space and requires country code. eg : +639171234567")],widget=forms.TextInput(attrs={'placeholder': '09123456789', 'class': 'form-control',}),
                                    error_messages={'unique': ("Mobile Number already exists.")})
    
    email = forms.CharField(widget=forms.TextInput(attrs={'placeholder': 'jonesmith@gmail.com', 'class': 'form-control',}),
                            error_messages={'unique': ("Email already exists.")},)
    username = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control',}),
                               error_messages={'unique': ("Username already exists.")},)
    password = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-control',}))
    #password = forms.CharField(validators=[MinLengthValidator(8),RegexValidator('^(?=.*[A-Z])(?=.*[!@#$&*])(?=.*[0-9])(?=.*[a-z])$', message="Password should be a combination of Alphabets and Numbers")], widget=forms.PasswordInput(attrs={'placeholder': '********', 'style': 'width: 460px; '}))
    confirm_password = forms.CharField(widget=forms.PasswordInput(attrs={'placeholder': '********', 'class': 'form-control', }))
   
        
        
    def clean(self):
        clean_data = super(UserManagementForm, self).clean()
        password = clean_data.get('password')
        confirm_password = clean_data.get('confirm_password')
        
        
        
        if password != confirm_password:
            raise forms.ValidationError(
                "Password and Confirm Password does not match!"
            )

