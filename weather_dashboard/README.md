# Kigali Weather Dashboard

A Django weather dashboard for Kigali that stores live weather readings, generates
machine-learning predictions, exposes REST API endpoints, and provides a
professional web interface for monitoring and reporting.

## Project Overview

The system collects current weather data from OpenWeatherMap, saves it in a
MySQL database, and uses trained ML models to predict the next temperature and
precipitation values. The project includes:

- A responsive dashboard for live readings, charts, and recent predictions
- A prediction page for generating new forecasts from the latest saved reading
- Login-protected prediction reports with CSV export
- Django REST Framework endpoints for readings and predictions
- Management commands for fetching data and running predictions
- Training files and deployed model files for the ML workflow

## Tech Stack

- Backend: Django 6, Django REST Framework
- Database: MySQL
- Machine learning: pandas, NumPy, scikit-learn, joblib
- Weather source: OpenWeatherMap API
- Frontend: Django templates, Bootstrap/AdminLTE, Chart.js, Bootstrap Icons

## Project Structure

```text
weather_dashboard/
├── accounts/              # Login, prediction report page, CSV export
├── api/                   # DRF serializers and API views
├── dashboard/             # Main dashboard page
├── data_api/              # WeatherReading model, fetch service, fetch commands
├── ml_training/           # Training dataset and model training script
├── predictor/             # Prediction model, inference, services, predictor page
├── templates/             # Shared base template and global UI styling
├── weather_dashboard/     # Django project settings and root URLs
├── manage.py
├── postman_collection.json
├── requirements.txt
└── README.md
```

## Setup Instructions

1. Create and activate a virtual environment:

```powershell
python -m venv venv
venv\Scripts\activate
```

2. Install dependencies:

```powershell
pip install -r requirements.txt
```

3. Create a `.env` file in the project root:

```env
OWM_API_KEY=your_openweathermap_api_key
```

4. Confirm the MySQL database settings in `weather_dashboard/settings.py`:

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

5. Apply migrations:

```powershell
python manage.py migrate
```

6. Start the development server:

```powershell
python manage.py runserver
```

Open the dashboard at:

```text
http://127.0.0.1:8000/
```

## Main URLs

| Page or endpoint | URL |
| --- | --- |
| Dashboard | `http://127.0.0.1:8000/` |
| Predictor page | `http://127.0.0.1:8000/predictor/` |
| Predictor JSON endpoint | `http://127.0.0.1:8000/predictor/predict/` |
| API root | `http://127.0.0.1:8000/api/` |
| Weather readings API | `http://127.0.0.1:8000/api/weather-readings/` |
| Predictions API | `http://127.0.0.1:8000/api/predictions/` |
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

## Machine Learning Workflow

The ML training files are in `ml_training/`. The project uses historical Kigali
weather data to train two models:

- Temperature model: predicts next temperature
- Precipitation model: predicts next precipitation value

Run training with:

```powershell
python ml_training\train_weather_model.py
```

The deployed model files are stored in:

```text
predictor/ml_model/
```

The inference feature order is defined in `predictor/inference.py` so the input
columns match the model training columns.

## Data Flow

1. `fetch_weather` calls the OpenWeatherMap API.
2. The returned weather values are saved as a `WeatherReading`.
3. `generate_and_save_prediction` selects the latest reading for the city.
4. `predict_next_weather` builds model features from the latest readings.
5. The temperature and precipitation models return predictions.
6. The result is saved as a `Prediction`.
7. The dashboard, reports, and API display the saved data.

## Contribution and Viva Notes

Use this section to explain your individual contribution and understanding.

### Main contribution

- Built the Django app structure with separate apps for dashboard, data fetching,
  prediction, accounts, and API.
- Implemented weather data storage using the `WeatherReading` model.
- Integrated OpenWeatherMap API fetching through a reusable service function.
- Added ML inference and prediction saving through the `Prediction` model.
- Created REST API endpoints using Django REST Framework serializers and views.
- Built the dashboard, predictor page, report page, login page, and CSV export.
- Improved the UI to make the application professional, responsive, and easier
  to present.

### What to explain in the viva

- `WeatherReading` stores real weather data such as temperature, humidity,
  pressure, wind speed, precipitation, cloud cover, and fetch time.
- `Prediction` links to a `WeatherReading`, which shows exactly which input data
  was used for each forecast.
- `data_api/services.py` handles external API communication.
- `predictor/inference.py` loads trained models once using `lru_cache`, builds
  features, and returns prediction values.
- `predictor/services.py` connects inference to the database by saving a
  `Prediction`.
- `api/serializers.py` controls how model data is converted to JSON.
- `api/views.py` provides list and generate endpoints for external clients.
- `dashboard/views.py` prepares the latest readings, predictions, and chart data
  for the template.
- Login is required for reports so exported prediction history is protected.

### Possible viva questions

**What problem does the project solve?**  
It provides a central system for collecting Kigali weather data, predicting
future values, and presenting the results through a dashboard, API, and reports.

**Why use Django REST Framework?**  
DRF makes it easier to expose model data as JSON and create API endpoints that
other clients, such as Postman or a mobile app, can consume.

**Why link Prediction to WeatherReading?**  
The foreign key keeps predictions traceable. Each forecast can be explained by
showing the exact reading used as input.

**How are models loaded efficiently?**  
`predictor/inference.py` uses `lru_cache` so model files are loaded once and
reused for later predictions.

**How can the system be improved?**  
Possible improvements include background scheduled jobs, more cities, more model
features, user-specific reports, deployment settings, and improved model
evaluation pages.

## Postman

Import `postman_collection.json` into Postman to test the main API endpoints.

## Notes

- The project expects MySQL to be running before using pages that query the
  database.
- The OpenWeatherMap API key must be available in `.env`.
- The model `.pkl` files must exist in `predictor/ml_model/` before generating
  predictions.
