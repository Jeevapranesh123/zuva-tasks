import pymongo
from flaskapi.Lib.client import client

# client=pymongo.MongoClient('localhost')

                            
db = client.TaskManager
Project = db.Projects
Members=db.Members
Sessions = db.Sessions

class Projects:

    def __init__(self):
        pass

    def create_project(self, projectname):
        '''This Function Creates a new Project in the database
        
        Parameters:
        arg1(string): The name of the project to create
        
        Retruns:
        dict: A dictionary containing the project information'''

        a=Project.find_one({'Project_Name': projectname})
        if a:
            raise Exception("Project {} already exists".format(projectname))

        a=Project.find()
        max=0

        for i in a:

            if i['Project_id']>max:
        
                max=i['Project_id']
        
        data={
            "Project_id":max+1,
            "Project_Name":projectname,
            "Project_Head":None,
            "duration":None,
            "members":[],
            "Description":"",
            "active":True,
        }

        if Project.insert_one(data):
            return data
        else:
            raise Exception("Project Not Created")
    
    def add_user(self,projectname,username):
            if not Project.find_one({'Project_Name':projectname}):
                raise Exception("Project Not Found")

            for i in username:
                if not Members.find_one({'name':i.lower()}):
                    raise Exception("{} Not Found in Members list".format(i))


            filter = { 'Project_Name':projectname }
    
            newvalues = { "$set": { 'members':username} }
    
            if Project.update_one(filter, newvalues):
                x=Project.find_one({'Project_Name':projectname})
                print(x)
                return x
            else:
                return False

    def assign_head(self,projectname,projecthead):

        if Project.find_one({'Project_Name':projectname}):
            pass
        else:
            raise Exception("Project Not Found")

        filter = { 'Project_Name':projectname }

        newvalues = { "$set": { 'Project_Head':projecthead.lower() } }

        if Project.update_one(filter, newvalues):


            filter = { 'name':projecthead.lower() }

            newvalues = { "$set": { 'is_head':True } }

            if Members.update_one(filter, newvalues):

                if Members.find_one({'name':projecthead.lower()}):
                    x= Members.find_one({'name':projecthead.lower()})

                    head=x['head']
                    
                    if head is not None:
                        # head.append(projectname)
                     
                        if projectname in head:
                            pass
                        else:
                            head.append(projectname)
                    else:
                        head=[]
                        head.append(projectname)

                    
                else:
                    raise Exception("User Not Found in Members list")
            else:
                raise Exception("Unable to Update Members List")
                        

            filter = { 'name':projecthead.lower() }
    
            newvalues = { "$set": { 'head':head } }

            if Members.update_one(filter, newvalues):
                
                return True
            else:
                return False
        else:
            raise Exception("Project Head Unable to be updated")

        
    def getteammembers(self, projectname):

        a=Project.find_one({'Project_Name':projectname.lower() })
        
        if a:
            members =[]
            for i in a['members']:
                members.append(i)
            data ={
                "Head":a['Project_Head'],
                "Members":members
            }
            return data
        else:
            raise Exception("Project Not Found")

    def get_user_projects(self,token):

        a=Sessions.find_one({'token':token,'active':True})
        
        if a:
            name=a['username']
            email=a['email']
        else:
            raise Exception("Session Not Found")

        data=[]

        x=Project.find()

        for i in x:
            for x in i['members']:
                if x.lower() == name.lower():
                    del i['_id']
                    data.append(i)

        return data


    def getprojects(self):

        data=[]
        x=Project.find()
        for i in x:
            del i['_id']
            data.append(i)

        return data

    def getproject_with_id(self, project_id:int):

        x=Project.find()
        for i in x:
            if i['Project_id']==project_id:
                del i['_id']
                return i
        else:
            raise Exception("Project Not Found")


    

