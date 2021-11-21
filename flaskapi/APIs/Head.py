import time
from flask import Blueprint,request
from flaskapi.Lib.Head_class import *
from flaskapi.Lib.func import *
import json

head_api = Blueprint('head_api',__name__)

@head_api.route('/members/add',methods=['POST'])
def add_member():
    request_data = request.form or request.get_json()
    name = request_data.get('Name')
    email = request_data.get('Email')
    if name and email:
        token=request.headers.get('Authorization')
        if token is None:
            data={
                    "Error":"Unauthorized"
                }
            return json.dumps(data),401
        
        if is_valid(token):

            if check_if_admin(token) or check_if_superuser(token):

                try:

                    x=Head().add_user(name,email)
                    if x:

                        data={
                            "Message":"Member Added Successfully",
                            "data":{
                                    "empid":x['empid'],
                                    "name":x['name'],
                                    "email":x['email'],
                                    "is_admin":x['is_admin'],
                                    "is_head":x['is_head'],
                                    "head":x['head']
                                }
                        }
                        return json.dumps(data),200
                except Exception as e:
                    data={
                        "Error":str(e)
                    }
                    return json.dumps(data),400
            else:
                data={
                    "Error":"Cannot Perform Action. Contact Higher Authorities :)"
                }
            return json.dumps(data),401

        else:
            data={
                    "Error":"Unauthorized"
                }
            return json.dumps(data),401
        
    else:
        data={
            "Error":"Invalid Request"
        }
        return json.dumps(data),400
