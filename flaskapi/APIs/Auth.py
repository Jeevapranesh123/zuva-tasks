import time
from flask import Blueprint,request
from flaskapi.Lib.Signup_class import *
from flaskapi.Lib.Auth_class import Auth
import json
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address
auth_api = Blueprint('auth_api',__name__)

# limiter = Limiter(auth_api, key_func=get_remote_address)

# @limiter.limit("5/minute")

def mysqlclean(a):
    return a


@auth_api.route('/auth/signup',methods=['POST'])
def signup():
    request_data = request.form or request.get_json()
    username = mysqlclean(request_data.get('username'))
    email = mysqlclean(request_data.get('email'))
    password = mysqlclean(request_data.get('password'))
    

    if email and username and password:

        try:

            
            a=Signup().createuser(username.strip().lower(), email.strip().lower(), password.strip())
            if a: 
                data={
                    'Message': 'Signup Success',
                    'Userid':a['uid'],
                    'Username': username,
                    'Email': email,
                }
                return json.dumps(data),200
        except Exception as e:
            data={
                "Error":str(e)
            }
            return json.dumps(data),409

    else:
        data={
                'Error':"Invalid Request"

            }
        return json.dumps(data),400


# @limiter.limit("5/minute")
@auth_api.route('/auth/login',methods=['POST'])
def login():

    request_data = request.form or request.get_json()
    email = mysqlclean(request_data.get('email'))
    password = mysqlclean(request_data.get('password'))

    if email and password:

        try:
            start = time.time()
            a=Auth(email.strip().lower(),password.strip().lower())
            end=time.time()
            data={
                'Message':'login Success',
                'Data':a.getdata(),
                'time':end-start
            }
            return json.dumps(data),200

        except Exception as e:
            data={
                'Error':str(e),
            }
            return json.dumps(data),403

    else:
        data={
            'Error':'Invalid Request'
        }
        return json.dumps(data),400

@auth_api.route('/auth/isvalid', methods=['POST'])
def is_valid():
    request_data = request.form or request.get_json()
    token = mysqlclean(request_data.get('token'))
    if token:
        a=Auth(token)
    else:
        return {'Error':'No data Input'},400
    if a.authenticate():
        data={
            'Valid': True,
            'Valid_for':a.valid_for_token()
        }
        return json.dumps(data),200
    else:
        data={
            'Error':'Invalid Token'
        }
        return json.dumps(data),400
