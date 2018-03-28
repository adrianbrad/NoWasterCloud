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
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
from datetime import datetime
from django.db import connection

import ujson, requests
from facebookMessage.messageHandler import returnMessageTypeAndContent, getSenderMessage
from facebookMessage.sender import postSenderAction, getUserInfo, postFacebookMessage
from stageManagement import stageZero, stageOne, stageTwo, stageThree

# import time

from models import User

stageFuncionCall = {
    0: stageZero,
    1: stageOne,
    2: stageTwo,
    3: stageThree
}

class Test(generic.View):

    def get(self, request, *args, **kwargs):
        origin = "the office cluj"
        dest = "iulius mall cluj"
        startT = datetime(2018, 3, 24, 21, 00)
        from location.locationText import getRouteRaw, geocodeLocation
        directions = geocodeLocation("olteniei 3 baia mare")
        # # print directions[0]["legs"][0]["steps"]
        # transitParameters = getTransitParameters(getRouteRaw(origin, dest, "transit"))
        # print(pictureUrlForRoute(transitParameters[0][0], transitParameters[0][1:]))
        # return HttpResponse(transitParameters)
        # from models import User
        # from models import Loc
        # lol = User(first_name = "Test", last_name = "Brad")
        # lol.save()
        # theUsr, created = User.objects.get_or_create(id="1489738607768443")
        # ret = getUserInfo('1489738607768443')
        # theUsr.first_name = "Aditza"
        # theUsr.save()
        return HttpResponse(directions)


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

        for entry in incoming_message['entry']:
            for message in entry['messaging']:
                msg = getSenderMessage(message) 

            if msg != None:
                senderID = message['sender']['id']
                usr = getUser(senderID)

                if usr != False:
                    postSenderAction("mark_seen", senderID)
                    postSenderAction("typing_on", senderID)
                    handleMessage(msg, senderID, usr)

        return HttpResponse()

def handleMessage(message, senderID, usr):
    messageTypeContent = returnMessageTypeAndContent(message)

    if messageTypeContent != None:
        print messageTypeContent["content"]
        if messageTypeContent["content"] == "Reset":
            usr.delete()
            postFacebookMessage(senderID, "te am sters din db")
        else:
        # usr.currently_responding_to = True
        # usr.save()
            stage = usr.stage

            stageFuncionCall[stage](messageTypeContent, senderID, usr)
            
            usr.save()

    else:
        postFacebookMessage(senderID, "nu stiu de astea :))")

def getUser(senderID):
    usr, created = User.objects.get_or_create(id = senderID)

    # if usr.currently_responding_to:
    #     return False

    userInfo = getUserInfo(senderID)

    if usr.first_name != userInfo["first_name"]:
        usr.first_name = userInfo["first_name"]

    if usr.last_name != userInfo["last_name"]:
        usr.last_name = userInfo["last_name"]
    
    if usr.profile_pic != userInfo["profile_pic"]:
        usr.profile_pic != userInfo["profile_pic"]

    usr.save()

    return usr

