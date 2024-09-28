from django.shortcuts import render
import json
import urllib.request
from urllib.parse import quote
from urllib.error import HTTPError
from .models import Weather 

def index(request):
    weather_records = Weather.objects.all().order_by('-created_at')[:5]  # Fetch last 5 records

    if request.method == 'POST':
        city = request.POST['city']
        city_encoded = quote(city)

        try:
            # Try to get the weather data from OpenWeather API
            source = urllib.request.urlopen('http://api.openweathermap.org/data/2.5/weather?q=' + city_encoded + '&units=metric&appid=<CHANGE-YOUR-API-KEY>').read()
            list_of_data = json.loads(source)

            # Check if the API returned valid data
            if list_of_data.get('cod') != 200:  # 200 means successful response
                context = {
                    'error_message': 'City not found. Please try again.',
                    'weather_records': weather_records,
                }
                return render(request, "main/index.html", context)

            # Process the weather data if valid
            data = {
                "country_code": str(list_of_data['sys']['country']),
                "coordinates": str(list_of_data['coord']['lon']) + ', ' + str(list_of_data['coord']['lat']),
                "temperature": list_of_data['main']['temp'],
                "pressure": list_of_data['main']['pressure'],
                "humidity": list_of_data['main']['humidity'],
                'weather_main': str(list_of_data['weather'][0]['main']),
                'weather_description': str(list_of_data['weather'][0]['description']),
                'weather_icon': list_of_data['weather'][0]['icon'],
            }

            # Save to the database
            weather_record = Weather.objects.create(
                city=city,
                country_code=data['country_code'],
                coordinates=data['coordinates'],
                temperature=data['temperature'],
                pressure=data['pressure'],
                humidity=data['humidity'],
                weather_main=data['weather_main'],
                weather_description=data['weather_description'],
                weather_icon=data['weather_icon']
            )

            context = {
                'country_code': data['country_code'],
                'coordinate': data['coordinates'],
                'temp': data['temperature'],
                'pressure': data['pressure'],
                'humidity': data['humidity'],
                'main': data['weather_main'],
                'description': data['weather_description'],
                'icon': data['weather_icon'],
                'weather_record': weather_record,
                'weather_records': weather_records,
            }

        except HTTPError as e:
            # If there's an HTTP error (e.g., city not found), return an error message
            context = {
                'error_message': 'City not found. Please try again.',
                'weather_records': weather_records,
            }

        except Exception as e:
            # Catch any other exceptions and return a generic error message
            context = {
                'error_message': 'An error occurred. Please try again later.',
                'weather_records': weather_records,
            }

    else:
        context = {'weather_records': weather_records}

    return render(request, "main/index.html", context)
