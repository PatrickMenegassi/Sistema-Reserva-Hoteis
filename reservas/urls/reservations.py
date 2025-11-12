from django.urls import path
from reservas.views.web.reservations_views import minhas_reservas

urlpatterns = [
    path('minhas-reservas/', minhas_reservas, name='minhas_reservas'),
    #path('nova-reserva/', views_web.nova_reserva, name='nova_reserva'), 
    #path('quartos/', views_web.lista_quartos, name='lista_quartos'),
]