# views.py
from rest_framework.response import Response
from rest_framework import status
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

class ParkingSlotRulesViewSet(viewsets.ModelViewSet):
    queryset = ParkingSlotRules.objects.all()
    serializer_class = ParkingSlotRulesSerializer

class BookingViewSet(viewsets.ModelViewSet):
    queryset = Booking.objects.all()
    serializer_class = BookingSerializer
    
    def create(self, request, *args, **kwargs):
        booking_start_date_str = request.data.get('booking_start_date', None)
        booking_end_date_str = request.data.get('booking_end_date', None)

        if not booking_start_date_str or not booking_end_date_str:
            return Response({'error': 'Booking start date and end date are required in query parameters.'}, status=status.HTTP_400_BAD_REQUEST)

        try:
            booking_start_date = datetime.strptime(booking_start_date_str, '%Y-%m-%dT%H:%M:%S.%fZ')
            booking_end_date = datetime.strptime(booking_end_date_str, '%Y-%m-%dT%H:%M:%S.%fZ')
        except ValueError:
            return Response({'error': 'Invalid date format. Please use ISO format (e.g., 2023-01-01T00:00:00.000Z).'}, status=status.HTTP_400_BAD_REQUEST)
        
        rules_exist = ParkingSlotRules.objects.filter(
            parking_slot=request.data.get('parking_slot', None),
            date_start_rule=booking_start_date,
            date_end_rule=booking_end_date,
        ).exists()
        
        if rules_exist:
            ok = 0
            parking_slot_available = ParkingSlotRules.objects.filter(
                parking_slot_id=request.data.get('parking_slot', None),
                available=True,
            ).exists()
            
            parking_slot_price = ParkingSlotRules.objects.filter(
                parking_slot=request.data.get('parking_slot', None),
                date_start_rule__lte=booking_start_date,
                date_end_rule__gte=booking_end_date,
            ).first()

            if not parking_slot_available:
                return Response({'error': 'The parking slot is not available for the specified period.'}, status=status.HTTP_400_BAD_REQUEST)

            else:
                data = {
                'parking_slot': request.data.get('parking_slot', None),
                'user': request.data.get('user', None),
                'booking_start_date': booking_start_date,
                'booking_end_date': booking_end_date,
                'price': parking_slot_price.price,
            }

        else:
            ok = 1
            parking_slot_available = ParkingSlot.objects.filter(
                parking_slot_id=request.data.get('parking_slot', None),
                physical_available=True,
            ).exists()
            
            if not parking_slot_available:
                return Response({'error': 'The parking slot is not available for the specified period.'}, status=status.HTTP_400_BAD_REQUEST)

            parking_slot_price = ParkingSlot.objects.get(pk=request.data.get('parking_slot', None)).standard_price
            data = {
                'parking_slot': request.data.get('parking_slot', None),
                'user': request.data.get('user', None),
                'booking_start_date': booking_start_date,
                'booking_end_date': booking_end_date,
                'price': parking_slot_price,
            }
            
        serializer = BookingSerializer(data=data)

        if serializer.is_valid():
                # Reserve the parking slot and mark it as unavailable for the specified period
            parking_slot = ParkingSlot.objects.get(pk=request.data.get('parking_slot', None))
            parking_slot.physical_available = False
            parking_slot.save()
            
            if ok == 0:
                parking_slot = ParkingSlotRules.objects.get(pk=request.data.get('parking_slot', None))
                parking_slot.available = False
                parking_slot.save()
                
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)