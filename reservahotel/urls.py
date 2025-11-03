from django.contrib import admin
from django.urls import path, include
from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny

@api_view(['GET'])
@permission_classes([AllowAny])
def home(request):
    return Response({"message": "Sistema funcionando!"})

urlpatterns = [
    path('admin/', admin.site.urls),  # Apenas para o Admin
    path('api/', include('reservas.urls')),
    path('', home, name='home'),      # Página inicial simples
]