from flask import Flask 
from flask_pymongo import PyMongo 

app = Flask(__name__, instance_relative_config=True)
app.config.from_object('config')
config = app.config.from_pyfile('config.py')

def getMongo():
    user = app.config['AUTHUSER']
    password = app.config['AUTHPASSWORD']
    app.config['MONGO_URI'] = f"mongodb://{user}:{password}@ds237717.mlab.com:37717/loginplayground?retryWrites=false"

    mongo = PyMongo(app)
    return mongo
