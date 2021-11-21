from re import A
import re
from traceback import print_list
from flask import Flask,render_template
from flaskapi.APIs.Auth import auth_api
from flaskapi.APIs.Projects import project_api
from flaskapi.APIs.Task import task_api
from flaskapi.APIs.Admin import admin_api
from flaskapi.APIs.Superuser import super_api
from flaskapi.APIs.Head import *
import pymongo
import json
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address

app=Flask(__name__)
app.register_blueprint(auth_api)
app.register_blueprint(project_api)
app.register_blueprint(head_api)
app.register_blueprint(task_api)
app.register_blueprint(admin_api)
app.register_blueprint(super_api)

# limiter = Limiter(app, key_func=get_remote_address)
#
# @limiter.limit("5/minute")
@app.route('/')
def home():
    # return "Welcome to Zuva Tech: "
    return render_template('index.html')

@app.route('/test')
def test():
    client=pymongo.MongoClient(host="mongodb",
                            port=27017,
                            username="root",
                            password="pass",
                            authSource="admin")
    if client:
        db=client.API
        user=db.User
        data = {
            'username':"jeeva",
            'email': 'abc',
            'Password': "abc123"
        }
        if user.insert_one(data):
            return "Inseted Successfully"
        else:
            return "Not Inserted"
    else:
        return "Problem in Connecting With Database"




if __name__ == '__main__':

    app.run(host='0.0.0.0',debug=True)


