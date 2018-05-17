import requests
import ujson

man_walking = u'\U0001F6B6'
bus = u'\U0001F68C'
taxi = u'\U0001F695'

def sendPostRequestMessage(message):
    post_message_url = 'https://graph.facebook.com/v2.6/me/messages?access_token=EAAUvgZBC11iEBAKsso9GeWBRGIQSqFQed7rwWDZBh3QIVZBtA29jzOLrhWmePZCVzM9pqHaq2BQ4IYiEhalfEOVwvpGJdeI5Aq73VJZBZCEGOq8fEG6tNkrafxGyooYitDswzWiNjdPXokkv4JjG9XrfHQ7GkgtbHWELk0dkx90M7i5bJQ7rN9'
    return requests.post(post_message_url, headers={"Content-Type": "application/json"},data=message)

def postFacebookImageFromUrl(fbid,url):
    response_msg = ujson.dumps({"recipient":{"id":fbid}, "message":{"attachment":{"type":"image", "payload":{"url":url, "is_reusable":True}}}})
    status = sendPostRequestMessage(response_msg)      

def postFacebookMessage(fbid, message):
    response_msg = ujson.dumps({"recipient":{"id":fbid}, "message":{"text":message}})
    status = sendPostRequestMessage(response_msg)           

def postAskForLocGetNearbyLoc(fbid, message):
    response_msg = ujson.dumps(
        {
            "recipient":
                {
                    "id":fbid
                }, 
                "message":
                    {
                        "text":message, 
                        "quick_replies":
                        [
                            {
                                "content_type":"location"
                            },
                            {
                                "content_type":"text",
                                "title":"Localuri",
                                "payload":"nearby",
                            }
                        ]
                    }
        }
    )
    status = sendPostRequestMessage(response_msg)       

def locationOptionsButton(fbid, location):
    response_msg = ujson.dumps(
        {
            "recipient":
            {
                "id":fbid
            },
            "message":
                {
                    "attachment":
                    {
                        "type":"template",
                        "payload":
                        {
                            "template_type":"button",
                            "text":"Ai ales %s" %(location),
                            "buttons":
                                [
                                    {   
                                        "type":"postback",
                                        "title":"Ruta",
                                        "payload":""
                                    },
                                    {
                                        "type":"postback",
                                        "title":"NoWaster",
                                        "payload":""
                                    },
                                    {
                                        "type":"postback",
                                        "title":"Informatii",
                                        "payload":""
                                    }
                                ]
                        }
                    }
                }
        }
    )
    status = sendPostRequestMessage(response_msg)      


def postAskForLocGetNearbyLocGetRoute(fbid, message):
    response_msg = ujson.dumps(
        {
            "recipient":
                {
                    "id":fbid
                }, 
                "message":
                    {
                        "text":message, 
                        "quick_replies":
                        [
                            {
                                "content_type":"location"
                            },
                            {
                                "content_type":"text",
                                "title":"Localuri",
                                "payload":"nearby"
                            },
                            {
                                "content_type":"text",
                                "title":"Ruta",
                                "payload":"get_route"
                            }
                        ]
                    }
        }
    )
    status = requests.post(post_message_url, headers={"Content-Type": "application/json"},data=response_msg)


def dynamicQuickReplyButton(fbid, text, buttonsList):
    btnForFb = []
    for button in buttonsList:
        btnForFb.append({
            "content_type":"text",
            "title":button["name"],
            "payload": "locationBut_" + button["name"]
        })

    response_msg = ujson.dumps(
        {
            "recipient":
            {
                "id":fbid
            },
            "message":
            {
                "text": text,
                "quick_replies":btnForFb
            }
        }
    )
    status = sendPostRequestMessage(response_msg)         
    print status      

def postSendLocationQuickReply(fbid, message):
    response_msg = ujson.dumps({"recipient":{"id":fbid}, "message":{"text":message,"quick_replies":[{"content_type":"location"}]}})
    status = sendPostRequestMessage(response_msg)        

def postTravelModeButtons(fbid):
    response_msg = ujson.dumps(
        {
            "recipient":
            {
                "id":fbid
            },
            "message":
            {
                "text": "Aelge un mod de deplasare",
                "quick_replies":
                [
                    {
                        "content_type":"text",
                        "title":"Bus " + bus,
                        "payload":"transit",
                    },
                    {
                        "content_type":"text",
                        "title":"Pe jos " + man_walking,
                        "payload":"walking",
                    },
                    {
                        "content_type":"text",
                        "title":"taxi " + taxi,
                        "payload":"driving",
                    }
                ]
            }
        }
    )
    status = sendPostRequestMessage(response_msg)      


def postTemplateTextButtons(fbid, originText, originGeocode, destText, destGeocode):
    response_msg = ujson.dumps(
        {
            "recipient":
            {
                "id":fbid
            },
            "message":
                {
                    "attachment":
                    {
                        "type":"template",
                        "payload":
                        {
                            "template_type":"generic",
                            "elements":
                            [
                                {
                                    "title":"Alege modul de deplasare",
                                    "subtitle":"De la %s pana la %s" % (originText, destText),
                                    "buttons":
                                        [
                                            {   
                                                "type":"postback",
                                                "title":"Bus %s" % (bus),
                                                "payload":"%s %s %s %s transit" %(str(originGeocode[0]), str(originGeocode[1]), str(destGeocode[0]), str(destGeocode[1]))
                                            },
                                            {
                                                "type":"postback",
                                                "title":"Pe jos %s" % (man_walking),
                                                "payload":"%s %s %s %s walking" %(str(originGeocode[0]), str(originGeocode[1]), str(destGeocode[0]), str(destGeocode[1]))
                                            },
                                            {
                                                "type":"postback",
                                                "title":"taxi %s" % (taxi),
                                                "payload":"%s %s %s %s driving" %(str(originGeocode[0]), str(originGeocode[1]), str(destGeocode[0]), str(destGeocode[1]))
                                            }
                                        ]
                                }
                            ]
                        }
                    }
                }
        }
    )
    status = sendPostRequestMessage(response_msg)      

def postSenderAction(senderAction, fbid):
    response_msg = ujson.dumps({"recipient":{"id":fbid}, "sender_action": senderAction})
    status = sendPostRequestMessage(response_msg)      

def postAskWhatToDoWithLocation(fbid, message):
    response_msg = ujson.dumps(      
        {
            "recipient":
            {
                "id":fbid
            },
            "message":
            {
                "text": message,
                "quick_replies":
                [
                    {
                        "content_type":"text",
                        "title":"Pornire",
                        "payload":"origin",
                    },
                    {
                        "content_type":"text",
                        "title":"Destinatie",
                        "payload":"dest",
                    },
                    {
                        "content_type":"text",
                        "title":"Localuri in apropiere",
                        "payload":"nearby",
                    }
                ]
            }
        }
    )
    status = sendPostRequestMessage(response_msg)      

# def getRouteButtonAndSetOriginButton(fbid):

