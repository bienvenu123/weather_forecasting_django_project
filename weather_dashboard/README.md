# Kigali Weather Dashboard

Django weather dashboard that stores live Kigali weather readings, generates ML
temperature and precipitation predictions, exposes DRF API endpoints, and
provides a simple dashboard and report export.

## Main URLs

- Dashboard: `http://127.0.0.1:8000/`
- Admin: `http://127.0.0.1:8000/admin/`
- Prediction JSON: `http://127.0.0.1:8000/predictor/predict/`
- Weather readings API: `http://127.0.0.1:8000/api/weather-readings/`
- Predictions API: `http://127.0.0.1:8000/api/predictions/`
- Generate prediction API: `http://127.0.0.1:8000/api/generate-prediction/`
- Reports: `http://127.0.0.1:8000/accounts/reports/predictions/`
- CSV export: `http://127.0.0.1:8000/accounts/reports/predictions.csv`

## Useful Commands

```powershell
python manage.py fetch_weather --city Kigali
python manage.py predict_weather --city Kigali
python manage.py fetch_and_predict --city Kigali
python manage.py runserver
```

Use `fetch_and_predict` in Windows Task Scheduler if you want one scheduled job
that both stores the latest live reading and saves a new prediction.

## ML Training

The training script and filtered Kigali dataset are in `ml_training/`.
The deployed model files are in `predictor/ml_model/`.

```powershell
python ml_training\train_weather_model.py
```

The model feature order is preserved in `predictor/inference.py`.

## Postman

Import `postman_collection.json` into Postman. It contains the three core DRF
endpoints plus the predictor JSON endpoint.
