from django.db import models


class Location(models.Model):
    city = models.CharField(max_length=100)
    country = models.CharField(max_length=100)
    latitude = models.DecimalField(
        max_digits=9, decimal_places=6, null=True, blank=True
    )
    longitude = models.DecimalField(
        max_digits=9, decimal_places=6, null=True, blank=True
    )
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.city}, {self.country}"


class WeatherData(models.Model):
    location = models.ForeignKey(
        Location, on_delete=models.CASCADE, related_name="weather_data"
    )
    temperature = models.DecimalField(max_digits=5, decimal_places=2)  # Ej: 25.50°C
    humidity = models.PositiveIntegerField()  # % de humedad
    wind_speed = models.DecimalField(max_digits=5, decimal_places=2)  # km/h
    description = models.CharField(max_length=200)  # "Cielo despejado"
    timestamp = models.DateTimeField(auto_now_add=True)  # Fecha/hora del registro

    def __str__(self):
        return f"{self.location.city} - {self.temperature}°C at {self.timestamp}"
