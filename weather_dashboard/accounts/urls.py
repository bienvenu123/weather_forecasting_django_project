from django.contrib.auth import views as auth_views
from django.urls import path

from . import views


urlpatterns = [
    path("login/", auth_views.LoginView.as_view(), name="login"),
    path("logout/", auth_views.LogoutView.as_view(), name="logout"),
    path("reports/predictions/", views.prediction_history, name="prediction-history"),
    path(
        "reports/predictions.csv",
        views.export_predictions_csv,
        name="export-predictions-csv",
    ),
]
