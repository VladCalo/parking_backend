# views.py
from rest_framework.response import Response
from django.shortcuts import get_object_or_404
from django.db import transaction
from rest_framework import status
from django.db.models import Q
from django.utils import timezone
from datetime import datetime
from rest_framework import viewsets
from .models import ParkOwner, Users, Credentials, Park, ParkDetails, Floor, ParkingSlot, ParkingSlotRules, Booking
from .serializers import ParkOwnerSerializer, UsersSerializer, CredentialsSerializer, ParkSerializer, ParkDetailsSerializer, FloorSerializer, ParkingSlotSerializer, ParkingSlotRulesSerializer, BookingSerializer

class ParkOwnerViewSet(viewsets.ModelViewSet):
    queryset = ParkOwner.objects.all()
    serializer_class = ParkOwnerSerializer

class UsersViewSet(viewsets.ModelViewSet):
    queryset = Users.objects.all()
    serializer_class = UsersSerializer
    
class CredentialsViewSet(viewsets.ModelViewSet):
    queryset = Credentials.objects.all()
    serializer_class = CredentialsSerializer

class ParkViewSet(viewsets.ModelViewSet):
    queryset = Park.objects.all()
    serializer_class = ParkSerializer

class ParkDetailsViewSet(viewsets.ModelViewSet):
    queryset = ParkDetails.objects.all()
    serializer_class = ParkDetailsSerializer

class FloorViewSet(viewsets.ModelViewSet):
    queryset = Floor.objects.all()
    serializer_class = FloorSerializer
    
class ParkingSlotViewSet(viewsets.ModelViewSet):
    queryset = ParkingSlot.objects.all()
    serializer_class = ParkingSlotSerializer
    
    def list_all(self, request, *args, **kwargs):
        queryset = ParkingSlot.objects.all()
        serializer = ParkingSlotSerializer(queryset, many=True)
        return Response(serializer.data)
    
    def list_available(self, request, *args, **kwargs):
       # Get the current date and time
        current_datetime = timezone.now()
        print(current_datetime)

        # Check for active bookings
        active_bookings = Booking.objects.filter(
            Q(booking_start_date__lte=current_datetime, booking_end_date__gt=current_datetime) |
            Q(booking_start_date__gte=current_datetime, booking_end_date__lt=current_datetime)
        )

        # Get parking slots with active bookings and set physical_available to False
        parking_slots_with_active_bookings = ParkingSlot.objects.filter(pk__in=active_bookings.values('parking_slot'))
        parking_slots_with_active_bookings.update(physical_available=False)

        # Get parking slots without active bookings and set physical_available to True
        parking_slots_without_active_bookings = ParkingSlot.objects.exclude(pk__in=parking_slots_with_active_bookings)
        parking_slots_without_active_bookings.update(physical_available=True)

        queryset = ParkingSlot.objects.filter(physical_available=True)
        
        has_charger = request.data.get('has_charger', None)
        if has_charger is not None:
            queryset = queryset.filter(has_charger=has_charger)

        serializer = ParkingSlotSerializer(queryset, many=True)
        return Response(serializer.data)

class ParkingSlotRulesViewSet(viewsets.ModelViewSet):
    queryset = ParkingSlotRules.objects.all()
    serializer_class = ParkingSlotRulesSerializer

class BookingViewSet(viewsets.ModelViewSet):
    queryset = Booking.objects.all()
    serializer_class = BookingSerializer
    
    def create(self, request, *args, **kwargs):
        user_id = request.data.get('user', None)
        parking_slot_id = request.data.get('parking_slot', None)
        booking_start_date_str = request.data.get('booking_start_date', None)
        booking_end_date_str = request.data.get('booking_end_date', None)
        
        if not user_id or not parking_slot_id or not booking_start_date_str or not booking_end_date_str:
            return Response({'error': 'Incomplete data provided.'}, status=status.HTTP_400_BAD_REQUEST)

        # Convert date strings to datetime objects
        try:
            booking_start_date = datetime.strptime(booking_start_date_str, '%Y-%m-%dT%H:%M:%S.%fZ')
            booking_end_date = datetime.strptime(booking_end_date_str, '%Y-%m-%dT%H:%M:%S.%fZ')
        except ValueError:
            return Response({'error': 'Invalid date format. Please use ISO format (e.g., 2023-01-01T00:00:00.000Z).'}, status=status.HTTP_400_BAD_REQUEST)

        # Check for conflicting rules
        conflicting_rules = ParkingSlotRules.objects.filter(
            parking_slot=parking_slot_id,
            date_start_rule__lt=booking_end_date,
            date_end_rule__gt=booking_start_date,
        ).first()

        if conflicting_rules:
            # Use the price from the conflicting rule
            price = conflicting_rules.price
        else:
            # No conflicting rules, use the standard price from ParkingSlot
            parking_slot = get_object_or_404(ParkingSlot, pk=parking_slot_id)
            price = parking_slot.standard_price

        # Check for conflicting bookings
        conflicting_bookings = Booking.objects.filter(
            parking_slot=parking_slot_id,
            booking_start_date__lt=booking_end_date,
            booking_end_date__gt=booking_start_date,
        ).exclude(
            Q(booking_start_date__gte=booking_end_date) | Q(booking_end_date__lte=booking_start_date)
        )

        if conflicting_bookings.exists():
            return Response({'error': 'Conflicts with existing bookings for the specified period.'}, status=status.HTTP_400_BAD_REQUEST)

        # If no conflicts, create the booking
        parking_slot = get_object_or_404(ParkingSlot, pk=parking_slot_id)

        data = {
            'user': user_id,
            'parking_slot': parking_slot_id,
            'booking_start_date': booking_start_date,
            'booking_end_date': booking_end_date,
            'price': price,
        }
        
        print(data)

        serializer = BookingSerializer(data=data)

        if serializer.is_valid():
            # Mark the parking slot as unavailable for the specified period
            # parking_slot.physical_available = False
            # parking_slot.save()

            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)