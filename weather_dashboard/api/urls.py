from django.urls import path

from . import views


urlpatterns = [
    path("", views.api_root, name="api-root"),
    path("weather-readings/", views.weather_readings, name="api-weather-readings"),
    path("predictions/", views.predictions, name="api-predictions"),
    path("generate-prediction/", views.generate_prediction, name="api-generate-prediction"),
]
