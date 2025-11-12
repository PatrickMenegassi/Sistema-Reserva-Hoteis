from django.urls import path, include
from rest_framework.routers import DefaultRouter
from reservas.views.api import UserViewSet, RoomViewSet, ReservationViewSet, register, login, logout

# Funciona para quando se necessita de um CRUD completo, servem apenas para as API
router = DefaultRouter()
router.register('users', UserViewSet)
router.register('rooms', RoomViewSet)
router.register('reservations', ReservationViewSet)

urlpatterns = [
    path('', include(router.urls)),
    path('auth/register/', register, name='register'),
    path('auth/login/', login, name='login'),
    path('auth/logout/', logout, name='logout'),
]