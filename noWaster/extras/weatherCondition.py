import threading
from weather import Weather
from weather.objects.weather_obj import WeatherObject

weatherCondition = {"temperature": "", "code": -1}
weather = Weather()

def updateWeather():
    loc = weather.lookup_by_location("Cluj-Napoca")
    condition = loc.condition()
    weatherCondition["temperature"] = condition.temp()
    weatherCondition["code"] = condition.code()
    threading.Timer(1800, updateWeather).start()

updateWeather()