

from django.conf import settings
from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager
from django.db.models.fields.related import ForeignKey, OneToOneField
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.core.validators import RegexValidator, MinLengthValidator
from PIL import Image
# Create your models here.

class UserManager(BaseUserManager):
    def create_user(self, first_name, middle_name, last_name, username, email, mobile_number, password=None):
        if not email:
            raise ValueError('User must have an email address')
        
        if not username:
            raise ValueError('User must have an username')
        
        if not mobile_number:
            raise ValueError('User must have a mobile number')
        
        user = self.model(
            email = self.normalize_email(email), #lowercase email
            username = username,
            first_name = first_name,
            middle_name = middle_name,
            last_name = last_name,
            mobile_number = mobile_number,
        )
        user.set_password(password)
        user.save(using=self.db) 
        return user
    
    def create_superuser(self, first_name, middle_name, last_name, username, email, mobile_number, password=None):
        user = self.create_user(
            email = self.normalize_email(email), #lowercase email
            username = username,
            password = password,
            first_name = first_name,
            middle_name = middle_name,
            last_name = last_name,
            mobile_number = mobile_number,
        )
        user.is_admin = True
        user.is_active = True
        user.is_staff = True
        user.is_superadmin = True
        user.save(using=self.db)
        return user
        

class User(AbstractBaseUser):
    MEMBER = 1
    ADMIN = 2
    SUPERADMIN = 3
    ROLE_CHOICE = (
        (MEMBER, 'Member'),
        (ADMIN, 'Admin'),
        (SUPERADMIN, 'Super Admin')
    )
    
    ACTIVE = 1
    DELETED = 2
    DEACTIVATED = 3
    
    STATUS = (
        (ACTIVE, 'Active'),
        (DELETED, 'Deleted'),
        (DEACTIVATED, 'Deactivated')
    )
    
    first_name = models.CharField(max_length=50)
    middle_name = models.CharField(max_length=50, default="Some String")
    last_name = models.CharField(max_length=50)
    username = models.CharField(max_length=50, unique=True)
    email = models.EmailField(max_length=100, unique=True)
    mobile_number = models.CharField(max_length = 100, db_index=True, null = True, validators=[
        
            RegexValidator(
                regex='^(\+\d{1,3})?,?\s?\d{8,13}',
                message='Phone number must not consist of space and requires country code. eg : +639171234567',
            ),
        ])
    password = models.CharField(max_length = 100,validators=[MinLengthValidator(8),
            
        ])
    role = models.PositiveSmallIntegerField(choices=ROLE_CHOICE, blank=True, null=True)
    status = models.PositiveSmallIntegerField(choices=STATUS, blank=True, null=True)
    
    # required fields
    date_joined = models.DateTimeField(auto_now_add=True)
    last_login = models.DateTimeField(auto_now_add=True)
    created_date= models.DateTimeField(auto_now_add=True)
    modified_date = models.DateTimeField(auto_now_add=True)
    is_admin = models.BooleanField(default=False)
    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=False)
    is_superadmin = models.BooleanField(default=False)
    
    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ['email', 'first_name', 'middle_name', 'last_name', 'mobile_number']
    
    objects = UserManager()
    
    def __str__(self):
        return self.username
    
    def has_perm(self, perm, obj=None):
        return self.is_admin
    
    def has_module_perms(self, app_label):
        return True
    
    def get_role(self):
        if self.role == 1:
            user_role = 'Member'
        elif self.role == 2:
            user_role = 'Admin'
        elif self.role == 3:
            user_role = 'Super Admin'
        return user_role
    
    def get_status(self):
        if self.status == 1:
            user_status = 'Active'
        elif self.status == 2:
            user_status = 'Deleted'
        elif self.status == 3:
            user_status = 'Deactivated'
        return user_status

class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True)
    birthdate = models.DateField(blank=True, null=True)
    profile_picture = models.ImageField(default='user.jpeg', upload_to='users/profile_pictures')
    upload_id = models.ImageField(default='user.jpeg', upload_to='member/id')
    created_at = models.DateTimeField(auto_now=True)
    modified_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.user.username
    
    

@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        UserProfile.objects.get_or_create(user=instance)
  
post_save.connect(create_user_profile, sender=User) 


