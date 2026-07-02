from django.db import models
from data_api.models import WeatherReading

class Prediction(models.Model):
    input_reading = models.ForeignKey(WeatherReading, on_delete=models.CASCADE, related_name='predictions')
    predicted_temperature = models.FloatField()
    predicted_precipitation = models.FloatField()
    model_used = models.CharField(max_length=100, default="LinearRegression+RandomForest")
    predicted_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Prediction for {self.input_reading.city} @ {self.predicted_at}: {self.predicted_temperature}°C"