from django.db import models

class ParkOwner(models.Model):
    park_owner_id = models.AutoField(primary_key=True)
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    email = models.EmailField(unique=False)
    password = models.CharField(max_length=100)  
    
    def __str__(self):
        return f"{self.first_name} {self.last_name}"
    
    class Meta:
        db_table = 'ParkOwner'

class Park(models.Model):
    park_id = models.AutoField(primary_key=True)
    park_owner = models.OneToOneField(ParkOwner, on_delete=models.CASCADE)
    total_spots = models.IntegerField()
    no_floors = models.IntegerField()
    park_details = models.OneToOneField('ParkDetails', on_delete=models.CASCADE)

    def __str__(self):
        return f"Park {self.park_id} - Owned by {self.park_owner}"
    
    class Meta:
        db_table = 'Park'

class ParkDetails(models.Model):
    park_details_id = models.AutoField(primary_key=True)
    address = models.CharField(max_length=255)
    latitude = models.DecimalField(max_digits=9, decimal_places=6)
    longitude = models.DecimalField(max_digits=9, decimal_places=6)
    height_limit = models.IntegerField(default=2)
    weigh_limit = models.IntegerField(default=3500)

    def __str__(self):
        return f"Details for Park with address: {self.address}"
    
    class Meta:
        db_table = 'ParkingDetails'

class Credentials(models.Model):
    credentials_id = models.AutoField(primary_key=True)
    email = models.EmailField(unique=False)
    password = models.CharField(max_length=100)  # Use Django's authentication system for passwords

    def __str__(self):
        return f"Credentials {self.credentials_id} - {self.email}"
    
    class Meta:
        db_table = 'Credentials'
    
class Users(models.Model):
    user_id = models.AutoField(primary_key=True)
    credentials = models.OneToOneField('Credentials', on_delete=models.CASCADE)
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    number_plate = models.CharField(max_length=100)
    vehicle_type = models.CharField(max_length=200)
    verified = models.BooleanField()
    
    def __str__(self):
        return f"User: {self.first_name} {self.last_name}"
    
    class Meta:
        db_table = 'Users'
    
class Floor(models.Model):
    floor_id = models.AutoField(primary_key=True)
    park = models.ForeignKey('Park', on_delete=models.CASCADE)
    floor_number = models.IntegerField()
    
    def __str__(self):
        return f"Floor {self.floor_number}"
    
    class Meta:
        db_table = 'Floor'
        
class ParkingSlot(models.Model):
    parking_slot_id = models.AutoField(primary_key=True)
    floor = models.ForeignKey('Floor', on_delete=models.CASCADE)
    slot_number = models.IntegerField()
    has_charger = models.BooleanField()
    physical_available = models.BooleanField(default=False)
    standard_price = models.IntegerField(default=10) 
    
    def __str__(self):
        return f"ParkingSlot {self.slot_number} with id: {self.parking_slot_id} on floor: {self.floor.floor_number}"
    
class ParkingSlotRules(models.Model):
    parking_slot_rules_id = models.AutoField(primary_key=True)
    parking_slot = models.ForeignKey('ParkingSlot', on_delete=models.CASCADE)
    date_start_rule = models.DateTimeField()
    date_end_rule = models.DateTimeField()
    price = models.FloatField()
    
    def __str__(self):
        return f"Rules starting at {self.date_start_rule} and ending at {self.date_end_rule} with price {self.price}"

    class Meta:
        db_table = 'ParkingSlotRules'

class Booking(models.Model):
    booking_id = models.AutoField(primary_key=True)
    parking_slot = models.ForeignKey('ParkingSlot', on_delete=models.CASCADE)
    user = models.ForeignKey('Users', on_delete=models.CASCADE)
    booking_start_date = models.DateTimeField()
    booking_end_date = models.DateTimeField()
    price = models.FloatField()
    # modified = models.BooleanField(default=False)    
    
    # def __str__(self):
    #     return f"Booking starting at {self.date_start_rule} and ending at {self.date_end_rule} with price {self.price} in slot: {self.parking_slot}"
    
    class Meta:
        db_table = 'Booking'
        unique_together = []
    

    
    
    
    