from rest_framework import serializers
from ..models import Room

class RoomSerializer(serializers.ModelSerializer):
    is_available_display = serializers.BooleanField(source='is_available', read_only=True)
    hotel_name = serializers.CharField(source='hotel.name', read_only=True)
    
    class Meta:
        model = Room
        fields = [
            'id',
            'hotel',
            'room_number', 
            'room_type',
            'price_per_night',
            'capacity',
            'is_available',
            # Campos de leitura
            'is_available_display',
            'hotel_name'
        ]