import pymongo
from flaskapi.Lib.client import client
# client=pymongo.MongoClient('localhost')
db = client.TaskManager
col = db.Users
Members = db.Members


class Superuser:

    def __init__(self,):
        pass

    def makeuseradmin(self,username,email):

        a=Members.find_one({'name':username.lower(),'email':email.lower()})

        if a:
            if col.find_one({'username':username.lower(),'email':email.lower(),'active':True}):

                filter = { 'name':username.lower(),'email':email.lower()}

                newvalues = { "$set": { 'is_admin':True}}

                if Members.update_one(filter, newvalues):
                    return True
                else:
                    return False
            else:
                raise Exception ("User Not Found in Users list")
        else:
            raise Exception ("User Not Found in Employee List")
        
    
    def removeadmin(self,username,email):

        a=Members.find_one({'name':username.lower(),'email':email.lower()})

        if a:
            if col.find_one({'username':username.lower(),'email':email.lower(),'active':True}):

                filter = { 'name':username.lower(),'email':email.lower()}

                newvalues = { "$set": { 'is_admin':False}}

                if Members.update_one(filter, newvalues):
                    return True
                else:
                    return False
            else:
                raise Exception ("User Not Found in Users list")
        else:
            raise Exception ("User Not Found in Employee List")

    def makesuperuser(self,username,email):
        a=col.find_one({'email':email.lower()})
        
        if a:
            if col.find_one({'username':username.lower(),'email':email.lower(),'active':True}):

                filter = { 'username':username.lower(),'email':email.lower()}

                newvalues = { "$set": { 'Superuser':True}}

                if col.update_one(filter, newvalues):

                    return True
                else:
                    return False

            else:
                raise Exception ("User Not Active")
        else:
            raise Exception('User Not Found')

