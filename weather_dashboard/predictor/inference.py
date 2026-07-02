from functools import lru_cache

import joblib
import pandas as pd
from django.conf import settings

from data_api.models import WeatherReading


FEATURE_SET = [
    "temperature_celsius_lag1",
    "humidity_lag1",
    "pressure_mb_lag1",
    "wind_kph_lag1",
    "precip_mm_lag1",
    "cloud_lag1",
    "temp_roll3",
]

MODEL_DIR = settings.BASE_DIR / "predictor" / "ml_model"
TEMPERATURE_MODEL_PATH = MODEL_DIR / "temperature_model.pkl"
PRECIPITATION_MODEL_PATH = MODEL_DIR / "precipitation_model.pkl"


@lru_cache(maxsize=1)
def _load_models():
    return {
        "temperature": joblib.load(TEMPERATURE_MODEL_PATH),
        "precipitation": joblib.load(PRECIPITATION_MODEL_PATH),
    }


def _wind_mps_to_kph(wind_speed):
    return float(wind_speed or 0.0) * 3.6


def _build_feature_frame(readings):
    latest = readings[0]
    temp_values = [float(reading.temperature) for reading in readings[:3]]
    temp_roll3 = sum(temp_values) / len(temp_values)

    features = {
        "temperature_celsius_lag1": float(latest.temperature),
        "humidity_lag1": float(latest.humidity),
        "pressure_mb_lag1": float(latest.pressure),
        "wind_kph_lag1": _wind_mps_to_kph(latest.wind_speed),
        "precip_mm_lag1": float(latest.precipitation or 0.0),
        "cloud_lag1": float(latest.cloud_cover or 0.0),
        "temp_roll3": temp_roll3,
    }
    return pd.DataFrame([features], columns=FEATURE_SET)


def predict_next_weather(city="Kigali"):
    readings = list(
        WeatherReading.objects.filter(city__iexact=city).order_by("-fetched_at")[:3]
    )
    if not readings:
        raise ValueError(
            f"No weather readings found for {city}. Run `python manage.py fetch_weather --city {city}` first."
        )

    models = _load_models()
    feature_frame = _build_feature_frame(readings)

    temperature = float(models["temperature"].predict(feature_frame)[0])
    precipitation = max(0.0, float(models["precipitation"].predict(feature_frame)[0]))

    latest = readings[0]
    return {
        "city": latest.city,
        "based_on_reading_id": latest.id,
        "based_on_fetched_at": latest.fetched_at.isoformat(),
        "readings_used": len(readings),
        "predicted_temperature_celsius": round(temperature, 2),
        "predicted_precipitation_mm": round(precipitation, 3),
        "features": {
            name: round(float(feature_frame.iloc[0][name]), 3) for name in FEATURE_SET
        },
    }
