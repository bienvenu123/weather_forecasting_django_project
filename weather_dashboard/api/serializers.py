from rest_framework import serializers

from data_api.models import WeatherReading
from predictor.models import Prediction


class WeatherReadingSerializer(serializers.ModelSerializer):
    class Meta:
        model = WeatherReading
        fields = [
            "id",
            "city",
            "temperature",
            "feels_like",
            "humidity",
            "pressure",
            "weather_desc",
            "wind_speed",
            "precipitation",
            "cloud_cover",
            "fetched_at",
        ]


class PredictionSerializer(serializers.ModelSerializer):
    city = serializers.CharField(source="input_reading.city", read_only=True)
    input_fetched_at = serializers.DateTimeField(
        source="input_reading.fetched_at", read_only=True
    )

    class Meta:
        model = Prediction
        fields = [
            "id",
            "city",
            "input_reading",
            "input_fetched_at",
            "predicted_temperature",
            "predicted_precipitation",
            "model_used",
            "predicted_at",
        ]
        read_only_fields = fields