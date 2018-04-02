import threading
from weather import Weather
from weather.objects.weather_obj import WeatherObject
from noWaster.models import WeatherDictionary, Emoji


weatherCondition = {"temperature": "", "description": "", "emojis":""}
weather = Weather()

def updateWeather():
    loc = weather.lookup_by_location("Cluj-Napoca")
    if loc != None:
        condition = loc.condition()
        wD = WeatherDictionary.objects.get(id = condition.code())
        weatherCondition["temperature"] = condition.temp()
        weatherCondition["description"] = wD.description
        weatherCondition["emojis"] = wD.emoji1.text.decode("unicode-escape")
        if wD.emoji2 != None:
             weatherCondition["emojis"] = wD.emoji2.text.decode("unicode-escape")

    
    threading.Timer(1800, updateWeather).start()

updateWeather()