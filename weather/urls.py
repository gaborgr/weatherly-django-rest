from django.urls import path
from .views import WeatherAPIView
from rest_framework_simplejwt.views import TokenObtainPairView

urlpatterns = [
    path("weather/", WeatherAPIView.as_view(), name="weather-api"),  # Endpoint API
    # path("token/", TokenObtainPairView.as_view(), name="token_obtain_pair"),  # ⚠️ Opcional (mejor en weatherly/urls.py)
]
