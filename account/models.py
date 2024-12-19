from django.db import models
from django.contrib.auth.models import User
# Create your models here.
class profile(models.Model):
    usr=models.ForeignKey(User,on_delete=models.CASCADE)
    img_pro=models.ImageField(upload_to="media",default="default\default_imgpro.jpg")
    state=models.TextField(default="Not Available")
    city=models.TextField(default="Not Available")
    street=models.TextField(default="Not Available")
    ph_pro=models.BigIntegerField(default="123456789")
    updated_on=models.DateTimeField(auto_now=True)
    def __str__(self):
        return self.usr.username
