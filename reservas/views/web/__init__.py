from django.urls import include, path

urlpatterns = [
    path('reservations/', include('reservas.urls.reservations')),
]