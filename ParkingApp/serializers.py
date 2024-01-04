from rest_framework import serializers
from .models import ParkOwner, Users, Park, ParkDetails, Floor, ParkingSlot, ParkingSlotRules, Booking, Credentials

class ParkOwnerSerializer(serializers.ModelSerializer):
    class Meta:
        model = ParkOwner
        fields = '__all__'

class UsersSerializer(serializers.ModelSerializer):
    class Meta:
        model = Users
        fields = '__all__'
        
class CredentialsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Credentials
        fields = '__all__'

class ParkSerializer(serializers.ModelSerializer):
    class Meta:
        model = Park
        fields = '__all__'
        
class ParkDetailsSerializer(serializers.ModelSerializer):
    class Meta:
        model = ParkDetails
        fields = '__all__'
        
class FloorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Floor
        fields = '__all__'
        
class ParkingSlotSerializer(serializers.ModelSerializer):
    class Meta:
        model = ParkingSlot
        fields = '__all__'
        
class ParkingSlotRulesSerializer(serializers.ModelSerializer):
    class Meta:
        model = ParkingSlotRules
        fields = '__all__'
        
class BookingSerializer(serializers.ModelSerializer):
    class Meta:
        model = Booking
        fields = '__all__'

