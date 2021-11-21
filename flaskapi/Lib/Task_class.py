import re
import pymongo
import secrets
import time
import json
from flaskapi.Lib.client import client

# client =pymongo.MongoClient('localhost')
db = client.TaskManager
Tasks = db.Task
Sessions = db.Sessions
Projects = db.Projects

class Task:

    def __init__(self):
        pass

    def add_task(self,Task_name,people=None,due=None,project_name=None,reward_point=10,priority=None):

        a=Tasks.find()
        max=0

        for i in a:

            if i['Task_id']>max:
        
                max=i['Task_id']

        if project_name:
            data={
                "Task_id":max+1,
                "Task_Name":Task_name,
                "is_project_Task":True,
                "project_info":[
                    project_name
                ],
                "task_member":people,
                "due":due,
                "Priotiry":priority,
                "Rewars_points":reward_point,
                "active":True
            }

        else:
            data={
                 "Task_id":max+1,
                "Task_Name":Task_name,
                "is_project_Task":False,
                "project_info":[],
                "task_member":people,
                "due":due,
                "Priotiry":priority,
                "Rewars_points":reward_point,
                "active":True
            }
        
        if Tasks.insert_one(data):
            return data
        else:
            raise Exception("Task Not Added")

    def get_user_tasks(self,token):

        a=Sessions.find_one({'token':token,'active':True})
        
        if a:
            name=a['username']
            email=a['email']
        else:
            raise Exception("Session Not Found")

        data=[]

        a=Tasks.find()
        for i in a:
            for x in i['task_member']:
                if x.lower() == name.lower():
                    del i['_id']
                    data.append(i)
        
        return data

    def getasks(self,):

        a=Tasks.find()

        data=[]
        for i in a:
            del i['_id']
            data.append(i)

        return data

    def get_task_with_id(self, id:int):

        x=Tasks.find()
        for i in x:
            if i['Task_id']==id:
                del i['_id']
                return i
        else:
            raise Exception("Task Not Found")


