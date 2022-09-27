from django.db import models
from accounts.models import User

# Create your models here.
class UserReport(models.Model):
    PENDING = 1
    APPROVED = 2
    REJECTED = 3
    STATUS = (
        (PENDING, 'Pending'),
        (APPROVED, 'Approved'),
        (REJECTED, 'Rejected')
    )
    user = models.ForeignKey(User, on_delete=models.CASCADE)
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
