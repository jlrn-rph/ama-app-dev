from django.db import models

# Create your models here.
class Weather(models.Model):
    city = models.CharField(max_length=100)
    country_code = models.CharField(max_length=10)
    coordinates = models.CharField(max_length=50)
    temperature = models.FloatField()
    pressure = models.FloatField()
    humidity = models.FloatField()
    weather_main = models.CharField(max_length=50)
    weather_description = models.CharField(max_length=150)
    weather_icon = models.CharField(max_length=50)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.city}, {self.country_code} - {self.temperature}°C"
