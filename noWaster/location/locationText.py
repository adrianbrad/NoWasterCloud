import googlemaps
from datetime import datetime
from noWaster.facebookMessage.formulate import formulateWalkingRoute, formulateTransitRoute

gmaps = googlemaps.Client(key='AIzaSyD2lAiwG69gKzptts3Z1aFcyoNYnsis7AY')
getRouteRaw = gmaps.directions

cluj_bounds = {
        "northeast" : {
            "lat" : 46.8098599743,
            "lng" : 23.6934167259
        },
        "southwest" : {
            "lat" : 46.7327321222,
            "lng" : 23.4912683136
        }
    }

def reverseGeocode(geocode):
    try:
        return gmaps.reverse_geocode(geocode)
    except:
        return None

def geocodeLocation(locationText):
    if isinstance(locationText, basestring):
        result = gmaps.geocode(locationText, region = "RO", bounds = cluj_bounds)
        if len (result) > 0:
            return (result[0]["geometry"]["location"]["lat"], result[0]["geometry"]["location"]["lng"])
    return None

def getTravelParameters(origin, dest, travelMode):
    if travelMode != "taxi":
        directionsRaw = getRouteRaw(origin, dest, travelMode, region = "RO")
        if len(directionsRaw) > 0:
            if travelMode == "walking":
                return {"routeText": formulateWalkingRoute({"distance" : directionsRaw[0]['legs'][0]["distance"]["text"]}), "routePolyline": directionsRaw[0]["overview_polyline"]["points"], "waypoints":[origin, dest], "duration" : directionsRaw[0]["legs"][0]["duration"]["text"]}
                
            if travelMode == "transit":
                directionsDictSteps = []
                directionDictsGeoloc = [origin]

                for step in directionsRaw[0]["legs"][0]["steps"]:
                    if step["travel_mode"] == "WALKING":    
                        # directionDictsGeoloc.append((step["start_location"]["lat"], step["start_location"]["lng"]))
                        directionsDictSteps.append(
                            {
                                "walking":
                                {
                                    # "start_location":(step["start_location"]["lat"], step["start_location"]["lng"]),
                                    "instructions":step["html_instructions"][8:]
                                }
                            }
                        )
                    elif step["travel_mode"] == "TRANSIT":
                        directionDictsGeoloc.append((step["start_location"]["lat"], step["start_location"]["lng"], step["transit_details"]["line"]["vehicle"]["icon"]))
                        directionDictsGeoloc.append((step["transit_details"]["arrival_stop"]["location"]["lat"], step["transit_details"]["arrival_stop"]["location"]["lng"]))
                        directionsDictSteps.append(
                            {
                                "transit":
                                {
                                    # "start_location":(step["start_location"]["lat"], step["start_location"]["lng"]),
                                    "line_number":step["transit_details"]["line"]["short_name"],
                                    "vehicle":step["transit_details"]["line"]["vehicle"]["type"],
                                    "stops":step["transit_details"]["num_stops"],
                                    "line_arrival_time":step["transit_details"]["departure_time"]["text"],
                                    "departure_station":step["transit_details"]["departure_stop"]["name"],
                                    "arrival_station":step["transit_details"]["arrival_stop"]["name"],
                                    "arrival_time":step["transit_details"]["arrival_time"]["text"]
                                }
                            }
                        )
                directionDictsGeoloc.append(dest)
                # print {"routeText": str(directionsDictSteps), "routePolyline": directionsRaw[0]["overview_polyline"]["points"], "waypoints":directionDictsGeoloc}
                return {"routeText": formulateTransitRoute(directionsDictSteps), "routePolyline": directionsRaw[0]["overview_polyline"]["points"], "waypoints":directionDictsGeoloc, "duration": directionsRaw[0]["legs"][0]["duration"]["text"]  }
    return "nu merge de data asta"

def getWalkingParameters(origin, dest):
    directionsRaw = getRouteRaw(origin, dest, "walking", region = "RO")
    if len(directionsRaw) > 0:
        return {"distance" : directionsRaw[0]['legs'][0]["distance"]["text"], "duration" : directionsRaw[0]["legs"][0]["duration"]["text"], "polyline" : directionsRaw[0]["overview_polyline"]["points"]}
    return None

def getTransitParameters(origin, dest):
    directionsRaw = getRouteRaw(origin, dest, "transit", region = "RO")
    if len(directionsRaw) > 0:
        directionsDictSteps = []
        directionDictsGeoloc = [directionsRaw[0]["overview_polyline"]["points"]]

        for step in directionsRaw[0]["legs"][0]["steps"]:
            if step["travel_mode"] == "WALKING":    
                # directionDictsGeoloc.append((step["start_location"]["lat"], step["start_location"]["lng"]))
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
                directionDictsGeoloc.append((step["transit_details"]["arrival_stop"]["location"]["lat"], step["transit_details"]["arrival_stop"]["location"]["lng"]))
                directionsDictSteps.append(
                    {
                        "transit":
                        {
                            # "start_location":(step["start_location"]["lat"], step["start_location"]["lng"]),
                            "line_number":step["transit_details"]["line"]["short_name"],
                            "vehicle":step["transit_details"]["line"]["vehicle"]["type"],
                            "stops":step["transit_details"]["num_stops"],
                            "line_arrival_time":step["transit_details"]["departure_time"]["text"],
                            "departure_station":step["transit_details"]["departure_stop"]["name"],
                            "arrival_station":step["transit_details"]["arrival_stop"]["name"],
                            "arrival_time":step["transit_details"]["arrival_time"]["text"]
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
        
