from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.views.generic import ListView, CreateView
from reservas.models import Reservation, Room
from reservas.forms import ReservationsForm

@login_required
def minhas_reservas(request): # Mostrar as reservas
    usuario = request.user # Pega o usuário logado

    if request.method == 'POST':
        form = ReservationsForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('minhas_reservas')
    else:
        form = ReservationsForm()
    
    
    return render(request, 'reservations/minhas_reservas.html', {'form': form,
                                                                 'user': usuario})