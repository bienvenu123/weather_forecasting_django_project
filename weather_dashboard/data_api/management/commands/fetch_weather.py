from django.core.management.base import BaseCommand
from data_api.services import fetch_weather

class Command(BaseCommand):
    help = 'Fetches live weather data and stores it in the database'

    def add_arguments(self, parser):
        parser.add_argument('--city', type=str, default='Kigali', help='City to fetch weather for')

    def handle(self, *args, **kwargs):
        city = kwargs['city']
        result = fetch_weather(city)
        if isinstance(result, dict) and 'error' in result:
            self.stdout.write(self.style.ERROR(f"Failed to fetch weather: {result['error']}"))
        else:
            self.stdout.write(self.style.SUCCESS(f"Fetched: {result}"))