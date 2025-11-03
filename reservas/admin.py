from django.contrib import admin
from reservas.models import Usuario, Room, Reservation, Hotel

@admin.register(Usuario)
class UserAdmin(admin.ModelAdmin):
    list_display = ('email', 'nome', 'user_type', 'ativo', 'data_criacao')
    list_filter = ('user_type', 'ativo', 'data_criacao')
    search_fields = ('email', 'nome', 'cpf')
    readonly_fields = ('data_criacao', 'data_atualizacao')
    
    fieldsets = (
        ('Informações de Acesso', {
            'fields': ('email',)
        }),
        ('Informações Pessoais', {
            'fields': ('nome', 'telefone', 'cpf', 'data_nascimento', 'endereco')
        }),
        ('Configurações do Sistema', {
            'fields': ('user_type', 'ativo')
        }),
        ('Datas', {
            'fields': ('data_criacao', 'data_atualizacao'),
            'classes': ('collapse',)
        }),
    )

@admin.register(Room)
class RoomAdmin(admin.ModelAdmin):
    list_display = ['room_number', 'room_type', 'price_per_night', 'capacity', 'is_available']

@admin.register(Reservation)
class ReservationAdmin(admin.ModelAdmin):
    list_display = ['customer', 'room', 'check_in', 'check_out', 'status']

# Se tiver modelo Hotel:
@admin.register(Hotel)
class HotelAdmin(admin.ModelAdmin):
    list_display = ['name', 'address']