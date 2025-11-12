# Importe todas as views para facilitar o acesso
from .auth_views import register, login, logout
from .user_views_api import UserViewSet
from .reservation_views_api import ReservationViewSet  
from .room_views_api import RoomViewSet

__all__ = [
    'register', 'login', 'logout',
    'UserViewSet', 'ReservationViewSet', 'RoomViewSet',
]