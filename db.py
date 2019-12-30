from flask import Flask 
from flask_pymongo import PyMongo 

app = Flask(__name__)
app.config["MONGO_URI"] = "mongodb://jj:jems101@ds139934.mlab.com:39934/escape-db"
mongo = PyMongo(app)