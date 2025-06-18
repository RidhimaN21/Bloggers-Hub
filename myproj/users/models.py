from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils.translation import gettext_lazy as _
from django.conf import settings


# Create your models here.
class EmailOTP(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL,on_delete=models.CASCADE,verbose_name=_("User"))
    otp = models.CharField(_("otp"),max_length=6)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username} - {self.otp}"
    
class UserProfile(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL,on_delete=models.CASCADE,verbose_name=_("User"))
    alternate_email = models.EmailField(_("alternate_email"),blank=True,null=True)

    def __str__(self):
        return self.user.username

class User(AbstractUser):
    backup_token = models.CharField( max_length=6 )













    