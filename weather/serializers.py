from rest_framework import serializers
from .models import WeatherData, Location


class LocationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Location
        fields = ["city", "country", "latitude", "longitude"]


class WeatherDataSerializer(serializers.ModelSerializer):
    location = LocationSerializer()  # Anidado para mostrar datos de ubicación

    class Meta:
        model = WeatherData
        fields = [
            "temperature",
            "humidity",
            "wind_speed",
            "description",
            "timestamp",
            "location",
        ]
