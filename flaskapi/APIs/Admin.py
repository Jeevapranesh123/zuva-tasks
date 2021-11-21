from flask import Blueprint,request
from flaskapi.Lib.func import *
from flaskapi.Lib.Admin_class import *
import json

admin_api= Blueprint('admin_api',__name__)

@admin_api.route('/admin/makeuseractive',methods=['POST'])
def makeuseractive():
    nakku = request.headers.get('Nakku')
    request_data = request.form or request.get_json()
    name = request_data.get('Name')
    email = request_data.get('Email')

    if name and email:
        token = request.headers.get('Authorization')
        nakku = request.headers.get('Nakku')
        if nakku is None:
            data={
                    "Error":"Unauthorized"
                }
            return json.dumps(data),401
    
        if check_if_nakku(nakku):
                
                try:

                        a=Admin().makeuseractive(name,email)
                        if a==True:

                            data={
                                "Message":"User Activated"
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


@admin_api.route("/admin/members",methods=["POST"])
def getmembers():
    token = request.headers.get('Authorization')
    if token is None:
        data={
            "Error":"Unauthorized"
            }
        return json.dumps(data),401

    if is_valid(token):

        if check_if_admin(token) or check_if_superuser(token):

            a=Admin().get_all_members()
            data={
                "Success":1,
                "data":a
            }
            return json.dumps(data),200

        else:
            data={
                "Error":"Cannot Perform Action. Contact Higher Authorities :)"
            }
            return json.dumps(data),403

    else:
        data={
            "Error":"Unauthorized"
        }
        return json.dumps(data),401

@admin_api.route("/admin/member/<id>",methods=["POST"])
def getmember_with_id(id:id):
    token = request.headers.get('Authorization')
    if token is None:
        data={
            "Error":"Unauthorized"
            }
        return json.dumps(data),401

    if is_valid(token):

        if check_if_admin(token) or check_if_superuser(token):

            a=Admin().get_members_with_id(int(id))
            data={
                "Success":1,
                "data":a
            }
            return json.dumps(data),200

        else:
            data={
                "Error":"Cannot Perform Action. Contact Higher Authorities :)"
            }
            return json.dumps(data),403

    else:
        data={
            "Error":"Unauthorized"
        }
        return json.dumps(data),401



    




