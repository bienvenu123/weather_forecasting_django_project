from django.shortcuts import render

from data_api.models import WeatherReading
from predictor.models import Prediction


def home(request):
    city = request.GET.get("city", "Kigali")
    readings = list(
        WeatherReading.objects.filter(city__iexact=city).order_by("-fetched_at")[:24]
    )
    latest_reading = readings[0] if readings else None
    latest_prediction = (
        Prediction.objects.select_related("input_reading")
        .filter(input_reading__city__iexact=city)
        .order_by("-predicted_at")
        .first()
    )

    chart_readings = list(reversed(readings[:12]))
    chart_labels = [reading.fetched_at.strftime("%H:%M") for reading in chart_readings]
    temperatures = [reading.temperature for reading in chart_readings]
    humidity = [reading.humidity for reading in chart_readings]

    recent_predictions = (
        Prediction.objects.select_related("input_reading")
        .filter(input_reading__city__iexact=city)
        .order_by("-predicted_at")[:10]
    )

    return render(
        request,
        "dashboard/home.html",
        {
            "city": city,
            "latest_reading": latest_reading,
            "latest_prediction": latest_prediction,
            "recent_readings": readings[:10],
            "recent_predictions": recent_predictions,
            "chart_labels": chart_labels,
            "temperatures": temperatures,
            "humidity": humidity,
        },
    )
