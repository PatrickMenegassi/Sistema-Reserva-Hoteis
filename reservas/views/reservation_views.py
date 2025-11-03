from rest_framework import viewsets, permissions, serializers
from reservas.models import Reservation, Room, Hotel
from reservas.serializers import (  
    ReservationSerializer)
from reservas.permissions import IsOwnerOrStaff, IsAuthenticated

class ReservationViewSet(viewsets.ModelViewSet):
    serializer_class = ReservationSerializer
    queryset = Reservation.objects.all()
    permission_classes = [IsAuthenticated]
    
    def get_permissions(self):
        
        if self.action == 'create':
            permission_classes = [permissions.AllowAny]
        else:
            permission_classes = [IsOwnerOrStaff]
        
        return [permission() for permission in permission_classes]
    
    def get_queryset(self):
        user = self.request.user
        if not hasattr(user, 'user_type'):
            return Reservation.objects.none()
        print(user)
        if user.user_type in ['staff', 'admin']:
            return Reservation.objects.all()
        else:
            return Reservation.objects.filter(customer=user)
    
    def perform_create(self, serializer):
        # Garante que está usando User personalizado
        if not hasattr(self.request.user, 'user_type'):
            raise serializers.ValidationError("Usuário não autenticado corretamente")
        
        #  Salva com User
        reserva = serializer.save(customer=self.request.user)
        
        reserva_data = {
            'reserva_id': reserva.id,
            'room_number': reserva.room.room_number,
            'room_type': reserva.room.get_room_type_display(),
            'check_in': reserva.check_in.strftime('%d/%m/%Y'),
            'check_out': reserva.check_out.strftime('%d/%m/%Y'),
            'total_price': str(reserva.total_price),
            'status': reserva.get_status_display(),
            'hotel_name': reserva.room.hotel.name,
        }
        
        # Envia email
        from reservas.tasks import send_reservation_confirmation
        send_reservation_confirmation.delay(reserva.customer.email, reserva.customer.nome, reserva_data)