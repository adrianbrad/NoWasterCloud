import googlemaps
from datetime import datetime

gmaps = googlemaps.Client(key='AIzaSyD2lAiwG69gKzptts3Z1aFcyoNYnsis7AY')

def reverseGeocode(geocode):
    try:
        return gmaps.reverse_geocode(geocode)
    except:
        return None

def geocodeLocation(locationText):
    if isinstance(locationText, basestring):
        result = gmaps.geocode(locationText)
        if len (result) > 0:
            return (result[0]["geometry"]["location"]["lat"], result[0]["geometry"]["location"]["lng"])
    return None

# def check

def getRouteRaw(origin, dest, tavelMode):
    return gmaps.directions(origin,
                            dest,
                            mode=tavelMode,
                            departure_time=datetime.now())

def getWalkingParameters(directionsRaw):
    if len(directionsRaw) > 0:
        return {"distance" : directionsRaw[0]['legs'][0]["distance"]["text"], "duration" : directionsRaw[0]["legs"][0]["duration"]["text"], "polyline" : directionsRaw[0]["overview_polyline"]["points"]}
    return None

def getGeocodeAndText(inputAsGeocodeOrLocation):
    geolocationCode = geocodeLocation(inputAsGeocodeOrLocation)
    locationText = reverseGeocode(inputAsGeocodeOrLocation)
    location = {}
    if geolocationCode != None:
        location["text"] = reverseGeocode(geolocationCode)[0]["formatted_address"]
        location["text"] = location["text"][0:location["text"][0:location["text"].rfind(",")].rfind(",")]
        location["geocode"] = geolocationCode
        return location
    elif locationText != None:
        location["text"] = locationText[0]["formatted_address"]
        location["text"] = location["text"][0:location["text"][0:location["text"].rfind(",")].rfind(",")]
        location["geocode"] = inputAsGeocodeOrLocation
        return location
    return None
        
