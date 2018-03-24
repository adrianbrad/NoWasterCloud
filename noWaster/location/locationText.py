import googlemaps
from datetime import datetime

gmaps = googlemaps.Client(key='AIzaSyD2lAiwG69gKzptts3Z1aFcyoNYnsis7AY')
getRouteRaw = gmaps.directions

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

# def getRouteRaw(origin, dest, tavelMode, startTime):
#     return gmaps.directions(origin,
#                             dest,
#                             mode=tavelMode,
#                             departure_time=startTime)

def getWalkingParameters(directionsRaw):
    if len(directionsRaw) > 0:
        return {"distance" : directionsRaw[0]['legs'][0]["distance"]["text"], "duration" : directionsRaw[0]["legs"][0]["duration"]["text"], "polyline" : directionsRaw[0]["overview_polyline"]["points"]}
    return None

def getTransitParameters(directionsRaw):
    if len(directionsRaw) > 0:
        directionsDictSteps = []
        directionDictsGeoloc = [directionsRaw[0]["overview_polyline"]["points"]]

        for step in directionsRaw[0]["legs"][0]["steps"]:
            if step["travel_mode"] == "WALKING":    
                directionDictsGeoloc.append((step["start_location"]["lat"], step["start_location"]["lng"]))
                directionsDictSteps.append(
                    {
                        "walking":
                        {
                            # "start_location":(step["start_location"]["lat"], step["start_location"]["lng"]),
                            "instructions":step["html_instructions"]
                        }
                    }
                )
            elif step["travel_mode"] == "TRANSIT":
                directionDictsGeoloc.append((step["start_location"]["lat"], step["start_location"]["lng"], step["transit_details"]["line"]["vehicle"]["icon"]))
                directionsDictSteps.append(
                    {
                        "transit":
                        {
                            # "start_location":(step["start_location"]["lat"], step["start_location"]["lng"]),
                            "instructions":step["html_instructions"],
                            "line_number":step["transit_details"]["line"]["short_name"],
                            "vehicle":step["transit_details"]["line"]["vehicle"]["type"],
                            "stops":step["transit_details"]["num_stops"],
                            "line_arrival_time":step["transit_details"]["departure_time"]["text"]
                        }
                    }
                )
        return (directionDictsGeoloc, directionsDictSteps)
        
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
        
