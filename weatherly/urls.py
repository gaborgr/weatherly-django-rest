"""
URL configuration for weatherly project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""

from django.contrib import admin
from django.urls import path, include
from drf_yasg.views import get_schema_view
from drf_yasg import openapi
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)

schema_view = get_schema_view(
    openapi.Info(
        title="Weatherly API",
        default_version="v1",
        description="API para consultar datos climáticos con autenticación JWT",
        terms_of_service="https://www.google.com/policies/terms/",
        contact=openapi.Contact(email="contact@weatherly.local"),
        license=openapi.License(name="BSD License"),
    ),
    public=True,
)

urlpatterns = [
    # Admin
    path("admin/", admin.site.urls),
    # Frontend (Django Templates)
    path("", include("weather.frontend_urls")),  # 👈 Nuevo archivo para frontend
    # API
    path("api/", include("weather.urls")),  # Tus endpoints API (/api/weather/)
    # Autenticación JWT (centralizada aquí)
    path("api/token/", TokenObtainPairView.as_view(), name="token_obtain_pair"),
    path("api/token/refresh/", TokenRefreshView.as_view(), name="token_refresh"),
    # Documentación
    path(
        "swagger/",
        schema_view.with_ui("swagger", cache_timeout=0),
        name="schema-swagger-ui",
    ),
]
