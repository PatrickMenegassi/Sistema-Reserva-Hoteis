from django.contrib import admin
from django.urls import path, include
from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny
from django.contrib.auth import views as auth_views
from django.views.generic.base import RedirectView
from reservas.views.web import initial_page

#@api_view(['GET'])
#@permission_classes([AllowAny])
#def home(request):
#    return Response({"message": "Sistema funcionando!"})

urlpatterns = [
    path('admin/', admin.site.urls),  # Apenas para o Admin

    path('', RedirectView.as_view(url='/accounts/login/', permanent=False), name='home'),

    path('accounts/login/', auth_views.LoginView.as_view(template_name='login.html'), name='login'),
    path('accounts/logout/', auth_views.LogoutView.as_view(), name='logout'),

    path('init_page/', initial_page.init_page, name='dashboard'),
    
    path('api/', include('reservas.urls.api_urls')), # Urls da API
    path('web/', include('reservas.urls')), # Urls que vão para sistema web
    #path('', home, name='home'),      # Página inicial simples
]