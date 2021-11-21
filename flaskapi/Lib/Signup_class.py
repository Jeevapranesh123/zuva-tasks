import pymongo
import json
from flaskapi.Lib.client import client


# client=pymongo.MongoClient()
db=client.TaskManager
Users=db.Users


class Signup:

    def __init__(self):
        pass

    def createuser(self, username,email, password):
        
        a = Users.find()
        
        for i in a:
            
            if i['email'] == email:
                raise Exception("Email already Exists")
            if i['username']==username.lower():
                raise Exception("Username already Exists")

        max=0

        for i in a:

            if i['uid']>max:
        
                max=i['uid']

        data = {
            'uid':max+1,
            'username':username.lower(),
            'email': email,
            'Password': password,
            'active': False,
            "Superuser":False,
        }
        
        Users.insert_one(data)
        return data

    def verifytoken(self,username,password):
        pass




