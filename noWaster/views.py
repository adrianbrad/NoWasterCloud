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
import googlemaps
from datetime import datetime
from django.db import connection

from extras.weatherCondition import weatherCondition
from location.locationText import * 
from location.locationPicture import * 
from facebookMessage.messageHandler import *
from facebookMessage.sender import *
from facebookMessage.formulate import *

gmaps = googlemaps.Client(key='AIzaSyD2lAiwG69gKzptts3Z1aFcyoNYnsis7AY')

users = {}

class Test(generic.View):
    def get(self, request, *args, **kwargs):
        return HttpResponse(str(users))

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
        # Converts the text payload into a python dictionary
        incoming_message = ujson.loads(self.request.body.decode('utf-8'))
        # if getSenderMessage(incoming_message) != None:
        message = getSenderMessage(incoming_message) 
        if message != None:
            senderID = message['sender']['id']
            messageTypeContent = returnMessageTypeAndContent(message)
            if messageTypeContent != None:
                if users.has_key(senderID):
                    stage = users[senderID]["stage"]
                else:
                    stage = 0
                    users[senderID] = {}
                    users[senderID]["stage"] = stage
                    users[senderID]["originLoc"] = {}
                    users[senderID]["destLoc"] = {}
                if stage == 0:
                    postSendLocationQuickReply(senderID, "Trimite-mi locatia ta")
                    stage = 1
                    users[senderID]["stage"] = stage
                elif stage == 1:
                    loc = getGeocodeAndText(messageTypeContent["content"])
                    if loc == None:
                        postSendLocationQuickReply(senderID, "locatia nu e valida, mai incearca o data") 
                    else:
                        users[senderID]["originLoc"] = loc
                        users[senderID]["stage"] = 2
                        postSendLocationQuickReply(senderID, "Trimite locatia unde vrei sa ajungi") 
                elif stage == 2:
                    loc = getGeocodeAndText(messageTypeContent["content"])
                    if loc == None:
                        postSendLocationQuickReply(senderID, "locatia nu e valida, mai incearca o data") 
                    else:
                        users[senderID]["destLoc"] = loc
                        walkingParameters = getWalkingParameters(getRouteRaw(users[senderID]["originLoc"]["geocode"], users[senderID]["destLoc"]["geocode"], "walking"))
                        if walkingParameters != None:
                            postFacebookMessage(senderID, walkingParameters["distance"] + " " + walkingParameters["duration"])
                            postFacebookMessage(senderID, str(weatherCondition))
                            try:
                                postFacebookImageFromUrl(senderID, pictureUrlForRoute(users[senderID]["originLoc"]["text"],users[senderID]["destLoc"]["text"], walkingParameters["polyline"]))
                            except:
                                print("what th efuck")
                            #este o eroare pe librarie de static maps(motionless) cand face quote ar trebui sa face quote(*string*.encode('utf-8))
                            # print ("Error:",e)
                        else: 
                            postFacebookMessage(senderID, "Nu prea merge cu locatiile astea")
                        postFacebookMessage(senderID,"Acum daca vei scrie ceva vei incepe procesul din nou")
                        users[senderID]["stage"] = 0
        return HttpResponse()