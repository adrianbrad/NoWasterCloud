from location.locationText import getGeocodeAndText, getRouteRaw, getTravelParameters, getNearbyLocationsList
from facebookMessage.sender import locationOptionsButton, dynamicQuickReplyButton, postFacebookMessage, postFacebookImageFromUrl, postSendLocationQuickReply, postTravelModeButtons, postTemplateTextButtons, postAskWhatToDoWithLocation, postAskForLocGetNearbyLocGetRoute, postAskForLocGetNearbyLoc
from location.locationPicture import pictureUrlForRoute, locationsPicture
from extras.weatherCondition import weatherCondition
from facebookMessage.formulate import formulateWeather, formulateNearbyLoc

def getStarted(messageTypeContent, senderID, usr):
    postFacebookMessage(senderID, "Mesaj de intampinare %s %s" % (usr.first_name, usr.last_name))
    setStageOne(senderID, usr)

def setStageOne(senderID, usr):
    postSendLocationQuickReply(senderID, "Trimite-mi locatia de pornire")
    usr.stage = 1
    
def setStageTwo(senderID, usr):
    postSendLocationQuickReply(senderID, "Trimite-mi locatia unde vrei sa ajungi")
    usr.stage = 2

def stageOne(messageTypeContent, senderID, usr): #sets the origin location
    if messageTypeContent["type"] == "location" or messageTypeContent["type"] == "text":
        loc = getGeocodeAndText(messageTypeContent["content"])
        if loc == None:
            postSendLocationQuickReply(senderID, "locatia nu e valida, mai incearca o data") 
        else:
            usr.origin_loc_address = loc["text"]
            usr.origin_loc_lat = loc["geocode"][0]
            usr.origin_loc_lng = loc["geocode"][1]
            print str((usr.origin_loc_lat,usr.origin_loc_lng ))
            postFacebookMessage(senderID, "Ai setat %s ca adresa de pornire" % (usr.origin_loc_address))
            if len(usr.dest_loc_address) > 0:
                postAskForLocGetNearbyLocGetRoute(senderID, "Trimite-mi o noua locatie unde vrei sa ajungi, sau vezi ce localuri sunt imprejur, sau obtine o ruta pentru locatiile curente")
            else:
                postAskForLocGetNearbyLoc(senderID, "Trimite-mi o locatie unde vrei sa ajungi, sau vezi ce localuri sunt imprejur")
            usr.stage = 2
    return

def stageTwo(messageTypeContent, senderID, usr):
    if messageTypeContent["type"] == "location" or messageTypeContent["type"] == "text":
        loc = getGeocodeAndText(messageTypeContent["content"])

        if loc == None:
            postSendLocationQuickReply(senderID, "locatia nu e valida, mai incearca o data") 

        else:
            usr.dest_loc_address = loc["text"]
            usr.dest_loc_lat = loc["geocode"][0]
            usr.dest_loc_lng = loc["geocode"][1]
            postFacebookMessage(senderID, "Ai setat %s ca destinatie" % (usr.dest_loc_address))
            if len(usr.origin_loc_address) > 0:
                postAskForLocGetNearbyLocGetRoute(senderID, "Schimba locatia de origine, vezi ce localuri sunt imprejur, sau obtine o ruta pentru locatiile curente")
            else:
                postAskForLocGetNearbyLoc(senderID, "Schimba locatia de origine sau vezi ce localuri sunt imprejur")

            usr.stage = 3
    return

def stageThree(messageTypeContent, senderID, usr):
    if messageTypeContent["type"] == "location" or messageTypeContent["type"] == "text":
        loc = getGeocodeAndText(messageTypeContent["content"])
        if loc != None:
            usr.origin_loc_address = loc["text"]
            usr.origin_loc_lat = loc["geocode"][0]
            usr.origin_loc_lng = loc["geocode"][1]
            postFacebookMessage(senderID, "Ai setat %s ca adresa de pornire" % (usr.origin_loc_address))
        if len(usr.dest_loc_address) > 0:
            postAskForLocGetNearbyLocGetRoute(senderID, "Trimite-mi o noua locatie unde vrei sa ajungi, sau vezi ce localuri sunt imprejur, sau obtine o ruta pentru locatiile curente")
        else:
            postAskForLocGetNearbyLoc(senderID, "Trimite-mi o locatie unde vrei sa ajungi, sau vezi ce localuri sunt imprejur")
        usr.stage = 2
    
    elif messageTypeContent["type"] == "quick_reply" and messageTypeContent["content"] == "get_route":
        postTemplateTextButtons(senderID, usr.origin_loc_address, (usr.origin_loc_lat,  usr.origin_loc_lng), usr.dest_loc_address, (usr.dest_loc_lat, usr.dest_loc_lng))
        usr.stage = 4

    elif messageTypeContent["type"] == "quick_reply" and messageTypeContent["content"] == "locations_near":
        pass

