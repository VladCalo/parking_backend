# your_app/urls.py

from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import (
    ParkOwnerViewSet, UsersViewSet, ParkViewSet,
    ParkDetailsViewSet, FloorViewSet, ParkingSlotViewSet,
    ParkingSlotRulesViewSet, BookingViewSet, CredentialsViewSet
)

router = DefaultRouter()
router.register(r'parkowner', ParkOwnerViewSet, basename='parkowner')
router.register(r'users', UsersViewSet, basename='users')
router.register(r'park', ParkViewSet, basename='park')
router.register(r'parkdetails', ParkDetailsViewSet, basename='parkdetails')
router.register(r'floors', FloorViewSet, basename='floor')
router.register(r'parkingslots', ParkingSlotViewSet, basename='parkingslot')
router.register(r'parkingslotrules', ParkingSlotRulesViewSet, basename='parkingslotrules')
router.register(r'bookings', BookingViewSet, basename='booking')
router.register(r'credentials', CredentialsViewSet, basename='credentials')

urlpatterns = [
    path('api/', include(router.urls)),
    # Add other URL patterns as needed
]
