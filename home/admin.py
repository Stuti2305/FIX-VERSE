from django.contrib import admin
from home.models import *
# Register your models here.
admin.site.register(Category)
admin.site.register(repair_centre)
admin.site.register(Service)
admin.site.register(contact)
admin.site.register(cart)
admin.site.register(bookingdetails)
admin.site.register(billingdetails)
admin.site.register(addservices)
admin.site.register(Order)
admin.site.register(feedback)

