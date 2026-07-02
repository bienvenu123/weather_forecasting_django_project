from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status

from data_api.models import WeatherReading
from predictor.models import Prediction
from predictor.services import generate_and_save_prediction

from .serializers import PredictionSerializer, WeatherReadingSerializer


def _parse_limit(request, default=50, maximum=200):
    """Return a safe queryset limit from the request query string."""

    raw_limit = request.GET.get("limit", default)
    try:
        limit = int(raw_limit)
    except (TypeError, ValueError):
        return None
    return max(1, min(limit, maximum))


@api_view(["GET"])
def api_root(request):
    """List the main API and web endpoints."""

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
    """Return recent weather readings, optionally filtered by city."""

    city = request.GET.get("city")
    limit = _parse_limit(request)
    if limit is None:
        return Response(
            {"error": "limit must be a number between 1 and 200"},
            status=status.HTTP_400_BAD_REQUEST,
        )

    readings = WeatherReading.objects.all().order_by("-fetched_at")
    if city:
        readings = readings.filter(city__iexact=city)

    serializer = WeatherReadingSerializer(readings[:limit], many=True)
    return Response(serializer.data)


@api_view(["GET"])
def predictions(request):
    """Return recent predictions, optionally filtered by city."""

    city = request.GET.get("city")
    limit = _parse_limit(request)
    if limit is None:
        return Response(
            {"error": "limit must be a number between 1 and 200"},
            status=status.HTTP_400_BAD_REQUEST,
        )

    queryset = Prediction.objects.select_related("input_reading").order_by("-predicted_at")
    if city:
        queryset = queryset.filter(input_reading__city__iexact=city)

    serializer = PredictionSerializer(queryset[:limit], many=True)
    return Response(serializer.data)


@api_view(["POST", "GET"])
def generate_prediction(request):
    """Generate, save, and return a new prediction for the selected city."""

    city = request.data.get("city") if request.method == "POST" else request.GET.get("city")
    prediction = generate_and_save_prediction(city or "Kigali")
    serializer = PredictionSerializer(prediction)
    return Response(serializer.data, status=status.HTTP_201_CREATED)
