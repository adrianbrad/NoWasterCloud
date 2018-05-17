from datetime import date
from noWaster.models import User
import requests


def getUserInfo(senderID):

    usr, created = User.objects.get_or_create(id = senderID)
    if created or usr.last_update_time != date.today():
        res = "https://graph.facebook.com/v2.6/%s?fields=first_name,last_name,profile_pic&access_token=%s" % (senderID, 'EAAUvgZBC11iEBAKsso9GeWBRGIQSqFQed7rwWDZBh3QIVZBtA29jzOLrhWmePZCVzM9pqHaq2BQ4IYiEhalfEOVwvpGJdeI5Aq73VJZBZCEGOq8fEG6tNkrafxGyooYitDswzWiNjdPXokkv4JjG9XrfHQ7GkgtbHWELk0dkx90M7i5bJQ7rN9') 
        userInfo = requests.get(res).json()

        if userInfo.get("first_name") != None:
            if usr.first_name != userInfo.get("first_name"):
                usr.first_name = userInfo.get("first_name")
        if userInfo.get("last_name") != None:
            if usr.last_name != userInfo.get("last_name"):
                usr.last_name = userInfo.get("last_name")
        
        if userInfo.get("profile_pic") != None:
            if usr.profile_pic != userInfo.get("profile_pic"):
                usr.profile_pic = userInfo.get("profile_pic")
        usr.last_update_time = date.today()
        
    usr.currently_responding_to = True
    usr.save()
    return usr
