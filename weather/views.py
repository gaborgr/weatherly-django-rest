from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.shortcuts import render
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi
from .services import get_coordinates, fetch_weather_by_coords
from .models import WeatherData, Location
from .serializers import WeatherDataSerializer


def weather_frontend(request):
    weather_data = None

    if "city" in request.GET:
        city = request.GET.get("city")
        country = request.GET.get("country", "cl")

        # Usa tu función de servicios o llama a tu propia API
        lat, lon = get_coordinates(city, country)
        if lat and lon:
            weather_data = fetch_weather_by_coords(lat, lon)
            if weather_data:
                # Formatea los datos como tu serializer
                weather_data = {
                    "location": {
                        "city": city,
                        "country": country,
                        "latitude": lat,
                        "longitude": lon,
                    },
                    "temperature": weather_data["main"]["temp"],
                    "humidity": weather_data["main"]["humidity"],
                    "wind_speed": weather_data["wind"]["speed"],
                    "description": weather_data["weather"][0]["description"],
                }

    return render(request, "weather/index.html", {"weather_data": weather_data})


class WeatherAPIView(APIView):
    @swagger_auto_schema(
        manual_parameters=[
            openapi.Parameter(
                name="city",
                in_=openapi.IN_QUERY,  # Cambiado de QUERY a IN_QUERY
                description="Nombre de la ciudad",
                type=openapi.TYPE_STRING,
            ),
            openapi.Parameter(
                name="country",
                in_=openapi.IN_QUERY,  # Cambiado de QUERY a IN_QUERY
                description="Código de país (ej: cl)",
                type=openapi.TYPE_STRING,
            ),
        ],
        responses={
            200: WeatherDataSerializer,
            404: "Ubicación no encontrada",
            503: "Error al consultar el clima",
        },
    )
    def get(self, request):
        city = request.query_params.get("city", "Santiago")
        country = request.query_params.get("country", "cl")

        # 1. Obtener o crear Location
        lat, lon = get_coordinates(city, country)
        if not lat or not lon:
            return Response(
                {"error": "Ubicación no encontrada"}, status=status.HTTP_404_NOT_FOUND
            )

        location, _ = Location.objects.get_or_create(
            city=city, country=country, defaults={"latitude": lat, "longitude": lon}
        )

        # 2. Obtener datos del clima
        weather_data = fetch_weather_by_coords(lat, lon)
        if not weather_data:
            return Response(
                {"error": "Error al consultar el clima"},
                status=status.HTTP_503_SERVICE_UNAVAILABLE,
            )

        # 3. Guardar en la base de datos
        weather_record = WeatherData.objects.create(
            location=location,
            temperature=weather_data["main"]["temp"],
            humidity=weather_data["main"]["humidity"],
            wind_speed=weather_data["wind"]["speed"],
            description=weather_data["weather"][0]["description"],
        )

        # 4. Retornar datos serializados
        serializer = WeatherDataSerializer(weather_record)
        return Response(serializer.data)
