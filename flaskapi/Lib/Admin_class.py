import pymongo
from flaskapi.Lib.client import client
# client=pymongo.MongoClient('localhost')
db = client.TaskManager
col = db.Users
Members = db.Members



class Admin:

    def __init__(self):
        pass

    def makeuseractive(self,username,email):

        a=col.find_one({'username':username.lower(),'email':email.lower()})
        if  a:
        
            if a['active']==True:

                raise Exception ("User Already Active")

            else:
                filter = {'username':username.lower(),'email':email.lower()}

                newvalues = { "$set": { 'active':True }}

                if col.update_one(filter, newvalues):
                    return True
                else:
                    return False
        else:
            raise Exception ('User Not Found')

    
    def get_all_members(self):

        a=Members.find()
        data=[]

        for i in a:
            del i['_id']
            data.append(i)
        return data


    def get_members_with_id(self, id:int):

        x=Members.find()
        for i in x:
            if i['empid']==id:
                del i['_id']
                return i
        else:
            raise Exception("Member Not Found")            



    

