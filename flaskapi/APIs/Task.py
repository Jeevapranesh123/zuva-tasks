import time
from flask import Blueprint,request
from flaskapi.Lib.func import *
from flaskapi.Lib.Task_class import Task
import pprint

import json
task_api = Blueprint('task_api',__name__)

@task_api.route('/task/add',methods=['POST'])
def add_task():

    people=None
    due=None
    project_name=None
    reward_point=10
    priority=None

    request_data = request.form or request.get_json()
    taskname = request_data.get('Taskname')
    if request_data.get('due') :
        due = int(request_data.get('due'))
    if request_data.get('projectname'):
        project_name = request_data.get('projectname')
    if request_data.get('reward_point'):
        reward_point = request_data.get('reward_point')
    if request_data.get('priority'):
        priority=request_data.get('priority')
    if request_data.get('Members'):
        people = request_data.get('Members')
    people=people.split(',')
    
    if taskname:

        token=request.headers.get('Authorization')
        if token is None:
            data={
                "Error":"Unauthorized"
            }
            return json.dumps(data),401

        if is_valid(token):

            if check_if_admin(token) or check_if_head(token):

                try:
                    x=Task().add_task(taskname,people,due,project_name,reward_point,priority)

                    if x:

                        data={
                            "Message":"Task added successfully",
                            "Task":{
                                "Task_id":x['Task_id'],
                                "Task_Name":x['Task_Name'],
                                "is_project_Task":x['is_project_Task'],
                                "project_info":x['project_info'],
                                "task_member":x['task_member'],
                                "due":x['due'],
                                "Priotiry":x['Priotiry'],
                                "Rewars_points":x['Rewars_points']
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
                    "Error":"You don't have permission to access this resource. Contact your administrator'"
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


@task_api.route('/task/getusertasks', methods=['POST'])
def get_user_tasks():
        # request_data = request.form or request.get_json()

        token = request.headers.get('Authorization')
    
        if token is None:
            data={
                    "Error":"Unauthorized"
                }
            return json.dumps(data),401
        
        if is_valid(token):

                try:

                    x=Task().get_user_tasks(token.split(' ')[1])
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

    
@task_api.route('/task/all', methods=['POST'])
def gettasks():

    token = request.headers.get('Authorization')
    if token is None:
            data={
                "Error":"Unauthorized"
            }
            return json.dumps(data),401

    if is_valid(token):
        if check_if_admin(token) or check_if_superuser(token):

            a=Task().getasks()
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

@task_api.route('/task/<id>', methods=['POST'])
def get_tasks_with_id(id:id):

    token = request.headers.get('Authorization')
    if token is None:
            data={
                "Error":"Unauthorized"
            }
            return json.dumps(data),401

    if is_valid(token):
        if check_if_admin(token) or check_if_superuser(token):
            try:


                a=Task().get_task_with_id(int(id))
                data={
                    "Success":1,
                    "data":a
                }
                return json.dumps(data),200
            
            except Exception as e:
                data={
                    "Error":str(e),
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