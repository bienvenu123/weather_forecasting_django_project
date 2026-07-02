import csv

from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.shortcuts import render

from predictor.models import Prediction


@login_required
def prediction_history(request):
    """Display saved predictions for reporting and review."""

    city = request.GET.get("city")
    predictions = Prediction.objects.select_related("input_reading").order_by("-predicted_at")
    if city:
        predictions = predictions.filter(input_reading__city__iexact=city)

    return render(
        request,
        "accounts/prediction_history.html",
        {"predictions": predictions[:100], "city": city or "All cities"},
    )


@login_required
def export_predictions_csv(request):
    """Export saved predictions as a CSV file."""

    city = request.GET.get("city")
    predictions = Prediction.objects.select_related("input_reading").order_by("-predicted_at")
    if city:
        predictions = predictions.filter(input_reading__city__iexact=city)

    response = HttpResponse(content_type="text/csv")
    response["Content-Disposition"] = 'attachment; filename="weather_predictions.csv"'

    writer = csv.writer(response)
    writer.writerow(
        [
            "Prediction ID",
            "City",
            "Input Reading ID",
            "Input Reading Time",
            "Predicted Temperature C",
            "Predicted Precipitation mm",
            "Model Used",
            "Predicted At",
        ]
    )
    for prediction in predictions:
        writer.writerow(
            [
                prediction.id,
                prediction.input_reading.city,
                prediction.input_reading_id,
                prediction.input_reading.fetched_at,
                prediction.predicted_temperature,
                prediction.predicted_precipitation,
                prediction.model_used,
                prediction.predicted_at,
            ]
        )

    return response
