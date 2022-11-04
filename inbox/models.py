from django.db import models
from ckeditor.fields import RichTextField
from accounts.managers import SoftDeleteManager
from django.utils import timezone
from accounts.models import User
# Create your models here.

class SoftDeleteModel(models.Model):
    is_deleted = models.BooleanField(default=False)
    deleted_at = models.DateTimeField(null=True, blank=True, default=None)
    objects = SoftDeleteManager()
    all_objects = models.Manager()

    def soft_delete(self):
        self.is_deleted = True
        self.deleted_at = timezone.now()
        self.save()

    def restore(self):
        self.is_deleted = False
        self.deleted_at = None
        self.save()

    class Meta:
        abstract = True

class Sent(SoftDeleteModel):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    to_email = models.EmailField(max_length=100, unique=False)
    subject = models.CharField(max_length=250)
    message = RichTextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return self.subject + ' | ' + str(self.user)
    
    