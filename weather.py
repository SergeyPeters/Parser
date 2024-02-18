# подключаем библиотеку для работы с запросами
import requests

def get_weather():
    city = open('City').readline()
    url = 'https://api.openweathermap.org/data/2.5/weather?q='+city+'&units=metric&lang=ru&appid=79d1ca96933b0328e1c7e3e7a26cb347'
    weather_data = requests.get(url).json()
    temperature = round(weather_data['main']['temp'])
    humidity = round(weather_data['main']['humidity'])
    wind_speed = round(weather_data['wind']['speed'])
    clouds = round(weather_data['clouds']['all'])
    cloudiness = ['ясно', 'переменная облачность', 'преимущественно облачно,пасмурно']

    def find_cloudiness():
        for part in range(len(cloudiness)):
            if clouds >= (2-part)*20: return 2-part
    return str(temperature), str(humidity), str(wind_speed), find_cloudiness()
