# Importe todas as views para facilitar o acesso
from .auth_views import register, login, logout
from .user_views import UserViewSet
from .reservation_views import ReservationViewSet  
from .room_views import RoomViewSet

__all__ = [
    'register', 'login', 'logout',
    'UserViewSet', 'ReservationViewSet', 'RoomViewSet',
]