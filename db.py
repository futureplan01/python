from flask import Flask 
from flask_pymongo import PyMongo 
import config

app = Flask(__name__)
def getMongo ():
    print(config.DBUSER, config.DBPASSWORD)
    app.config["MONGO_URI"] = "mongodb://{config.DBUSER}:{config.DBPASSWORD}@ds139934.mlab.com:39934/escape-db?retryWrites=false"
    mongo = PyMongo(app)
    return mongo