from django.urls import path
from .views import weather_frontend

urlpatterns = [
    path(
        "", weather_frontend, name="weather-frontend"
    ),  # Vista para el template con Alpine.js/Tailwind
]
