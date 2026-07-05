# Kigali Weather Dashboard

A Django weather dashboard for Kigali, Rwanda that stores live weather readings,
generates machine-learning predictions, exposes REST API endpoints, and provides
a web dashboard for monitoring and reporting.

## Domain Chosen

The selected domain is weather monitoring and forecasting. The system focuses on
Kigali weather data and helps users view recent weather conditions, generate
temperature and precipitation forecasts, and export prediction history for
reporting.

## API Used

The project uses the OpenWeatherMap Current Weather API:

- Base endpoint: `https://api.openweathermap.org/data/2.5/weather`
- Default city: Kigali
- Units: metric
- API key setting: `OWM_API_KEY` in `.env`

The API response is saved in the local database as a `WeatherReading`, including
temperature, feels-like temperature, humidity, pressure, weather description,
wind speed, precipitation, cloud cover, and fetch timestamp.

## Tech Stack

- Backend: Django 6, Django REST Framework
- Database: MySQL
- Machine learning: pandas, NumPy, scikit-learn, joblib
- Weather source: OpenWeatherMap API
- Frontend: Django templates, Bootstrap/AdminLTE, Chart.js, Bootstrap Icons

## Project Structure

```text
weather_dashboard/
|-- accounts/              # Login, prediction report page, CSV export
|-- api/                   # DRF serializers and API views
|-- dashboard/             # Main dashboard page
|-- data_api/              # WeatherReading model, fetch service, fetch commands
|-- ml_training/           # Training dataset and model training script
|-- predictor/             # Prediction model, inference, services, predictor page
|-- templates/             # Shared base template and global UI styling
|-- weather_dashboard/     # Django project settings and root URLs
|-- manage.py
|-- postman_collection.json
|-- requirements.txt
`-- README.md
```

## Setup and Run Instructions

1. Create and activate a virtual environment:

```powershell
python -m venv venv
venv\Scripts\activate
```

2. Install dependencies:

```powershell
pip install -r requirements.txt
```

3. Create a `.env` file in the project root, next to `manage.py`:

```env
OWM_API_KEY=your_openweathermap_api_key
```

4. Confirm the MySQL database exists and matches the settings in
   `weather_dashboard/settings.py`.

5. Apply migrations:

```powershell
python manage.py migrate
```

6. Start the development server:

```powershell
python manage.py runserver
```

7. Open the dashboard:

```text
http://127.0.0.1:8000/
```

## Database Connection Notes

The project is configured for MySQL in `weather_dashboard/settings.py`:

```python
DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.mysql",
        "NAME": "final",
        "USER": "root",
        "PASSWORD": "123Dative@",
        "HOST": "localhost",
        "PORT": "3306",
    }
}
```

Before running migrations, make sure:

- MySQL Server is installed and running.
- A database named `final` exists.
- The configured user has permission to create and update tables.
- `mysqlclient` installs successfully from `requirements.txt`.

Example MySQL setup:

```sql
CREATE DATABASE final;
```

## Main URLs

| Page or endpoint | URL |
| --- | --- |
| Dashboard | `http://127.0.0.1:8000/` |
| Predictor page | `http://127.0.0.1:8000/predictor/` |
| Predictor JSON endpoint | `http://127.0.0.1:8000/predictor/predict/` |
| API root | `http://127.0.0.1:8000/api/` |
| Weather readings API | `http://127.0.0.1:8000/api/weather-readings/` |
| Weather reading detail API | `http://127.0.0.1:8000/api/weather-readings/<id>/` |
| Predictions API | `http://127.0.0.1:8000/api/predictions/` |
| Prediction detail API | `http://127.0.0.1:8000/api/predictions/<id>/` |
| Generate prediction API | `http://127.0.0.1:8000/api/generate-prediction/` |
| Reports | `http://127.0.0.1:8000/accounts/reports/predictions/` |
| CSV export | `http://127.0.0.1:8000/accounts/reports/predictions.csv` |
| Admin | `http://127.0.0.1:8000/admin/` |

## Useful Commands

Fetch and save live weather data:

```powershell
python manage.py fetch_weather --city Kigali
```

Generate a prediction from the latest saved reading:

```powershell
python manage.py predict_weather --city Kigali
```

Fetch live data and immediately generate a prediction:

```powershell
python manage.py fetch_and_predict --city Kigali
```

Create an admin user:

```powershell
python manage.py createsuperuser
```

## API Usage

Get recent readings:

```text
GET /api/weather-readings/?city=Kigali&limit=10
```

Create a weather reading:

```text
POST /api/weather-readings/
Content-Type: application/json

{
  "city": "Kigali",
  "temperature": 24.5,
  "feels_like": 24.0,
  "humidity": 70,
  "pressure": 1013,
  "weather_desc": "clear sky",
  "wind_speed": 3.2,
  "precipitation": 0,
  "cloud_cover": 15
}
```

Get recent predictions:

```text
GET /api/predictions/?city=Kigali&limit=10
```

Generate a new prediction:

```text
POST /api/generate-prediction/
Content-Type: application/json

{
  "city": "Kigali"
}
```

The `limit` query parameter is clamped between 1 and 200.

## ML Model Summary

The ML workflow is in `ml_training/train_weather_model.py`. It trains two
separate regression models using `ml_training/kigali_weather_history.csv`.

- Temperature model: Linear Regression
- Precipitation model: Random Forest Regressor
- Features: lagged temperature, humidity, pressure, wind speed, precipitation,
  cloud cover, and a three-reading rolling temperature average
- Split method: chronological train/test split with `shuffle=False`
- Evaluation metrics: MAE, RMSE, and R2
- Baseline check: naive persistence forecast for temperature
- Export format: `.pkl` files saved with `joblib`

Run the training/evaluation/export script:

```powershell
python ml_training\train_weather_model.py
```

Training exports models to:

```text
ml_training/temperature_model.pkl
ml_training/precipitation_model.pkl
```

The deployed copies used by the Django app are stored in:

```text
predictor/ml_model/temperature_model.pkl
predictor/ml_model/precipitation_model.pkl
```

Inference uses the same feature order defined in `predictor/inference.py`.

## Data Flow

1. `fetch_weather` calls the OpenWeatherMap API.
2. The returned weather values are saved as a `WeatherReading`.
3. `generate_and_save_prediction` selects the latest reading for the city.
4. `predict_next_weather` builds model features from recent readings.
5. The temperature and precipitation models return predictions.
6. The result is saved as a `Prediction`.
7. The dashboard, reports, and API display the saved data.

## Submission Checklist

- Complete Django source code: this project folder.
- Pinned dependencies: `requirements.txt`.
- README with domain, API, setup/run, database notes, and ML summary: this file.
- ML training/evaluation/export artifact: `ml_training/train_weather_model.py`.
- Group contribution sheet: `GROUP_CONTRIBUTIONS.md`.
- API testing collection: `postman_collection.json`.

## Postman

Import `postman_collection.json` into Postman to test the main API endpoints.

## Notes

- The project expects MySQL to be running before using pages that query the
  database.
- The OpenWeatherMap API key must be available in `.env`.
- The model `.pkl` files must exist in `predictor/ml_model/` before generating
  predictions.
