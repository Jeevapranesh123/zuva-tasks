from flask import Blueprint,request
from flaskapi.Lib.func import *
from flaskapi.Lib.Superuser_class import *
import json

super_api = Blueprint('super_api',__name__)

@super_api.route('/superuser/makeadmin',methods=['POST'])
def makeadmin():
    request_data = request.form or request.get_json()
    username= request_data.get('Name')
    email= request_data.get('Email')

    if username and email:

        token = request.headers.get('Authorization')

        if token is None:
            data={
                    "Error":"Unauthorized"
                }
            return json.dumps(data),401
        
        if is_valid(token):

            if check_if_superuser(token):

                try:

                    a=Superuser().makeuseradmin(username,email)
                    data={
                        "Message":"Admin Update Success"
                    }
                    return json.dumps(data),200

                except Exception as e:

                    data={
                        "Error":str(e)
                    }
                    return json.dumps(data),400
                
            else:
                data={
                    "Error":"Unauthorized access to the Resource"
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

@super_api.route('/superuser/removeadmin', methods=['POST'])
def removeadmin():
        
    request_data = request.form or request.get_json()
    username= request_data.get('Name')
    email= request_data.get('Email')

    if username and email:

        token = request.headers.get('Authorization')

        if token is None:
            data={
                    "Error":"Unauthorized"
                }
            return json.dumps(data),401
        
        if is_valid(token):

            if check_if_superuser(token):

                try:

                    a=Superuser().removeadmin(username,email)
                    data={
                        "Message":"Admin Update Success"
                    }
                    return json.dumps(data),200

                except Exception as e:

                    data={
                        "Error":str(e)
                    }
                    return json.dumps(data),400
                
            else:
                data={
                    "Error":"Unauthorized access to the Resource"
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

@super_api.route('/superuser/makesuperuser',methods=['POST'])
def makesuperuser():
    username =None
    email =None
    request_data = request.form or request.get_json()
    if request_data is not None:
        username= request_data.get('Name')
        email= request_data.get('Email')

    if username and email:

        nakku = request.headers.get('Nakku')

        if nakku is None:
            data={
                    "Error":"Unauthorized"
                }
            return json.dumps(data),401
        
        if check_if_nakku(nakku):
                try:

                    a=Superuser().makesuperuser(username.lower().strip(),email.lower().strip())
                    data={
                        "Message":"Superuser Update Success"
                    }
                    return json.dumps(data),200

                except Exception as e:

                    data={
                        "Error":str(e)
                    }
                    return json.dumps(data),400
                
        else:
                data={
                    "Error":"Unauthorized access to the Resource"
                }
                return json.dumps(data),401
       
        
    else:
        data={
            "Error":"Invalid Request"
        }
        return json.dumps(data),400