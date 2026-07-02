from django.core.management.base import BaseCommand

from predictor.services import generate_and_save_prediction


class Command(BaseCommand):
    help = "Generates a weather prediction from the latest reading and saves it"

    def add_arguments(self, parser):
        parser.add_argument("--city", type=str, default="Kigali")

    def handle(self, *args, **kwargs):
        city = kwargs["city"]
        try:
            prediction = generate_and_save_prediction(city)
        except ValueError as exc:
            self.stdout.write(self.style.ERROR(str(exc)))
            return
        except FileNotFoundError as exc:
            self.stdout.write(self.style.ERROR(f"Model file not found: {exc}"))
            return

        self.stdout.write(
            self.style.SUCCESS(
                "Prediction saved: "
                f"{prediction.predicted_temperature}°C, "
                f"{prediction.predicted_precipitation}mm at "
                f"{prediction.predicted_at}"
            )
        )
