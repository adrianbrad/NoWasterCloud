import googlemaps
from datetime import datetime
import threading

gmaps = googlemaps.Client(key='AIzaSyD2lAiwG69gKzptts3Z1aFcyoNYnsis7AY')
getRouteRaw = gmaps.directions

def reverseGeocode(geocode):
    try:
        geocode[1] = gmaps.reverse_geocode(geocode[0])
    except:
        geocode[1] = None

    return geocode[1]

def geocodeLocation(locationText):
    if isinstance(locationText[0], basestring):
        result = gmaps.geocode(locationText[0])
        if len (result) > 0:
            locationText[1] = (result[0]["geometry"]["location"]["lat"], result[0]["geometry"]["location"]["lng"])
            return locationText[1]
    return None


def getWalkingParameters(directionsRaw):
    if len(directionsRaw) > 0:
        return {"distance" : directionsRaw[0]['legs'][0]["distance"]["text"], "duration" : directionsRaw[0]["legs"][0]["duration"]["text"], "polyline" : directionsRaw[0]["overview_polyline"]["points"]}
    return None

def getTransitParameters(directionsRaw):

    return directionsRaw

def getGeocodeAndText(inputAsGeocodeOrLocation):
    listGeoC = [inputAsGeocodeOrLocation, None]
    listText = [inputAsGeocodeOrLocation, None]
    geoC = threading.Thread(target=geocodeLocation, args=(listGeoC,))
    revG = threading.Thread(target=reverseGeocode, args=(listText,))
    geoC.start()
    revG.start()
    geoC.join()
    revG.join()
    locationText = listText[1]
    geolocationCode = listGeoC[1]
    location = {}
    if geolocationCode != None:
        location["text"] = (reverseGeocode([geolocationCode,None]))[0]["formatted_address"]
        location["text"] = location["text"][0:location["text"][0:location["text"].rfind(",")].rfind(",")]
        location["geocode"] = geolocationCode
        return location
    elif locationText != None:
        location["text"] = locationText[0]["formatted_address"]
        location["text"] = location["text"][0:location["text"][0:location["text"].rfind(",")].rfind(",")]
        location["geocode"] = inputAsGeocodeOrLocation
        return location
    return None
        
