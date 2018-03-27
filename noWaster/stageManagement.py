from location.locationText import getGeocodeAndText, getWalkingParameters, getRouteRaw, getTransitParameters
from facebookMessage.sender import postFacebookMessage, postFacebookImageFromUrl, postSendLocationQuickReply, postTravelModeButtons
from location.locationPicture import pictureUrlForRoute
from facebookMessage.formulate import formulateWalkingRoute
from extras.weatherCondition import weatherCondition

def stageZero(messageTypeContent, senderID, usr):
    postSendLocationQuickReply(senderID, "Trimite-mi locatia ta")
    usr.stage += 1
    return

def stageOne(messageTypeContent, senderID, usr):
    loc = getGeocodeAndText(messageTypeContent["content"])
    if loc == None:
        postSendLocationQuickReply(senderID, "locatia nu e valida, mai incearca o data") 

    else:
        usr.origin_loc_address = loc["text"]
        usr.origin_loc_lat = loc["geocode"][0]
        usr.origin_loc_lng = loc["geocode"][1]
        postSendLocationQuickReply(senderID, "Trimite locatia unde vrei sa ajungi")
        usr.stage += 1 
    return

def stageTwo(messageTypeContent, senderID, usr):
    loc = getGeocodeAndText(messageTypeContent["content"])

    if loc == None:
        postSendLocationQuickReply(senderID, "locatia nu e valida, mai incearca o data") 

    else:
        usr.dest_loc_address = loc["text"]
        usr.dest_loc_lat = loc["geocode"][0]
        usr.dest_loc_lng = loc["geocode"][1]
        postTravelModeButtons(senderID)
        usr.stage += 1
    return

def stageThree(messageTypeContent, senderID, usr):
    if messageTypeContent["type"] != "quick_reply":
        postFacebookMessage(senderID, "Apasa pe butoanele astea te rog :))")
        postTravelModeButtons(senderID)

    else:
        if messageTypeContent["content"] == "walking":
            walkingParameters = getWalkingParameters(getRouteRaw((usr.origin_loc_lat, usr.origin_loc_lng), (usr.dest_loc_lat, usr.dest_loc_lng), "walking"))

            if walkingParameters != None:

                walkingParameters["origin"] = usr.origin_loc_address
                walkingParameters["dest"] = usr.dest_loc_address

                postFacebookMessage(senderID, str(weatherCondition))
                postFacebookMessage(senderID, formulateWalkingRoute(walkingParameters))
                try:
                    postFacebookImageFromUrl(senderID, pictureUrlForRoute(walkingParameters["polyline"], [(usr.origin_loc_lat, usr.origin_loc_lng),(usr.dest_loc_lat, usr.dest_loc_lng)]))
                except:
                    print("no picture for: %s" % (pictureUrlForRoute(walkingParameters["polyline"], [(usr.origin_loc_lat, usr.origin_loc_lng),(usr.dest_loc_lat, usr.dest_loc_lng)])))
                #este o eroare pe librarie de static maps(motionless) cand face quote ar trebui sa face quote(*string*.encode('utf-8))
                # print ("Error:",e)

        elif messageTypeContent["content"] == "transit":
            transitParameters = getTransitParameters(getRouteRaw((usr.origin_loc_lat, usr.origin_loc_lng), (usr.dest_loc_lat, usr.dest_loc_lng), "transit"))

            if transitParameters != None:
                postFacebookMessage(senderID, str(transitParameters[1]))
                transitParameters[0].insert(1, (usr.origin_loc_lat, usr.origin_loc_lng))
                transitParameters[0].append((usr.dest_loc_lat, usr.dest_loc_lng))
                postFacebookImageFromUrl(senderID, pictureUrlForRoute(transitParameters[0][0], transitParameters[0][1:]))

        else: 
            postFacebookMessage(senderID, "Nu prea merge cu locatiile astea")

        postSendLocationQuickReply(senderID, "Acum daca vrei sa incepi procesul din nou trimite-mi locatia ta")

        usr.stage = 1
    return