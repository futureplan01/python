from flask import Flask 
from flask_pymongo import PyMongo 


app = Flask(__name__, instance_relative_config=True)
app.config.from_object('config')
config = app.config.from_pyfile('config.py')

def getMongo ():
    user = app.config['DBUSER']
    password = app.config['DBPASSWORD']
    app.config["MONGO_URI"] = f"mongodb://{user}:jems101@ds139934.mlab.com:39934/escape-db?retryWrites=false"

    mongo = PyMongo(app)
    return mongo