from django.http import JsonResponse
from django.shortcuts import render

from .services import generate_and_save_prediction


def prediction_page(request):
    city = request.GET.get("city", "Kigali")
    prediction = None
    error = None

    if request.method == "POST":
        city = request.POST.get("city") or "Kigali"
        try:
            prediction = generate_and_save_prediction(city=city)
        except ValueError as exc:
            error = str(exc)
        except FileNotFoundError as exc:
            error = f"Model file not found: {exc}"

    return render(
        request,
        "predictor/predict.html",
        {"city": city, "prediction": prediction, "error": error},
    )


def predict_weather(request):
    city = request.GET.get("city", "Kigali")
    try:
        prediction = generate_and_save_prediction(city=city)
    except ValueError as exc:
        return JsonResponse({"error": str(exc)}, status=400)
    except FileNotFoundError as exc:
        return JsonResponse({"error": f"Model file not found: {exc}"}, status=500)

    return JsonResponse(
        {
            "id": prediction.id,
            "city": prediction.input_reading.city,
            "based_on_reading_id": prediction.input_reading_id,
            "based_on_fetched_at": prediction.input_reading.fetched_at.isoformat(),
            "predicted_temperature_celsius": prediction.predicted_temperature,
            "predicted_precipitation_mm": prediction.predicted_precipitation,
            "model_used": prediction.model_used,
            "predicted_at": prediction.predicted_at.isoformat(),
        }
    )
