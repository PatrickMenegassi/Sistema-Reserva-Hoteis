# reserves/views.py
from django.shortcuts import render
from django.contrib.auth.decorators import login_required

@login_required
def init_page(request):
    """Página principal após o login"""
    return render(request, 'base.html', {
        'user': request.user
    })