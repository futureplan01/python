from flask import Flask 
from flask_pymongo import PyMongo 

def getMongo ():
    app = Flask(__name__)
    app.config["MONGO_URI"] = "mongodb://jj:jems101@ds139934.mlab.com:39934/escape-db?retryWrites=false"
    mongo = PyMongo(app)
    return mongo