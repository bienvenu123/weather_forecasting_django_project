from .inference import predict_next_weather
from .models import Prediction
from data_api.models import WeatherReading


def generate_and_save_prediction(city="Kigali"):
    """
    Runs the ML prediction using the latest weather reading and saves
    the result into the Prediction table with a timestamp.
    """
    result = predict_next_weather(city)

    reading = WeatherReading.objects.get(id=result["based_on_reading_id"])

    prediction = Prediction.objects.create(
        input_reading=reading,
        predicted_temperature=result["predicted_temperature_celsius"],
        predicted_precipitation=result["predicted_precipitation_mm"],
        model_used="LinearRegression (temp) + RandomForest (precip)",
    )
    return prediction