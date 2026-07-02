from django.contrib import admin
from .models import WeatherReading

@admin.register(WeatherReading)
class WeatherReadingAdmin(admin.ModelAdmin):
    list_display = ('city', 'temperature', 'humidity', 'weather_desc', 'fetched_at')
    list_filter = ('city',)
    ordering = ('-fetched_at',)