from django.urls import path

from .views import predict_weather, prediction_page


urlpatterns = [
    path("", prediction_page, name="prediction-page"),
    path("predict/", predict_weather, name="predict-weather"),
]
