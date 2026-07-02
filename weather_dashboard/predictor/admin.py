from django.contrib import admin

from .models import Prediction


@admin.register(Prediction)
class PredictionAdmin(admin.ModelAdmin):
    list_display = (
        "input_reading",
        "predicted_temperature",
        "predicted_precipitation",
        "model_used",
        "predicted_at",
    )
    list_filter = ("model_used", "predicted_at")
    search_fields = ("input_reading__city",)
    readonly_fields = ("predicted_at",)
