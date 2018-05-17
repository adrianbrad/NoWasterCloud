
myPageID = "1489738607768443"

def returnMessageTypeAndContent(message):
    if "text" in message:
        if "quick_reply" in message:
            if message["quick_reply"]["payload"] == "origin" or message["quick_reply"]["payload"] == "dest":
                return {"type":"location_setter", "content": message["quick_reply"]["payload"]}
                
            else:
                return {"type":"quick_reply", "content":message["quick_reply"]["payload"]}
                
        return {"type":"text", "content":message["text"]}
        
    if "attachments" in message:
        if message['attachments'][0]['type'] == "location":
            return {"type":"location", "content": (message['attachments'][0]['payload']['coordinates']['lat'], message['attachments'][0]['payload']['coordinates']['long'])}

    if "postback" in message:
        if "payload" in message["postback"]:
            if message["postback"]["payload"] == "GET_STARTED_PAYLOAD":
                return {"type":"get_started", "content" : ""}

            try:
                return {"type":"menu_but", "content" : int(message["postback"]["payload"])}
            except:
                return {"type":"travel_postback", "content" :recreateLocationsFromPostback(message["postback"]["payload"])}              
    return None

def recreateLocationsFromPostback(postbackString):
    listFromPostback = postbackString.split()
    return {"origin" : (float(listFromPostback[0]), float(listFromPostback[1])), "dest" : (float(listFromPostback[2]), float(listFromPostback[3])), "travel_mode": listFromPostback[4]}

def getSenderMessage(message):
    if 'message' in message:
        if(message['recipient']['id'] != myPageID):
            return message["message"]

    if "postback" in message:
        return message

    return None