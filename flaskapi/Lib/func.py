from flaskapi.Lib.Auth_class import Auth
import pymongo
from flaskapi.Lib.client import client

# client =pymongo.MongoClient('localhost')
db = client.TaskManager
Users = db.Users
Sessions = db.Sessions
Members = db.Members

def mysqlclean(a):
    return a

def is_valid(token):

    x=token.split(' ')
    if token:
        a=Auth(x[1])
    else:
        return {'Error':'No data Input'},400
    if a.authenticate():
        return True
    else:
        return False

def check_if_admin(token):

        x=token.split(' ')
        if token:
            a=Auth(x[1])
        else:
            return {'Error':'No data Input'},400
        
        if a.authenticate():
            x=Sessions.find_one({'token':x[1]})
            if x:
                username = x['username'].lower()
                m=Members.find_one({'name':username})
                if m:
                    if m['is_admin']:
                        return True
                    else:
                        return False
            else:
                raise Exception('Unauthorized')
        else:
            raise Exception('Unauthorized')

def check_if_head(token,projectname):

        x=token.split(' ')
  
        if token:
            a=Auth(x[1])
        else:
            return {'Error':'No data Input'},400
        
        if a.authenticate():
            x=Sessions.find_one({'token':x[1]})
        
            if x:
                username = x['username'].lower()
                m=Members.find_one({'name':username})
            
                if m:
                    if m['is_head']:
                        return True
                    else:
                        return False
            else:
                raise Exception('Unauthorized')
        else:
            raise Exception('Unauthorized')

def check_if_superuser(token):
        x=token.split(' ')
        if token:
            a=Auth(x[1])
            
        else:
            return {'Error':'No data Input'},400
        
        if a.authenticate():
            x=Sessions.find_one({'token':x[1]})
            
            if x:
                username = x['username'].lower()
                
                m=Users.find_one({'username':username})
               
                if m:
                    if m['Superuser']:
                        return True
                    else:
                        return False
            else:
                raise Exception('Unauthorized')
        else:
            raise Exception('Unauthorized')

def check_if_user(name,email):

    a=Users.find_one({'username':name.lower(),'email':email.lower()})
    if a:
        if a['active']==True:
            return True
        else:
            raise Exception('User Not Active')
    else:
        raise Exception('User Not Found')

def check_if_member(name, email):


    a=Members.find_one({'name':name.lower(),'email':email.lower()})
    if a:
        return True
    else:
        return False

def check_if_nakku(password):
    if password=="c3baaa85ead56dd4ae01c638c18bf723":
        return True
    else:
        return False

