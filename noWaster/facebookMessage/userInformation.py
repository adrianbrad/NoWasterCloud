from sender import PAGE_TOKEN
from datetime import date
from noWaster.models import User
import requests


def getUserInfo(senderID):

    usr, created = User.objects.get_or_create(id = senderID)
    if created or usr.last_update_time != date.today():
        res = "https://graph.facebook.com/v2.6/%s?fields=first_name,last_name,profile_pic&access_token=%s" % (senderID, PAGE_TOKEN) 
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
        usr.save()
        print "updated"
    return usr
