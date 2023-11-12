from django.contrib import admin
from .models import *
# Register your models here.

admin.site.register(ParkOwner) 
admin.site.register(Credentials) 
admin.site.register(Users)
admin.site.register(Park)
admin.site.register(ParkDetails)
admin.site.register(Floor)
admin.site.register(ParkingSlot)
admin.site.register(ParkingSlotRules)
admin.site.register(Booking)       