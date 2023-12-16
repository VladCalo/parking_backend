from django.urls import reverse
from django.test import TestCase
from rest_framework.test import APIClient, APITestCase
from rest_framework import status
from ..serializers import *
from ..models import *


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
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn("park owner with this email already exists", response.content.decode())
        
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
        print(response.content)
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
        self.park = Park.objects.create(**self.park_data)
        self.list_create_url = reverse('park-list-create')
        self.detail_url = reverse('park-detail', args=[self.park.pk])

    def test_get_park_list(self):
        response = self.client.get(self.list_create_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), Park.objects.count())

    def test_get_park_detail(self):
        response = self.client.get(self.detail_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['park_id'], self.park.park_id)

    def test_update_park(self):
        updated_data = {
            'park_owner': self.park_owner.pk,
            'total_spots': 150,
            'no_floors': 3,
            'park_details': self.park_details.pk
        }
        response = self.client.put(self.detail_url, updated_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.park.refresh_from_db()
        self.assertEqual(self.park.total_spots, updated_data['total_spots'])

    def test_delete_park(self):
        response = self.client.delete(self.detail_url)
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
        
class UsersCredentialsAPITest(APITestCase):
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
        self.users = Users.objects.create(**self.users_data)
        self.users_list_create_url = reverse('users-list-create')
        self.users_detail_url = reverse('users-detail', args=[self.users.pk])
        self.credentials_list_create_url = reverse('credentials-list-create')
        self.credentials_detail_url = reverse('credentials-detail', args=[self.credentials.pk])

        self.client = APIClient()

    def test_get_credentials_detail(self):
        response = self.client.get(self.credentials_detail_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_update_credentials(self):
        updated_data = {
            'email': 'test@example.com',
            'password': 'newpassword'
            }
        response = self.client.put(self.credentials_detail_url, updated_data, format='json')
        print(response.content)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.credentials.refresh_from_db()
        self.assertEqual(self.credentials.password, updated_data['password'])

    def test_delete_credentials(self):
        response = self.client.delete(self.credentials_detail_url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

    def test_get_users_detail(self):
        response = self.client.get(self.users_detail_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_update_users(self):
        updated_data = {
            'credentials': self.credentials.pk,
            'first_name': 'Update',
            'last_name': 'Doe',
            'number_plate': 'ABC123',
            'vehicle_type': 'Car',
            'verified': True
        }
        response = self.client.put(self.users_detail_url, updated_data, format='json')
        print(response.content)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.users.refresh_from_db()
        self.assertEqual(self.users.first_name, updated_data['first_name'])

    def test_delete_users(self):
        response = self.client.delete(self.users_detail_url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
          
class ParkingSlotAPITest(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.park_owner = ParkOwner.objects.create(first_name='John', last_name='Doe', email='john@example.com', password='password')
        self.park_details = ParkDetails.objects.create(
            address='Test Address',
            latitude=0.0,
            longitude=0.0,
            height_limit=2,
            weigh_limit=3500
        )
        self.park = Park.objects.create(park_owner=self.park_owner, park_details=self.park_details, total_spots=50, no_floors=5)
        self.floor = Floor.objects.create(park=self.park, floor_number=1)
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

    def test_create_parking_slot(self):
        response = self.client.post(self.parking_slot_list_create_url, self.parking_slot_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_get_parking_slot_detail(self):
        parking_slot = ParkingSlot.objects.create(floor=self.floor, slot_number=1, has_charger=True, physical_available=True, standard_price=10)
        response = self.client.get(self.parking_slot_detail_url)
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
        response = self.client.get(self.parking_slot_available_list_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        
