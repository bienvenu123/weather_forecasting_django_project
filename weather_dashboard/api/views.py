from rest_framework.decorators import api_view
from rest_framework.response import Response

from data_api.models import WeatherReading
from predictor.models import Prediction
from predictor.services import generate_and_save_prediction

from .serializers import PredictionSerializer, WeatherReadingSerializer


@api_view(["GET"])
def api_root(request):
    return Response(
        {
            "weather_readings": request.build_absolute_uri("weather-readings/"),
            "predictions": request.build_absolute_uri("predictions/"),
            "generate_prediction": request.build_absolute_uri("generate-prediction/"),
            "predictor_page": request.build_absolute_uri("/predictor/"),
            "dashboard": request.build_absolute_uri("/"),
            "reports": request.build_absolute_uri("/accounts/reports/predictions/"),
        }
    )


@api_view(["GET"])
def weather_readings(request):
    city = request.GET.get("city")
    limit = int(request.GET.get("limit", 50))
    limit = max(1, min(limit, 200))

    readings = WeatherReading.objects.all().order_by("-fetched_at")
    if city:
        readings = readings.filter(city__iexact=city)

    serializer = WeatherReadingSerializer(readings[:limit], many=True)
    return Response(serializer.data)


@api_view(["GET"])
def predictions(request):
    city = request.GET.get("city")
    limit = int(request.GET.get("limit", 50))
    limit = max(1, min(limit, 200))

    queryset = Prediction.objects.select_related("input_reading").order_by("-predicted_at")
    if city:
        queryset = queryset.filter(input_reading__city__iexact=city)

    serializer = PredictionSerializer(queryset[:limit], many=True)
    return Response(serializer.data)


@api_view(["POST", "GET"])
def generate_prediction(request):
    city = request.data.get("city") if request.method == "POST" else request.GET.get("city")
    prediction = generate_and_save_prediction(city or "Kigali")
    serializer = PredictionSerializer(prediction)
    return Response(serializer.data, status=201)
