from rest_framework import serializers
from ..models import Reservation
from reservas.tasks import send_reservation_confirmation

class ReservationSerializer(serializers.ModelSerializer):
    # Campos de leitura apenas (não podem ser editados na criação)
    customer_name = serializers.CharField(source='customer.get_full_name', read_only=True)
    room_number = serializers.CharField(source='room.room_number', read_only=True)
    room_type = serializers.CharField(source='room.get_room_type_display', read_only=True)
    hotel_name = serializers.CharField(source='room.hotel.name', read_only=True)
    
    class Meta:
        model = Reservation
        fields = [
            'id',
            'room',              
            'check_in',
            'check_out',
            'status',
            'total_price',
            'created_at',
            'customer_name',
            'room_number', 
            'room_type',
            'hotel_name'
        ]
        read_only_fields = ['status', 'total_price', 'created_at', 'customer']

    def validate(self, data):
        # Verifica se as datas são válidas
        if data['check_in'] >= data['check_out']:
            raise serializers.ValidationError("Check-out deve ser após check-in")
        
        # Verifica se o quarto está disponível
        room = data['room']
        if not room.is_available:
            raise serializers.ValidationError("Quarto não está disponível")
        
        # Verifica conflitos de reserva
        conflicting_reservations = Reservation.objects.filter(
            room=room,
            status__in=['confirmed', 'pending'],
            check_in__lt=data['check_out'],
            check_out__gt=data['check_in']
        )
        
        if conflicting_reservations.exists():
            raise serializers.ValidationError("Quarto já reservado para estas datas")
        
        return data

    def create(self, validated_data):
        validated_data['customer'] = self.context['request'].user
        # Calcula o número de dias
        days = (validated_data['check_out'] - validated_data['check_in']).days
        # Calcula o preço total
        validated_data['total_price'] = days * validated_data['room'].price_per_night
        
        # Cliente é automaticamente o usuário logado
        validated_data['customer'] = self.context['request'].user
        
        return super().create(validated_data)
    
    def perform_create(self, serializer):
        # Salva a reserva
        reserva = serializer.save(customer=self.request.user)
        
        # ENVIA EMAIL ASSÍNCRONO
        send_reservation_confirmation.delay(reserva.id)
        
        print(f"🎫 Reserva #{reserva.id} criada - Email em processamento")