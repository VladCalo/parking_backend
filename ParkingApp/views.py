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
    
    def create(self, request, *args, **kwargs):
        parking_slot_id = request.data.get('parking_slot', None)
        date_start_rule_str = request.data.get('date_start_rule', None)
        date_end_rule_str = request.data.get('date_end_rule', None)
        available = request.data.get('available', None)
        price = request.data.get('price', None)

        if not parking_slot_id or not date_start_rule_str or not date_end_rule_str or not available or price is None:
            return Response({'error': 'Incomplete data provided.'}, status=status.HTTP_400_BAD_REQUEST)

        # Convert date strings to datetime objects
        try:
            date_start_rule = datetime.strptime(date_start_rule_str, '%Y-%m-%dT%H:%M:%S.%fZ')
            date_end_rule = datetime.strptime(date_end_rule_str, '%Y-%m-%dT%H:%M:%S.%fZ')
        except ValueError:
            return Response({'error': 'Invalid date format. Please use ISO format (e.g., 2023-01-01T00:00:00.000Z).'},
                            status=status.HTTP_400_BAD_REQUEST)

        # Check for conflicting rules
        conflicting_rules = ParkingSlotRules.objects.filter(
            parking_slot=parking_slot_id,
            date_start_rule__lt=date_end_rule,
            date_end_rule__gt=date_start_rule,
        ).first()

        if conflicting_rules:
            return Response({'error': 'Conflicts with existing rules for the specified period.'},
                            status=status.HTTP_400_BAD_REQUEST)

        # If no conflicts, create the rule
        parking_slot_rule_data = {
            'parking_slot': parking_slot_id,
            'date_start_rule': date_start_rule,
            'date_end_rule': date_end_rule,
            'available': available,
            'price': price,
        }

        serializer = ParkingSlotRulesSerializer(data=parking_slot_rule_data)
        
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def get_object(self):
        # Override the get_object method to dynamically fetch the parking_slot
        queryset = self.get_queryset()

        date_start_rule_str = self.request.data.get('date_start_rule', None)
        date_end_rule_str = self.request.data.get('date_end_rule', None)

        if not date_start_rule_str or not date_end_rule_str:
            raise AttributeError("date_start_rule and date_end_rule must be provided in the request data.")

        try:
            date_start_rule = datetime.strptime(date_start_rule_str, '%Y-%m-%dT%H:%M:%S.%fZ')
            date_end_rule = datetime.strptime(date_end_rule_str, '%Y-%m-%dT%H:%M:%S.%fZ')
        except ValueError:
            raise ValueError("Invalid date format. Please use ISO format (e.g., 2023-01-01T00:00:00.000Z).")

        parking_slot_id = self.request.data.get('parking_slot', None)

        if not parking_slot_id:
            raise AttributeError("parking_slot must be provided in the request data.")

        obj = queryset.filter(
            parking_slot=parking_slot_id,
            date_start_rule__lt=date_end_rule,
            date_end_rule__gt=date_start_rule
        ).first()

        return obj

    def put(self, request, *args, **kwargs):
        partial = kwargs.pop('partial', False)

        instance = self.get_object()

        if instance is None:
            return Response({'error': 'No matching rule found for the specified period and parking slot.'},
                            status=status.HTTP_404_NOT_FOUND)

        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)

        return Response(serializer.data)

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
        
    def put(self, request, *args, **kwargs):
        user_id = request.data.get('user', None)
        new_start_date_str = request.data.get('new_start_date', None)
        new_end_date_str = request.data.get('new_end_date', None)
        new_parking_slot_id = request.data.get('new_parking_slot', None)

        if not user_id or not new_start_date_str or not new_end_date_str or not new_parking_slot_id:
            return Response({'error': 'Incomplete data provided.'}, status=status.HTTP_400_BAD_REQUEST)

        # Convert date strings to datetime objects
        try:
            new_start_date = datetime.strptime(new_start_date_str, '%Y-%m-%dT%H:%M:%S.%fZ')
            new_end_date = datetime.strptime(new_end_date_str, '%Y-%m-%dT%H:%M:%S.%fZ')
        except ValueError:
            return Response({'error': 'Invalid date format. Please use ISO format (e.g., 2023-01-01T00:00:00.000Z).'},
                            status=status.HTTP_400_BAD_REQUEST)

        # Check for conflicts with new start and end date
        conflicting_bookings = Booking.objects.filter(
            user=user_id,
            parking_slot=new_parking_slot_id,
            booking_start_date__lt=new_end_date,
            booking_end_date__gt=new_start_date,
        ).exclude(
            Q(booking_start_date__gte=new_end_date) | Q(booking_end_date__lte=new_start_date)
)

        if conflicting_bookings.exists():
            return Response({'error': 'Conflicts with existing bookings for the specified period.'},
                            status=status.HTTP_400_BAD_REQUEST)

        # Get the existing booking for the user
        existing_booking = Booking.objects.get(user=user_id)
        parking_slot = ParkingSlot.objects.get(pk=new_parking_slot_id)

        if existing_booking:
            # Update the existing booking with the new dates and parking slot
            existing_booking.booking_start_date = new_start_date
            existing_booking.booking_end_date = new_end_date
            existing_booking.parking_slot = parking_slot
            
            parking_slot_rule = ParkingSlotRules.objects.filter(
                parking_slot=new_parking_slot_id,
                date_start_rule__lte=new_end_date,
                date_end_rule__gte=new_start_date,
            ).first()
            
            if parking_slot_rule:
                # Use the price from the parking slot rule
                existing_booking.price = parking_slot_rule.price

            existing_booking.save()

            serializer = BookingSerializer(existing_booking)
            return Response(serializer.data, status=status.HTTP_200_OK)
        else:
            return Response({'error': 'No active booking found for the specified user.'},
                            status=status.HTTP_400_BAD_REQUEST)