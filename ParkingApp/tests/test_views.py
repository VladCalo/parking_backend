from django.urls import reverse
from django.test import TestCase
from rest_framework.test import APIClient, APITestCase
from rest_framework import status
from ..serializers import *
from ..models import *
from datetime import datetime
from django.contrib.auth import get_user_model
import json


class ParkOwnerAPITest(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.park_owner_data = {
            'first_name': 'John',
            'last_name': 'Doe',
            'email': 'jd@yahoo.com',
            'password': 'securepassword'
        }
        self.park_owner = ParkOwner.objects.create(**self.park_owner_data)
        self.list_create_url = reverse('park-owner-list-create')
        self.detail_url = reverse('park-owner-detail', args=[self.park_owner.pk])

    def test_create_park_owner(self):
        response = self.client.post(self.list_create_url, self.park_owner_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        
    def test_get_park_owner_list(self):
        response = self.client.get(self.list_create_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), ParkOwner.objects.count())

    def test_get_park_owner_detail(self):
        response = self.client.get(self.detail_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['first_name'], self.park_owner.first_name)

    def test_update_park_owner(self):
        updated_data = {
            'first_name': 'UpdatedName',
            'last_name': self.park_owner.last_name,  
            'email': self.park_owner.email,         
            'password': self.park_owner.password    
        }
        response = self.client.put(self.detail_url, updated_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.park_owner.refresh_from_db()
        self.assertEqual(self.park_owner.first_name, updated_data['first_name'])
        
    def test_delete_park_owner(self):
        response = self.client.delete(self.detail_url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(ParkOwner.objects.count(), 0)

class ParkAPITest(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.park_owner = ParkOwner.objects.create(
            first_name='John',
            last_name='Doe',
            email='john.doe@example.com',
            password='securepassword'
        )
        self.park_details = ParkDetails.objects.create(
            address='123 Main St',
            latitude=40.7128,
            longitude=-74.0060,
            height_limit=2,
            weigh_limit=3500
        )
        self.park_data = {
            'park_owner': self.park_owner,
            'total_spots': 100,
            'no_floors': 2,
            'park_details': self.park_details
        }
        # self.park = Park.objects.create(**self.park_data)
        # self.detail_url = reverse('park-detail', args=[self.park.pk])
        self.list_create_url = reverse('park-list-create')
        
    def test_create_park(self):
        # self.park_data['park_owner'] = self.park_owner.pk
        # self.park_data['park_details'] = self.park_details.pk
        park_data = {
            'park_owner': self.park_owner.pk,
            'total_spots': 100,
            'no_floors': 2,
            'park_details': self.park_details.pk
        }
        
        response = self.client.post(self.list_create_url, park_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_get_park_list(self):
        response = self.client.get(self.list_create_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), Park.objects.count())

    def test_get_park_detail(self):
        park = Park.objects.create(**self.park_data)
        detail_url = reverse('park-detail', args=[park.pk])
        response = self.client.get(detail_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['park_id'], park.park_id)

    def test_update_park(self):
        park = Park.objects.create(**self.park_data)
        detail_url = reverse('park-detail', args=[park.pk])
        updated_data = {
            'park_owner': self.park_owner.pk,
            'total_spots': 150,
            'no_floors': 3,
            'park_details': self.park_details.pk
        }
        response = self.client.put(detail_url, updated_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        park.refresh_from_db()
        self.assertEqual(park.total_spots, updated_data['total_spots'])

    def test_delete_park(self):
        park = Park.objects.create(**self.park_data)
        detail_url = reverse('park-detail', args=[park.pk])
        response = self.client.delete(detail_url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Park.objects.count(), 0)

class ParkDetailsAPITest(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.park_details_data = {
            'address': '456 Oak St',
            'latitude': 34.0522,
            'longitude': -118.2437,
            'height_limit': 2,
            'weigh_limit': 3500
        }
        self.park_details = ParkDetails.objects.create(**self.park_details_data)
        self.list_create_url = reverse('park-details-list-create')
        self.detail_url = reverse('park-details-detail', args=[self.park_details.pk])

    def test_create_park_details(self):
        response = self.client.post(self.list_create_url, self.park_details_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(ParkDetails.objects.count(), 2)

    def test_get_park_details_list(self):
        response = self.client.get(self.list_create_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), ParkDetails.objects.count())

    def test_get_park_details_detail(self):
        response = self.client.get(self.detail_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['park_details_id'], self.park_details.park_details_id)

    def test_update_park_details(self):
        updated_data = {
            'address': '789 Pine St',
            'latitude': 37.7749,
            'longitude': -122.4194,
            'height_limit': 3,
            'weigh_limit': 4000
        }
        response = self.client.put(self.detail_url, updated_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.park_details.refresh_from_db()
        self.assertEqual(self.park_details.address, updated_data['address'])

    def test_delete_park_details(self):
        response = self.client.delete(self.detail_url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(ParkDetails.objects.count(), 0)
        
class CredentialsAPITest(TestCase):
    def setUp(self):
        self.credentials_data = {
            'email': 'test@example.com',
            'password': "password"
        }    
        
        self.credentials = Credentials.objects.create(**self.credentials_data)
        self.credentials_list_create_url = reverse('credentials-list-create')
        self.credentials_detail_url = reverse('credentials-detail', args=[self.credentials.pk])
        
    def test_create_credentials(self):
        response = self.client.post(
            self.credentials_list_create_url,
            data=json.dumps(self.credentials_data),
            content_type='application/json',
        )
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        
    def test_get_credentials_list(self):
        response = self.client.get(self.credentials_list_create_url)   
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), Credentials.objects.count())
        
    def test_get_credentials_detail(self):
        response = self.client.get(self.credentials_detail_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_update_credentials(self):
        updated_data = {
            'email': 'test@example.com',
            'password': 'newpassword'
            }
        response = self.client.put(
            self.credentials_detail_url, 
            data = json.dumps(updated_data), 
            content_type='application/json',
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.credentials.refresh_from_db()
        self.assertEqual(self.credentials.password, updated_data['password'])

    def test_delete_credentials(self):
        response = self.client.delete(self.credentials_detail_url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
                 
class UsersAPITest(TestCase):
    def setUp(self):
        self.credentials_data = {
            'email': 'test@example.com',
            'password': 'securepassword'
        }
        self.credentials = Credentials.objects.create(**self.credentials_data)

        self.users_data = {
            'credentials': self.credentials,
            'first_name': 'John',
            'last_name': 'Doe',
            'number_plate': 'ABC123',
            'vehicle_type': 'Car',
            'verified': True
        }
        # self.users = Users.objects.create(**self.users_data)
        # self.users_detail_url = reverse('users-detail', args=[self.users.pk])
        self.users_list_create_url = reverse('users-list-create')
        self.client = APIClient()
        
    def test_create_users(self):
        users_data = {
            'credentials': self.credentials.pk,
            'first_name': 'John',
            'last_name': 'Doe',
            'number_plate': 'ABC123',
            'vehicle_type': 'Car',
            'verified': True
        }
        
        response = self.client.post(self.users_list_create_url, users_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        
    def test_get_users_list(self):
        response = self.client.get(self.users_list_create_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), Park.objects.count())

    def test_get_users_detail(self):
        users = Users.objects.create(**self.users_data)
        users_detail_url = reverse('users-detail', args=[users.pk])
        response = self.client.get(users_detail_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_update_users(self):
        users = Users.objects.create(**self.users_data)
        users_detail_url = reverse('users-detail', args=[users.pk])
        updated_data = {
            'credentials': self.credentials.pk,
            'first_name': 'Update',
            'last_name': 'Doe',
            'number_plate': 'ABC123',
            'vehicle_type': 'Car',
            'verified': True
        }
        response = self.client.put(users_detail_url, updated_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        users.refresh_from_db()
        self.assertEqual(users.first_name, updated_data['first_name'])

    def test_delete_users(self):
        users = Users.objects.create(**self.users_data)
        users_detail_url = reverse('users-detail', args=[users.pk])
        response = self.client.delete(users_detail_url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
          
class FloorAPITest(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.park_owner = ParkOwner.objects.create(
            first_name='John',
            last_name='Doe',
            email='john.doe@example.com',
            password='securepassword'
        )
        self.park_details = ParkDetails.objects.create(
            address='123 Main St',
            latitude=40.7128,
            longitude=-74.0060,
            height_limit=2,
            weigh_limit=3500
        )
        
        self.park = Park.objects.create(
            park_owner=self.park_owner,
            total_spots=100,
            no_floors=2,
            park_details=self.park_details
        )
        
        self.floor_data = {
            'park': self.park,
            'floor_number': 1
        }
        
        self.floor = Floor.objects.create(**self.floor_data)
        self.detail_url = reverse('floor-detail', args=[self.floor.pk])
        self.list_create_url = reverse('floor-list-create')
        
    def test_create_floor(self):
        floor_data = {
            'park': self.park.pk,
            'floor_number': 1
        }
        response = self.client.post(self.list_create_url, floor_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
    
    def test_get_floor_list(self):
        response = self.client.get(self.list_create_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), Park.objects.count())
        
    def test_get_floor_details(self):
        response = self.client.get(self.detail_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        
    def test_update_floor(self):
        updated_data = {
            'park': self.park.pk,
            'floor_number': 2
        }
        response = self.client.put(self.detail_url, updated_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.floor.refresh_from_db()
        self.assertEqual(self.floor.floor_number, updated_data['floor_number'])
        
    def test_delete_floor(self):
        response = self.client.delete(self.detail_url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
                
class ParkingSlotAPITest(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.park_owner = ParkOwner.objects.create(
            first_name='John', 
            last_name='Doe', 
            email='john@example.com', 
            password='password'
        )
        self.park_details = ParkDetails.objects.create(
            address='Test Address',
            latitude=0.0,
            longitude=0.0,
            height_limit=2,
            weigh_limit=3500
        )
        self.park = Park.objects.create(
            park_owner=self.park_owner, 
            park_details=self.park_details, 
            total_spots=50, 
            no_floors=5
        )
        self.floor = Floor.objects.create(
            park=self.park, 
            floor_number=1
        )
        self.parking_slot_data = {
            'floor': self.floor.floor_id,
            'slot_number': 1,
            'has_charger': True,
            'physical_available': True,
            'standard_price': 10,
        }
                
        self.parking_slot_list_create_url = reverse('parkingslot-list-create')
        self.parking_slot_detail_url = reverse('parkingslot-detail', kwargs={'pk': 1})
        self.parking_slot_available_list_url = reverse('parkingslot-list-available')
        
        self.parking_slot_rules_list_create_url = reverse('parkingslotrules-list-create')
        self.parking_slot_rules_detail_url = reverse('parkingslotrules-update', kwargs={'pk': 1})
        self.parking_slot_rules_by_pk_url = reverse('parkingslotrules-detail-by-pk', kwargs={'pk': 1})


    def test_create_parking_slot(self):
        response = self.client.post(self.parking_slot_list_create_url, self.parking_slot_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        
    def test_get_parking_slot_list(self):
        data = {
            "has_charger": True
        }
        response = self.client.get(self.parking_slot_list_create_url, data=data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_get_parking_slot_detail(self):
        parking_slot = ParkingSlot.objects.create(
            floor=self.floor, 
            slot_number=1, 
            has_charger=True, 
            physical_available=True, 
            standard_price=10
        )
        data = {
            "has_charger": True
        }
        response = self.client.get(self.parking_slot_detail_url, data=data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_update_parking_slot(self):
        parking_slot = ParkingSlot.objects.create(floor=self.floor, slot_number=1, has_charger=True, physical_available=True, standard_price=10)
        updated_data = {
            'floor': self.floor.floor_id,
            'slot_number': 1,
            'has_charger': False,
            'physical_available': False,
            'standard_price': 15,
        }
        response = self.client.put(self.parking_slot_detail_url, {**self.parking_slot_data, **updated_data}, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        parking_slot.refresh_from_db()
        self.assertEqual(parking_slot.has_charger, updated_data['has_charger'])
        self.assertEqual(parking_slot.physical_available, updated_data['physical_available'])
        self.assertEqual(parking_slot.standard_price, updated_data['standard_price'])

    def test_delete_parking_slot(self):
        parking_slot = ParkingSlot.objects.create(floor=self.floor, slot_number=1, has_charger=True, physical_available=True, standard_price=10)
        response = self.client.delete(self.parking_slot_detail_url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

    def test_get_available_parking_slots(self):
        data = {
            "has_charger": True
        }
        response = self.client.get(self.parking_slot_available_list_url, data=data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
            
class BookingParkingSlotRulesAPITest(TestCase):
    def setUp(self):
        self.park_owner = ParkOwner.objects.create(
            first_name="John", 
            last_name="Doe", 
            email="john.doe@example.com", 
            password="password123"
        )
        self.user = Users.objects.create(
            credentials=Credentials.objects.create(
                email="user@example.com", 
                password="userpassword"
            ), 
            first_name="Jane", last_name="Doe", 
            number_plate="ABC123", 
            vehicle_type="Car", 
            verified=True
        )
        self.credentials = Credentials.objects.create(
            email="test@example.com", 
            password="testpassword"
        )

        self.park_details = ParkDetails.objects.create(
            address="123 Main St", 
            latitude=40.7128, 
            longitude=-74.0060, 
            height_limit=2, 
            weigh_limit=3500
        )
        
        self.park = Park.objects.create(
            park_owner=self.park_owner, 
            total_spots=100, 
            no_floors=5, 
            park_details=self.park_details
        )
        
        self.floor = Floor.objects.create(
            park=self.park,
            floor_number=1
        )
        self.parking_slot = ParkingSlot.objects.create(
            floor=self.floor, 
            slot_number=1, 
            has_charger=True, 
            physical_available=True, 
            standard_price=10
        )
        self.parking_slot_rules = ParkingSlotRules.objects.create(
            parking_slot=self.parking_slot, 
            date_start_rule="2023-01-01T00:00:00.000Z", 
            date_end_rule="2023-01-01T00:00:00.000Z", 
            price=15.0
        )
        # self.booking = Booking.objects.create(
        #     parking_slot=self.parking_slot, 
        #     user=self.user, 
        #     booking_start_date="2023-01-01T12:00:00.000Z", 
        #     booking_end_date="2023-01-01T14:00:00.000Z", 
        #     price=10.0
        # )

        self.client = APIClient()

    def test_create_booking(self):
        url = reverse('booking-list')
        data = {
            'user': self.user.pk,
            'parking_slot': self.parking_slot.pk,
            'booking_start_date': "2023-01-03T12:00:00.000Z",
            'booking_end_date': "2023-01-03T14:00:00.000Z",
            'price': 12.0,
        }

        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
                
    def test_create_missing_args_booking(self):
        url = reverse('booking-list')
        data = {
            # 'user': self.user.pk,
            'parking_slot': self.parking_slot.pk,
            'booking_start_date': "2023-01-03T12:00:00.000Z",
            'booking_end_date': "2023-01-03T14:00:00.000Z",
            'price': 12.0,
        }

        response = self.client.post(url, data, format='json')
        
    def test_create_invalid_args_booking(self):
        url = reverse('booking-list')
        data = {
            'user': self.user.pk,
            'parking_slot': self.parking_slot.pk,
            'booking_start_date': "2023-01-03T12:00:00",
            'booking_end_date': "2023-01-03T14:00:00.000Z",
            'price': 12.0,
        }

        response = self.client.post(url, data, format='json')

    def test_read_booking(self):
        booking = Booking.objects.create(
            parking_slot=self.parking_slot, 
            user=self.user, 
            booking_start_date="2023-01-01T12:00:00.000Z", 
            booking_end_date="2023-01-01T14:00:00.000Z", 
            price=10.0
        )

        url = reverse('booking-detail', args=[booking.pk])
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        
    def test_delete_booking(self):
        booking = Booking.objects.create(
            parking_slot=self.parking_slot, 
            user=self.user, 
            booking_start_date="2023-01-01T12:00:00.000Z", 
            booking_end_date="2023-01-01T14:00:00.000Z", 
            price=10.0
        )
        
        url = reverse('booking-detail', args=[booking.pk])
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        
    # def test_update_booking(self):
    #     booking = Booking.objects.create(
    #         parking_slot=self.parking_slot, 
    #         user=self.user, 
    #         booking_start_date="2023-01-01T12:00:00.000Z", 
    #         booking_end_date="2023-01-01T14:00:00.000Z", 
    #         price=10.0
    #     )
        
    #     updated_data = {
    #         'parking_slot': self.parking_slot.pk,
    #         'user': self.user.pk,
    #         'booking_start_date': "2023-01-01T12:00:00.000Z",
    #         'booking_end_data': "2023-01-01T14:00:00.000Z",
    #         'price': 15.0
    #     }
        
    #     url = reverse('booking-detail', args=[booking.pk])
    #     response = self.client.put(url, updated_data, format='json')
    #     print("\n###########################\n")
    #     print(response.content)
    #     self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_create_parking_slot_rule(self):
        url = reverse('parkingslotrules-list-create')
        data = {
            'parking_slot': self.parking_slot.pk,
            'date_start_rule': "2023-01-03T12:00:00.000Z",
            'date_end_rule': "2023-01-03T14:00:00.000Z",
            'price': 20.0,
        }

        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        
    def test_create_conflicting_parking_slot_rule(self):
        url = reverse('parkingslotrules-list-create')
        data = {
            'parking_slot': self.parking_slot.pk,
            'date_start_rule': "2023-01-03T12:00:00.000Z",
            'date_end_rule': "2023-01-03T14:00:00.000Z",
            'price': 20.0,
        }   
        response = self.client.post(url, data, format='json')
        response2 = self.client.post(url, data, format='json')
        
    def test_create_incomplete_parking_slot_rule(self):
        url = reverse('parkingslotrules-list-create')
        data = {
            'parking_slot': self.parking_slot.pk,
            'date_start_rule': "2023-01-03T12:00:00.000Z",
            # 'date_end_rule': "2023-01-03T14:00:00.000Z",
            'price': 20.0,
        }

        response = self.client.post(url, data, format='json')

    def test_create_invalid_parking_slot_rule(self):
        url = reverse('parkingslotrules-list-create')
        data = {
            'parking_slot': self.parking_slot.pk,
            'date_start_rule': "2023-01-03T12:00:00.000Z",
            'date_end_rule': "2023-01-03T14:00:00",
            'price': 20.0,
        }

        response = self.client.post(url, data, format='json')

    def test_get_parking_slot_rules_list(self):
        url = reverse('parkingslotrules-list-create')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
    
    def test_get_parking_slot_rules_by_pk(self):
        url = reverse('parkingslotrules-detail-by-pk', args=[self.parking_slot_rules.pk])
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        
    def test_get_missing_parking_slot_rules_by_pk(self):
        try:
            url = reverse('parkingslotrules-detail-by-pk', args=[999])
            response = self.client.get(url)
            self.assertEqual(response.status_code, status.HTTP_200_OK) 
        except Exception as e:
            pass 
         
    def test_update_parking_slot_rules(self):
        url = reverse("parkingslotrules-update", args=[self.parking_slot_rules.pk])
        updated_data = {
            'parking_slot': self.parking_slot.pk,
            'date_start_rule': "2023-01-01T00:00:00.000Z",
            'date_end_rule': "2023-01-02T00:00:00.000Z",
            'price': 21.0,
        }
        response = self.client.put(url, updated_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.parking_slot_rules.refresh_from_db()
        self.assertEqual(self.parking_slot_rules.price, updated_data['price'])
        
    def test_update_missing_date_parking_slot_rules(self):
        url = reverse("parkingslotrules-update", args=[self.parking_slot_rules.pk])
        updated_data = {
            'parking_slot': self.parking_slot.pk,
            'date_start_rule': "2023-01-01T00:00:00",
            # 'date_end_rule': "2023-01-02T00:00:00.000Z",
            'price': 21.0,
        }
        try:
            response = self.client.put(url, updated_data, format='json')
        except Exception as e:
            pass
        
    def test_update_invalid_date_parking_slot_rules(self):
        url = reverse("parkingslotrules-update", args=[self.parking_slot_rules.pk])
        updated_data = {
            # 'parking_slot': self.parking_slot.pk,
            'date_start_rule': "2023-01-01T00:00:00",
            'date_end_rule': "2023-01-02T00:00:00",
            'price': 21.0,
        }
        try:
            response = self.client.put(url, updated_data, format='json')
        except Exception as e:
            pass
        
    def test_update_missing_id_parking_slot_rules(self):
        url = reverse("parkingslotrules-update", args=[self.parking_slot_rules.pk])
        updated_data = {
            # 'parking_slot': self.parking_slot.pk,
            'date_start_rule': "2023-01-01T00:00:00.000Z",
            'date_end_rule': "2023-01-02T00:00:00.000Z",
            'price': 21.0,
        }
        try:
            response = self.client.put(url, updated_data, format='json')
        except Exception as e:
            pass
        
    def test_update_no_matching_rules_parking_slot_rules(self):
        url = reverse("parkingslotrules-update", args=[self.parking_slot_rules.pk])
        updated_data = {
            'parking_slot': self.parking_slot.pk,
            'date_start_rule': "2024-01-01T00:00:00.000Z",
            'date_end_rule': "2024-01-02T00:00:00.000Z",
            'price': 21.0,
        }
        try:
            response = self.client.put(url, updated_data, format='json')
        except Exception as e:
            pass    
        
    # def test_delete_parking_slot_rules(self):     
    #     rule = ParkingSlotRules.objects.create(
    #         parking_slot=self.parking_slot, 
    #         date_start_rule="2025-01-01T00:00:00.000Z", 
    #         date_end_rule="2025-01-01T00:00:00.000Z", 
    #         price=15.0
    #     )
        
    #     data={
    #         'parking_slot': rule.pk,
    #         'date_start_rule': "2025-01-01T00:00:00.000Z",
    #         'date_end_rule': "2025-01-01T00:00:00.000Z",
    #         # 'price': 15.0
    #     }
        
    #     url = reverse("parkingslotrules-update", args=[rule.pk])
    #     response = self.client.delete(url, data=data, format='json')
    #     print("\n################################################################\n")
    #     print(response.content)
    #     # self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
    
class LoginAPITest(TestCase):
    def setUp(self):
        self.url = reverse("login")
        self.valid_email = "test@example.com"
        self.valid_password = "password123"
        Credentials.objects.create(email=self.valid_email, password=self.valid_password)
        
        park_owner = ParkOwner.objects.create(
            first_name = "John",
            last_name = "Doe",
            email  = "owner@example.com",
            password = "password123"
        )
        
    def test_login_with_valid_credentials(self):
        data = {
            'email': self.valid_email, 
            'password': self.valid_password
        }
        response = self.client.post(self.url, data, format='json', content_type='application/json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        
    def test_login_with_missing_credentials(self):
        data = {
            'email': self.valid_email, 
            # 'password': self.valid_password
        }
        response = self.client.post(self.url, data, format='json', content_type='application/json')
        
    def test_login_parkowner_credentials(self):
        data = {
            'email': "owner@example.com", 
            'password': "password123"
        }
        response = self.client.post(self.url, data, format='json', content_type='application/json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        
    def test_login_bad_credentials(self):
        data = {
            'email': "aaaa@example.com", 
            'password': "securepassword"
        }
        response = self.client.post(self.url, data, format='json', content_type='application/json')
        
    


