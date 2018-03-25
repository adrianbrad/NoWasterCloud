# Copyright 2015 Google Inc. All rights reserved.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

from django.http import HttpResponse
from django.views import generic
import ujson, requests
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
from datetime import datetime
from django.db import connection

from extras.weatherCondition import weatherCondition
from location.locationText import * 
from location.locationPicture import * 
from facebookMessage.messageHandler import *
from facebookMessage.sender import *
from facebookMessage.formulate import *
import time

users = {}


class Test(generic.View):

    def get(self, request, *args, **kwargs):
        origin = "the office cluj"
        dest = "iulius mall cluj"
        startT = datetime(2018, 3, 24, 21, 00)
        directions = getRouteRaw(origin, dest, "transit", departure_time = startT)
        # print directions[0]["legs"][0]["steps"]
        transitParameters = getTransitParameters(getRouteRaw(origin, dest, "transit"))
        print(pictureUrlForRoute(transitParameters[0][0], transitParameters[0][1:]))
        return HttpResponse(transitParameters)


class NoWasterView(generic.View):
    def get(self, request, *args, **kwargs):
        if self.request.GET['hub.verify_token'] == 'brad':
            return HttpResponse(self.request.GET['hub.challenge'])
        else:
            return HttpResponse('Error, invalid token')


    @method_decorator(csrf_exempt)
    def dispatch(self, request, *args, **kwargs):
        return generic.View.dispatch(self, request, *args, **kwargs)

    # Post function to handle Facebook messages
    def post(self, request, *args, **kwargs):
        incoming_message = ujson.loads(self.request.body.decode('utf-8'))
        # print (incoming_message["entry"][0]["messaging"][0]["message"]["nlp"]) 
        # handleMessage(incoming_message)
        for entry in incoming_message['entry']:
            for message in entry['messaging']:
                # Check to make sure the received call is a message call
                # This might be delivery, optin, postback for other events 
                msg = getSenderMessage(message) 
            if msg != None:
                senderID = message['sender']['id']
                userDict = returnUserDictIfNotAlreadyResponding(senderID, users)
                if userDict != None:
                    postSenderAction("mark_seen", senderID)
                    postSenderAction("typing_on", senderID)
                    # userDict["responding"] = True
                    handleMessage(msg, senderID, userDict)
                    # print(returnMessageTypeAndContent(msg))
                    # postSendLocationQuickReply(senderID, "asdf")
        return HttpResponse()

def handleMessage(message, senderID, userDict):
    messageTypeContent = returnMessageTypeAndContent(message)
    # print(messageTypeContent)
    if messageTypeContent != None:
        stage = userDict["stage"]
        if stage == 0:
            # print("aici")
            postSendLocationQuickReply(senderID, "Trimite-mi locatia ta")
            userDict["stage"] += 1
        elif stage == 1:
            loc = getGeocodeAndText(messageTypeContent["content"])
            if loc == None:
                postSendLocationQuickReply(senderID, "locatia nu e valida, mai incearca o data") 
            else:
                userDict["originLoc"] = loc
                userDict["stage"] += 1
                postSendLocationQuickReply(senderID, "Trimite locatia unde vrei sa ajungi") 
        elif stage == 2:
            loc = getGeocodeAndText(messageTypeContent["content"])
            if loc == None:
                postSendLocationQuickReply(senderID, "locatia nu e valida, mai incearca o data") 
            else:
                userDict["destLoc"] = loc
                userDict["stage"] += 1
                postTravelModeButtons(senderID)
        elif stage == 3:
            if messageTypeContent["type"] != "quick_reply":
                postFacebookMessage(senderID, "Apasa pe butoanele astea te rog :))")
                postTravelModeButtons(senderID)
            else:
                # print(messageTypeContent["content"] == "transit")
                if messageTypeContent["content"] == "walking":
                    walkingParameters = getWalkingParameters(getRouteRaw(userDict["originLoc"]["geocode"], userDict["destLoc"]["geocode"], "walking"))
                    if walkingParameters != None:

                        walkingParameters["origin"] = userDict["originLoc"]["text"]
                        walkingParameters["dest"] = userDict["destLoc"]["text"]

                        postFacebookMessage(senderID, str(weatherCondition))
                        postFacebookMessage(senderID, formulateWalkingRoute(walkingParameters))
                        try:
                            postFacebookImageFromUrl(senderID, pictureUrlForRoute(walkingParameters["polyline"], [userDict["originLoc"]["geocode"],userDict["destLoc"]["geocode"]]))
                        except:
                            print(pictureUrlForRoute(walkingParameters["polyline"], [userDict["originLoc"]["geocode"],userDict["destLoc"]["geocode"]]))
                        #este o eroare pe librarie de static maps(motionless) cand face quote ar trebui sa face quote(*string*.encode('utf-8))
                        # print ("Error:",e)
                elif messageTypeContent["content"] == "transit":
                    transitParameters = getTransitParameters(getRouteRaw(userDict["originLoc"]["geocode"], userDict["destLoc"]["geocode"], "transit"))
                    if transitParameters != None:
                        postFacebookMessage(senderID, str(transitParameters[1]))
                        transitParameters[0].insert(1, userDict["originLoc"]["geocode"])
                        transitParameters[0].append(userDict["destLoc"]["geocode"])
                        postFacebookImageFromUrl(senderID, pictureUrlForRoute(transitParameters[0][0], transitParameters[0][1:]))
                else: 
                    postFacebookMessage(senderID, "Nu prea merge cu locatiile astea")
                postSendLocationQuickReply(senderID, "Acum daca vrei sa incepi procesul din nou trimite-mi locatia ta")
                userDict["stage"] = 1
        else:
            postFacebookMessage(senderID, "nu stiu de astea :))")

def returnUserDictIfNotAlreadyResponding(senderID, users):
    if users.has_key(senderID) == False:
        users[senderID] = {}
        users[senderID]["stage"] = 0
        users[senderID]["originLoc"] = {}
        users[senderID]["destLoc"] = {}
    return users[senderID]