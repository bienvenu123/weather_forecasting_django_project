from django.core.management.base import BaseCommand

from data_api.services import fetch_weather
from predictor.services import generate_and_save_prediction


class Command(BaseCommand):
    help = "Fetches live weather data, then generates and saves an ML prediction"

    def add_arguments(self, parser):
        parser.add_argument("--city", type=str, default="Kigali")

    def handle(self, *args, **kwargs):
        city = kwargs["city"]
        result = fetch_weather(city)
        if isinstance(result, dict) and "error" in result:
            self.stdout.write(self.style.ERROR(f"Failed to fetch weather: {result['error']}"))
            return

        prediction = generate_and_save_prediction(city)
        self.stdout.write(
            self.style.SUCCESS(
                "Fetched weather and saved prediction: "
                f"{prediction.predicted_temperature}°C, "
                f"{prediction.predicted_precipitation}mm at "
                f"{prediction.predicted_at}"
            )
        )
