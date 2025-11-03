from django.contrib.auth.models import AbstractUser
from django.db import models
from .room import Room
from .user import Usuario

class Reservation(models.Model):
    STATUS_CHOICES = (
        ('confirmed', 'Confirmada'),
        ('pending', 'Pendente'),
        ('cancelled', 'Cancelada'),
        ('completed', 'Concluída'),
    )
    customer = models.ForeignKey(Usuario, on_delete=models.CASCADE)
    room = models.ForeignKey(Room, on_delete=models.CASCADE)
    check_in = models.DateField()
    check_out = models.DateField()
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    total_price = models.DecimalField(max_digits=10, decimal_places=2)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Reserva #{self.id} - {self.customer.nome}"