def setStageFour(senderID, usr):
    postTemplateTextButtons(senderID, usr.origin_loc_address, (usr.origin_loc_lat,  usr.origin_loc_lng), usr.dest_loc_address, (usr.dest_loc_lat, usr.dest_loc_lng))
    usr.stage = 4

def stageFour(messageTypeContent, senderID, usr):
    if messageTypeContent["type"] != "travel_postback":
        postTemplateTextButtons(senderID, usr.origin_loc_address, (usr.origin_loc_lat,  usr.origin_loc_lng), usr.dest_loc_address, (usr.dest_loc_lat, usr.dest_loc_lng))
    else:
        postFacebookMessage(senderID,formulateWeather())
        travelParameters = getTravelParameters(messageTypeContent["content"]["origin"], messageTypeContent["content"]["dest"], messageTypeContent["content"]["travel_mode"])

        if travelParameters.has_key("routePolyline"):
            postFacebookMessage(senderID, "De la %s pana la %s ar dura %s" % (usr.origin_loc_address, usr.dest_loc_address, travelParameters["duration"]))
            postFacebookMessage(senderID, travelParameters["routeText"])
            try:
                postFacebookImageFromUrl(senderID, pictureUrlForRoute(travelParameters["routePolyline"], travelParameters["waypoints"]))
            except:
                print("no picture for: %s" % (pictureUrlForRoute(walkingParameters["routePolyline"], [(usr.origin_loc_lat, usr.origin_loc_lng),(usr.dest_loc_lat, usr.dest_loc_lng)])))

            #este o eroare pe librarie de static maps(motionless) cand face quote ar trebui sa face quote(*string*.encode('utf-8))
        else: 
            postFacebookMessage(senderID, "Nu prea merge cu locatiile astea")

        setStageOne(senderID, usr)
    return

def getNearbyLocations(senderID, usr):
    locationsList = ""
    if usr.stage == 2:
        locationsList = getNearbyLocationsList((usr.origin_loc_lat, usr.origin_loc_lng))
    elif usr.stage == 3:
        locationsList = getNearbyLocationsList((usr.origin_loc_lat, usr.origin_loc_lng))

    postFacebookMessage(senderID, formulateNearbyLoc(locationsList))
    postFacebookImageFromUrl(senderID, locationsPicture((usr.origin_loc_lat, usr.origin_loc_lng), locationsList))
    dynamicQuickReplyButton(senderID, "alege una dintre locatii",locationsList)
    locationOptionsButton(senderID, "Brad")
    return

def handleUnexpectedLocation(messageTypeContent, senderID, usr):
    loc = getGeocodeAndText(messageTypeContent["content"])

    usr.temporary_loc_lat = loc["geocode"][0]
    usr.temporary_loc_lng = loc["geocode"][1]
    usr.temporary_loc_address = loc["text"]

    postAskWhatToDoWithLocation(senderID, "Ce ai vrea sa faci cu locatia asta?")
    usr.stage = 5
    return

def resolveLocation(messageTypeContent, senderID, usr):
    if messageTypeContent["type"] != "location_setter":
        postAskWhatToDoWithLocation(senderID, "Nu ma ajuti, ce ai vrea sa faci cu ultima locatie trimisa?")
    elif usr.temporary_loc_address != None:
        if messageTypeContent["content"] == "origin":
            usr.origin_loc_address = usr.temporary_loc_address
            usr.origin_loc_lat = usr.temporary_loc_lat
            usr.origin_loc_lng = usr.temporary_loc_lng

            usr.temporary_loc_address = ""
            usr.temporary_loc_lat = usr.temporary_loc_lng = None

            postTemplateTextButtons(senderID, usr.origin_loc_address, (usr.origin_loc_lat,  usr.origin_loc_lng), usr.dest_loc_address, (usr.dest_loc_lat, usr.dest_loc_lng))
            usr.stage = 3

        elif messageTypeContent["content"] == "dest":
            usr.dest_loc_address = usr.temporary_loc_address
            usr.dest_loc_lat = usr.temporary_loc_lat
            usr.dest_loc_lng = usr.temporary_loc_lng
            
            usr.temporary_loc_address = ""
            usr.temporary_loc_lat = usr.temporary_loc_lng = None

            postTemplateTextButtons(senderID, usr.origin_loc_address, (usr.origin_loc_lat,  usr.origin_loc_lng), usr.dest_loc_address, (usr.dest_loc_lat, usr.dest_loc_lng))
            usr.stage = 3

        elif messageTypeContent["content"] == "nearby":
            pass
    else:
        if messageTypeContent["content"] == "origin":
            postSendLocationQuickReply(senderID, "Trimite-mi locatia ta")

        elif messageTypeContent["content"] == "dest":
            postSendLocationQuickReply(senderID, "Trimite-mi locatia unde vrei sa ajungi")
            
        elif messageTypeContent["content"] == "nearby":
            pass
    return