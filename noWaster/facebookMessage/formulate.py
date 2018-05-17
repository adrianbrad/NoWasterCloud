from noWaster.extras.weatherCondition import weatherCondition

def formulateWalkingRoute(walkingParameters):
    return "Sunt %s pe jos" %(walkingParameters["distance"])

def formulateWeather():
    return "Tine cont ca afara sunt %s grade si e %s" % (weatherCondition["temperature"], weatherCondition["description"]+weatherCondition["emojis"])

def formulateTransitRoute(transitParameters):
    message = ""
    for param in transitParameters:
        if param.has_key("walking"):
            message = message + "Mergi pana la %s." %(param["walking"]["instructions"])
        else:
            if param["transit"]["vehicle"] == "BUS":
                message = message + " Iei busul "
            elif param["transit"]["vehicle"] == "tram":
                message = message + " Iei tramvaiul "
            else:
                message = message + " Iei "

            message = message + "%s de la %s la ora %s, ai %s opriri si ajungi la %s la ora %s. " %(param["transit"]["line_number"], param["transit"]["departure_station"], param["transit"]["line_arrival_time"], param["transit"]["stops"], param["transit"]["arrival_station"], param["transit"]["arrival_time"] )
    return message

def formulateTaxiRoute(distance, duration):
    return "%s %s" %(distance, duration)

def formulateNearbyLoc(nearbyLocParams):
    message = ""
    crtNr = 1
    for location in nearbyLocParams:
        message = message + "%i %s\n" % (crtNr, location["name"])
        crtNr += 1
    print message
    return message