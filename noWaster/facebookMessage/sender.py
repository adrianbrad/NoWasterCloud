import requests
import ujson

PAGE_TOKEN = 'EAAUvgZBC11iEBAKsso9GeWBRGIQSqFQed7rwWDZBh3QIVZBtA29jzOLrhWmePZCVzM9pqHaq2BQ4IYiEhalfEOVwvpGJdeI5Aq73VJZBZCEGOq8fEG6tNkrafxGyooYitDswzWiNjdPXokkv4JjG9XrfHQ7GkgtbHWELk0dkx90M7i5bJQ7rN9'

def postFacebookImageFromUrl(fbid,url):
    post_message_url = 'https://graph.facebook.com/v2.6/me/messages?access_token=' + PAGE_TOKEN
    response_msg = ujson.dumps({"recipient":{"id":fbid}, "message":{"attachment":{"type":"image", "payload":{"url":url, "is_reusable":True}}}})
    # response_msg = json.dumps({"recipient":{"id":fbid}, "message":{"text":url}})
    status = requests.post(post_message_url, headers={"Content-Type": "application/json"},data=response_msg)      

def postFacebookMessage(fbid, message):
    post_message_url = 'https://graph.facebook.com/v2.6/me/messages?access_token=' + PAGE_TOKEN
    response_msg = ujson.dumps({"recipient":{"id":fbid}, "message":{"text":message}})
    status = requests.post(post_message_url, headers={"Content-Type": "application/json"},data=response_msg)        

def postSendLocationQuickReply(fbid, message):
    post_message_url = 'https://graph.facebook.com/v2.6/me/messages?access_token=' + PAGE_TOKEN
    response_msg = ujson.dumps({"recipient":{"id":fbid}, "message":{"text":message,"quick_replies":[{"content_type":"location"}]}})
    status = requests.post(post_message_url, headers={"Content-Type": "application/json"},data=response_msg)      
