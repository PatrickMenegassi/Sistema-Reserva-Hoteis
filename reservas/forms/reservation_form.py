from django import forms
from ..models import Reservation, Room, Usuario

class ReservationsForm(forms.ModelForm):
    class Meta:
        model = Reservation
        fields = [ 'customer', 'room', 'check_in', 'check_out']

    

    customer = forms.ModelChoiceField(
        label='Usuário',
        queryset=Usuario.objects.all().order_by('nome'),
        required=True,
        widget=forms.Select(attrs={
            'class': 'form-control select2-busca',
        }),
    )

    room = forms.ModelChoiceField(
        label='Quarto',
        queryset=Room.objects.all(),
        required=True,
        widget=forms.Select(attrs={
            'class': 'form-control select2-busca',
        }),
    )

    check_in = forms.DateField(
        label='Data de entrada',
        widget=forms.DateInput(attrs={
            'type': 'date',
            'class': 'form-control',
        }),
        required=True
    )
    
    check_out = forms.DateField(
        label='Data de saída',
        widget=forms.DateInput(attrs={
            'type': 'date',
            'class': 'form-control',
        }),
        required=True
    )

