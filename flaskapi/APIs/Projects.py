import time
from flask import Blueprint,request
from flaskapi.Lib.func import *
from flaskapi.Lib.Projects_class import Projects


import json
project_api = Blueprint('project_api',__name__)


@project_api.route('/projects/create',methods=['POST'])
def create_project():
    request_data = request.form or request.get_json()
    projectname = request_data.get('Project_Name').lower()
    if projectname:
        token=request.headers.get('Authorization')
        if token is None:
            data={
                    "Error":"Unauthorized"
                }
            return json.dumps(data),401
        if is_valid(token):
            if check_if_admin(token):

                try:
                    x=Projects().create_project(projectname)

                    if x:
                        data = {
                            "Message":"Project created successfully",
                            "Project_Name":projectname
                        }
                        return json.dumps(data),200
                
                except Exception as e:
                    data={
                        "Error":str(e)
                    }

                    return json.dumps(data),400
            else:
                data={
                    "Error":"You are Not an Admin to Process this Request"
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

@project_api.route("/projects/adduser",methods=["POST"])
def adduser():
    request_data = request.form or request.get_json()
    projectname = request_data.get("projectname").lower()
    project_members=request_data.get("project_members")

    x=project_members.split(",")
    if project_members and projectname:
        token=request.headers.get('Authorization')
        if token is None:
            data={
                    "Error":"Unauthorized"
                }
            return json.dumps(data),401
        
        if is_valid(token):

            if check_if_head(token,projectname.lower()) or check_if_admin(token):

                try:
                    a=Projects().add_user(projectname.lower(),x)
                    data={
                        "Message":"Members added to Project Successfully",
                        "Data":{
                            "Project_Name":a['Project_Name'],
                            "Project_Head":a['Project_Head'],
                            "duration":a['duration'],
                            "members":a['members'],
                            "Description":a['Description'],
                            "active":a['active'],
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
                    "Error":"You Dont Have Access to this Project. Contact your administrator"
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

@project_api.route('/projects/assignhead',methods=['POST'])
def assignhead():

    request_data = request.form or request.get_json()
    projectname= request_data.get('Projectname').lower()
    projecthead= request_data.get('Projecthead')

    if projectname and projecthead:
        token=request.headers.get('Authorization')
        if token is None:
            data={
                    "Error":"Unauthorized"
                }
            return json.dumps(data),401
        
        if is_valid(token):

            if check_if_admin(token):
                
                try:

                    x=Projects().assign_head(projectname.lower(),projecthead.lower())
                    if x:
                        data={
                            "Message":"Project Head was successfully assigned"
                        }
                        return json.dumps(data),200

                except Exception as e:
                    data={
                        'Error':str(e)
                    }
                    return json.dumps(data),400
            else:
                data={
                    "Error":"You do not have permission to access this resource. Contact your administrator"
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
    
@project_api.route('/projects/getteammembers', methods=['POST'])
def getteammembers():
    request_data = request.form or request.get_json()
    projectname = request_data.get('Projectname')

    if projectname:
        projectname=projectname.lower()

        token = request.headers.get('Authorization')
        if token is None:
            data={
                    "Error":"Unauthorized"
                }
            return json.dumps(data),401
        
        if is_valid(token):

            if check_if_admin(token) or check_if_head(token):

                try:

                    x=Projects().getteammembers(projectname)
                    data={
                        "Project Head":x['Head'],
                        "Project Members":x['Members']
                    }
                    return json.dumps(data),200
                
                except Exception as e:
                    data={
                        'Error':str(e)
                    }
                    return json.dumps(data),400
            else:
                data={
                    "Error":"You do not have permission to access this resource. Contact your administrator"
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
            
@project_api.route('/projects/getprojects', methods=['POST'])
def get_user_projects():

        token = request.headers.get('Authorization')
    
        if token is None:
            data={
                    "Error":"Unauthorized"
                }
            return json.dumps(data),401
        
        if is_valid(token):

                try:

                    x=Projects().get_user_projects(token.split(' ')[1])
                    data={
                        "Success":1,
                        "data":x
                    }
                    return json.dumps(data),200
                
                except Exception as e:
                    data={
                        'Error':str(e)
                    }
                    return json.dumps(data),400
            
        else:
            data={
                    "Error":"Unauthorized"
                }
            return json.dumps(data),401

@project_api.route("/projects/getprojects/all",methods=["POST"])
def getprojects():
    token = request.headers.get('Authorization')
    
    if token is None:
        data={
            "Error":"Unauthorized"
            }
        return json.dumps(data),401

    if is_valid(token):
        print(check_if_admin(token))

        if check_if_admin(token) or check_if_superuser(token):
            a=Projects().getprojects()
            data={
                "Success":1,
                "data":a
            }
            # return json.dumps(data),200
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

@project_api.route("/projects/getproject/<id>",methods=["POST"])
def get_project_with_id(id:id):
    token = request.headers.get('Authorization')
    
    if token is None:
        data={
            "Error":"Unauthorized"
            }
        return json.dumps(data),401

    if is_valid(token):

        if check_if_admin(token) or check_if_superuser(token):

            try:
                a=Projects().getproject_with_id(int(id))
                data={
                    "Success":1,
                    "data":a
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
            return json.dumps(data),403
    else:
        data={
            "Error":"Unauthorized"
        }
        return json.dumps(data),401


