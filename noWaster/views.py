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
from datetime import date
from django.db import connection

import ujson, requests
from facebookMessage.messageHandler import returnMessageTypeAndContent, getSenderMessage
from facebookMessage.sender import postSenderAction, postFacebookMessage
from facebookMessage.userInformation import getUserInfo
from stageManagement import getStarted, stageOne, stageTwo, sendRoute, handleUnexpectedLocation, resolveLocation

# import time
stageFuncionCall = {
    0: getStarted,
    1: stageOne,
    2: stageTwo,
    3: sendRoute,
    4: handleUnexpectedLocation,
    5: resolveLocation
}

class Test(generic.View):

    def get(self, request, *args, **kwargs):
        PAGE_TOKEN = 'EAAUvgZBC11iEBAKsso9GeWBRGIQSqFQed7rwWDZBh3QIVZBtA29jzOLrhWmePZCVzM9pqHaq2BQ4IYiEhalfEOVwvpGJdeI5Aq73VJZBZCEGOq8fEG6tNkrafxGyooYitDswzWiNjdPXokkv4JjG9XrfHQ7GkgtbHWELk0dkx90M7i5bJQ7rN9'

        post_message_url = 'https://graph.facebook.com/v2.6/me/messenger_profile?access_token=' + PAGE_TOKEN
        response_msg = ujson.dumps({
        "persistent_menu":[
            {
            "locale":"default",
            "composer_input_disabled":"false",
            "call_to_actions":[
                {
                "title":"Schimba locatia ta",
                "type":"postback",
                "payload":"origin"
                },
                {
                "title":"Alege o destinatie noua",
                "type":"postback",
                "payload":"dest"
                },
                {
                "title":"Vezi ce localuri ai in jur",
                "type":"postback",
                "payload":"nearby"
                }
            ]
            }
        ]
        })
        status = requests.post(post_message_url, headers={"Content-Type": "application/json"},data=response_msg)       
        return HttpResponse(status)


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
                usr = getUserInfo(senderID)
                # if usr != False and usr.currently_responding_to == False:
                if usr != False:
                    postSenderAction("mark_seen", senderID)
                    postSenderAction("typing_on", senderID)
                    handleMessage(msg, senderID, usr)
                    # postFacebookMessage(senderID, "ok")
        return HttpResponse()

def handleMessage(message, senderID, usr):
    messageTypeContent = returnMessageTypeAndContent(message)

    if messageTypeContent != None:
        if messageTypeContent["content"] == "Reset":
            usr.delete()
            postFacebookMessage(senderID, "te am sters din db")  

        elif messageTypeContent["type"] ==  "travel_postback":
            stageFuncionCall[3](messageTypeContent, senderID, usr)

        elif messageTypeContent["type"] == "location" and (usr.stage != 1 or usr.stage != 2):
            stageFuncionCall[4](messageTypeContent, senderID, usr)
        
        elif messageTypeContent["type"] == "location_setter":
            stageFuncionCall[5](messageTypeContent, senderID, usr)

        else:
            stageFuncionCall[usr.stage](messageTypeContent, senderID, usr)

        # if messageTypeContent["content"] == "Reset":
        #     usr.delete()
        #     postFacebookMessage(senderID, "te am sters din db")
            
        # elif messageTypeContent["type"] == "get_started":
        #     stageFuncionCall[0](messageTypeContent, senderID, usr)
        
        # elif usr.stage != 3:

        #     stageFuncionCall[usr.stage](messageTypeContent, senderID, usr)
        
        usr.currently_responding_to = False
        usr.save()

    else:
        postFacebookMessage(senderID, "nu stiu de astea :))")

