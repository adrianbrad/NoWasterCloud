import requests
import ujson

PAGE_TOKEN = 'EAAUvgZBC11iEBAKsso9GeWBRGIQSqFQed7rwWDZBh3QIVZBtA29jzOLrhWmePZCVzM9pqHaq2BQ4IYiEhalfEOVwvpGJdeI5Aq73VJZBZCEGOq8fEG6tNkrafxGyooYitDswzWiNjdPXokkv4JjG9XrfHQ7GkgtbHWELk0dkx90M7i5bJQ7rN9'
man_walking = u'\U0001F6B6'
bus = u'\U0001F68C'
taxi = u'\U0001F695'

def postFacebookImageFromUrl(fbid,url):
    post_message_url = 'https://graph.facebook.com/v2.6/me/messages?access_token=' + PAGE_TOKEN
    response_msg = ujson.dumps({"recipient":{"id":fbid}, "message":{"attachment":{"type":"image", "payload":{"url":url, "is_reusable":True}}}})
    status = requests.post(post_message_url, headers={"Content-Type": "application/json"},data=response_msg)      

def postFacebookMessage(fbid, message):
    post_message_url = 'https://graph.facebook.com/v2.6/me/messages?access_token=' + PAGE_TOKEN
    response_msg = ujson.dumps({"recipient":{"id":fbid}, "message":{"text":message}})
    status = requests.post(post_message_url, headers={"Content-Type": "application/json"},data=response_msg)        

def postSendLocationQuickReply(fbid, message):
    post_message_url = 'https://graph.facebook.com/v2.6/me/messages?access_token=' + PAGE_TOKEN
    response_msg = ujson.dumps({"recipient":{"id":fbid}, "message":{"text":message,"quick_replies":[{"content_type":"location"}]}})
    status = requests.post(post_message_url, headers={"Content-Type": "application/json"},data=response_msg)      

def postTravelModeButtons(fbid):
    post_message_url = 'https://graph.facebook.com/v2.6/me/messages?access_token=' + PAGE_TOKEN
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
                        "payload":"taxi",
                    }
                ]
            }
        }
    )
    status = requests.post(post_message_url, headers={"Content-Type": "application/json"},data=response_msg)

def postTemplateTextButtons(fbid, title, subtitle, buttons):
    post_message_url = 'https://graph.facebook.com/v2.6/me/messages?access_token=' + PAGE_TOKEN
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
                                    "title":title,
                                    "subtitle":subtitle,
                                    "buttons":
                                        [
                                            {   
                                                "type":"postback",
                                                "title":"One",
                                                "payload":"UNU"
                                            },
                                            {
                                                "type":"postback",
                                                "title":"Two",
                                                "payload":"Doi"
                                            }
                                        ]
                                }
                            ]
                        }
                    }
                }
        }
    )
    status = requests.post(post_message_url, headers={"Content-Type": "application/json"},data=response_msg)

def postSenderAction(senderAction, fbid):
    post_message_url = 'https://graph.facebook.com/v2.6/me/messages?access_token=' + PAGE_TOKEN
    response_msg = ujson.dumps({"recipient":{"id":fbid}, "sender_action": senderAction})
    status = requests.post(post_message_url, headers={"Content-Type": "application/json"},data=response_msg)      