
myPageID = "1489738607768443"

def returnMessageTypeAndContent(message):
    print (message)
    if "text" in message:
        if "quick_reply" in message:
            return {"type":"quick_reply", "content":message["quick_reply"]["payload"]}
        return {"type":"text", "content":message["text"]}
    if "attachments" in message:
        if message['attachments'][0]['type'] == "location":
            return {"type":"location", "content": (message['attachments'][0]['payload']['coordinates']['lat'], message['attachments'][0]['payload']['coordinates']['long'])}
    return None

def getSenderMessage(message):
    if 'message' in message:
        if(message['recipient']['id'] != myPageID):
            # Print the message to the terminal
            return message["message"]
    return None