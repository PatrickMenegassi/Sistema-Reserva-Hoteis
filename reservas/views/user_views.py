from rest_framework import viewsets, permissions, status
from rest_framework.decorators import action
from reservas.models import Usuario
from reservas.permissions import IsOwnerOrStaff
from reservas.serializers import (  
    UserSerializer,
    UserRegistrationSerializer
)

class UserViewSet(viewsets.ModelViewSet):
    queryset = Usuario.objects.all()
    
    def get_serializer_class(self):
        if self.action == 'create':
            return UserRegistrationSerializer
        return UserSerializer
    
    def get_permissions(self):
        
        if self.action == 'create':
            permission_classes = [permissions.AllowAny]
        else:
            permission_classes = [IsOwnerOrStaff]
        
        return [permission() for permission in permission_classes]