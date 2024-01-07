# your_app/urls.py

from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import (
    BookingViewSet, ParkingSlotRulesListCreateView, ParkingSlotRulesUpdateView,
    ParkOwnerListCreateView, ParkOwnerDetailView,
    UsersListCreateView, UsersDetailView,
    CredentialsListCreateView, CredentialsDetailView,
    ParkListCreateView, ParkDetailView,
    ParkDetailsListCreateView, ParkDetailsDetailView, ParkingSlotRulesByPkOnlyView,
    FloorListCreateView, FloorDetailView,
    ParkingSlotListCreateView, ParkingSlotDetailView, ParkingSlotAvailableListView, LoginView
)
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)


router = DefaultRouter()
router.register(r'bookings', BookingViewSet, basename='booking')


urlpatterns = [
    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('login/', LoginView.as_view(), name='login'),
    path('park-owner/', ParkOwnerListCreateView.as_view(), name='park-owner-list-create'),
    path('park-owner/<int:pk>/', ParkOwnerDetailView.as_view(), name='park-owner-detail'),
    path('users/', UsersListCreateView.as_view(), name='users-list-create'),
    path('users/<int:pk>/', UsersDetailView.as_view(), name='users-detail'),
    path('credentials/', CredentialsListCreateView.as_view(), name='credentials-list-create'),
    path('credentials/<int:pk>/', CredentialsDetailView.as_view(), name='credentials-detail'),
    path('park/', ParkListCreateView.as_view(), name='park-list-create'),
    path('park/<int:pk>/', ParkDetailView.as_view(), name='park-detail'),
    path('park-details/', ParkDetailsListCreateView.as_view(), name='park-details-list-create'),
    path('park-details/<int:pk>/', ParkDetailsDetailView.as_view(), name='park-details-detail'),
    path('floors/', FloorListCreateView.as_view(), name='floor-list-create'),
    path('floors/<int:pk>/', FloorDetailView.as_view(), name='floor-detail'),
    path('parking-slots/', ParkingSlotListCreateView.as_view(), name='parkingslot-list-create'),
    path('parking-slots/<int:pk>/', ParkingSlotDetailView.as_view(), name='parkingslot-detail'),
    path('parking-slots/available/', ParkingSlotAvailableListView.as_view(), name='parkingslot-list-available'),
    path('parking-slot-rules/', ParkingSlotRulesListCreateView.as_view(), name='parkingslotrules-list-create'),
    path('parking-slot-rules/<int:pk>/', ParkingSlotRulesUpdateView.as_view(), name='parkingslotrules-update'),
    path('parking-slot-rules/by-pk/<int:pk>/', ParkingSlotRulesByPkOnlyView.as_view(), name='parkingslotrules-detail-by-pk'),
    path('bookings/', BookingViewSet.as_view(), name='booking-list'),
    path('bookings/<int:pk>/', BookingViewSet.as_view(), name='booking-detail'),
]
