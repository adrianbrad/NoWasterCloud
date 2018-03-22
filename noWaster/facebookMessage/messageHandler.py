
myPageID = "1489738607768443"

def returnMessageTypeAndContent(message):
    if "text" in message['message']:
        return {"type":"text", "content":message['message']["text"]}
    if "attachments" in message['message']:
        if message['message']['attachments'][0]['type'] == "location":
            return {"type":"location", "content": (message['message']['attachments'][0]['payload']['coordinates']['lat'], message['message']['attachments'][0]['payload']['coordinates']['long'])}
    return None

def getSenderMessage(messageRawFile):
    for entry in messageRawFile['entry']:
            for message in entry['messaging']:
                # Check to make sure the received call is a message call
                # This might be delivery, optin, postback for other events 
                if 'message' in message:
                    if(message['recipient']['id'] != myPageID):
                        # Print the message to the terminal
                        return message
    return None