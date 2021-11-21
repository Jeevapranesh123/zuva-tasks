import re
import pymongo
import json
import time
import pprint
from flaskapi.Lib.client import client


# client=pymongo.MongoClient('localhost')
db = client.TaskManager
col = db.Projects
members = db.Members
Users = db.Users


class Head:

    def __init__(self):
        pass

    def add_user(self,name,email):
        x=Users.find_one({'username':name.lower(),'email':email,'active':True})
        
        if x is None:
            raise Exception ("User Not Found in Users table")

        a=members.find()

        max=0
        for i in a:
            
            if i['name']==name:
            
                raise Exception('User already exists')

            if i['email']==email:
                raise Exception("Email already in use")

            if i['empid']>max:
     
                max=i['empid']
        l=list()
        data={
            "empid":max+1,
            "name":name.lower(),
            "email":email,
            "is_admin":False,
            "is_head":False,
            "head":[],

        }

        if members.insert_one(data):
            return data
        else:
            raise Exception("Could Not Insert Data")

    
        
