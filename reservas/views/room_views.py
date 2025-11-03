from rest_framework import viewsets, permissions
from reservas.models import Room
from reservas.permissions import IsOwnerOrStaff
from reservas.serializers import (  
    RoomSerializer, 
)

class RoomViewSet(viewsets.ModelViewSet):
    serializer_class = RoomSerializer
    queryset = Room.objects.all()
    
    def get_permissions(self):
        if self.action in ['create', 'update', 'destroy']:
            permission_classes = [IsOwnerOrStaff]
        else:
            permission_classes = [permissions.AllowAny]
        return [permission() for permission in permission_classes]