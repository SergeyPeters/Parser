# подключаем библиотеку для работы с запросами
import requests
# указываем город
city = input()
# формируем запрос
url = 'https://api.openweathermap.org/data/2.5/weather?q='+city+'&units=metric&lang=ru&appid=79d1ca96933b0328e1c7e3e7a26cb347'
# отправляем запрос на сервер и сразу получаем результат
weather_data = requests.get(url).json()
# получаем данные о температуре и о том, как она ощущается
temperature = round(weather_data['main']['temp'])
temperature_feels = round(weather_data['main']['feels_like'])
humidity = round(weather_data['main']['humidity'])
wind_speed = round(weather_data['wind']['speed'])
clouds = round(weather_data['clouds']['all'])
cloudiness = ['ясно', 'малооблачно', 'переменная облачность', 'облачно с прояснениями', 'преимущественно облачно,пасмурно']
print(clouds)
def find_cloudiness():
    for part in range(len(cloudiness)):
        if clouds >= (4-part)*20: return cloudiness[4-part]
# выводим значения на экран
print('Сейчас в городе', city, str(temperature), '°C')
print('Ощущается как', str(temperature_feels), '°C')
print('Влажность', str(humidity), '%')
print('Скорость ветра', str(wind_speed), 'км/ч')
print(find_cloudiness())
