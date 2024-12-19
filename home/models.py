from distutils.command.upload import upload
import imp
from tkinter import CASCADE
from django.db import models
from django.contrib.auth.models import User
from account.models import *
# Create your models herecd .
class Category(models.Model):
    name_cat=models.CharField(max_length=50)
    img_cat=models.ImageField(upload_to="media")
    desc_cat=models.TextField()
    updated_on=models.DateTimeField(auto_now=True)
    def __str__(self):
        return self.name_cat
class repair_centre(models.Model):
    profile=models.ForeignKey(profile,on_delete=models.CASCADE)
    usr=models.ForeignKey(User,on_delete=models.CASCADE)
    cate=models.ForeignKey(Category,default=1,on_delete=models.CASCADE)
    img_re=models.ImageField(upload_to="media",default="default\julb.jpg")
    name_re=models.CharField(max_length=60)
    desc_rer=models.TextField()
    updated_on=models.DateTimeField(auto_now=True)
    def __str__(self):
        return self.name_re 

class Service(models.Model):
    rep=models.ForeignKey(repair_centre,default=1,on_delete=models.CASCADE)
    name_ser=models.CharField(max_length=60)
    desc_ser=models.TextField()
    img_ser=models.ImageField(upload_to="media",default="default\default_imgpro.jpg")
    price_ser=models.IntegerField()
    updated_on=models.DateTimeField(auto_now=True)
    def __str__(self):
        return self.name_ser
class addservices(models.Model):
    adserv=models.ForeignKey(repair_centre,default=1,on_delete=models.CASCADE)
    adcat=models.ForeignKey(Category,default=1,on_delete=models.CASCADE)
    img_addserv=models.ImageField(upload_to="media",default="default\default_imgpro.jpg")
    name_serv=models.CharField(max_length=40)
    desc_serv=models.TextField()
    price_serv=models.IntegerField()
    updated_on=models.DateTimeField(auto_now=True)
    def __str__(self):
        return self.name_serv
class repprofile(models.Model):
    rest=models.ForeignKey(repair_centre, on_delete=models.CASCADE)
    overview=models.CharField(max_length=100)
    about=models.CharField(max_length=1000)
    localty=models.CharField(max_length=30)
    timings=models.CharField(max_length=30)
    costEstimate=models.CharField(max_length=30)
    contact=models.CharField(max_length=25)
    img1=models.ImageField(upload_to="media/restro",default='default/default restaurant.jpg')
    img2=models.ImageField(upload_to="media/restro",default='default/default restaurant.jpg')
    img3=models.ImageField(upload_to="media/restro",default='default/default restaurant.jpg')
    updated_on=models.DateTimeField(auto_now=True,null=True) 
    map=models.URLField(default="https://www.google.com/maps/embed?pb=!1m18!1m12!1m3!1d227822.55035627162!2d80.8024271802209!3d26.84862299412667!2m3!1f0!2f0!3f0!3m2!1i1024!2i768!4f13.1!3m3!1m2!1s0x399bfd991f32b16b%3A0x93ccba8909978be7!2sLucknow%2C%20Uttar%20Pradesh!5e0!3m2!1sen!2sin!4v1652175194751!5m2!1sen!2sin")

class cart(models.Model):
    usr=models.ForeignKey(User,on_delete=models.CASCADE)
    quantity=models.IntegerField()
    status=models.BooleanField(default=False)
    service=models.ForeignKey(Service,on_delete=models.CASCADE)
    added_on=models.DateTimeField(auto_now_add=True,null=True)
    update_on=models.DateTimeField(auto_now=True,null=True)
    def __str__(self):
        return self.usr.username
class Order(models.Model):
    cust_id = models.ForeignKey(User,on_delete=models.CASCADE)
    cart_ids = models.CharField(max_length=250)
    product_ids = models.CharField(max_length=250)
    invoice_id = models.CharField(max_length=250)
    status = models.BooleanField(default=False)
    processed_on = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.cust_id.username
class contact(models.Model):
    usr=models.ForeignKey(User,on_delete=models.CASCADE)
    phone=models.BigIntegerField()
    msg=models.TextField()
    addon=models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return self.usr.username  
class feedback(models.Model):
    usr=models.ForeignKey(User,on_delete=models.CASCADE)
    title=models.CharField(max_length=50)
    revbody=models.TextField()
    addon=models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return self.usr.username  

class bookingdetails(models.Model):
    usr=models.ForeignKey(User,on_delete=models.CASCADE)
    cartdetails=models.ForeignKey(cart,default=1,on_delete=models.CASCADE)
    servicename=models.CharField(max_length=40)
    modelname=models.CharField(max_length=40)
    prob_desc=models.TextField()
    date_desc=models.CharField(max_length=40)
    def __str__(self):
        return self.usr.username
class billingdetails(models.Model):
    usr=models.ForeignKey(User,on_delete=models.CASCADE)
    fname=models.CharField(max_length=40)
    lname=models.CharField(max_length=40)
    email=models.CharField(max_length=40)
    state=models.TextField()
    city=models.TextField()
    street=models.TextField()
    ph_pro=models.BigIntegerField()
    det=models.TextField(max_length=80)
    def __str__(self):
        return self.usr.username
class Review(models.Model):
    repcentre = models.ForeignKey(repair_centre, on_delete=models.CASCADE)
    usr = models.ForeignKey(User, on_delete=models.CASCADE, default="")
    subject = models.CharField(max_length=50)
    review = models.CharField(max_length=200)
    rating = models.IntegerField()
    created_at = models.DateTimeField(auto_now_add=True)
    def __str__(self):
        return self.repcentre.re_name + " by " + self.user.first_name
        
