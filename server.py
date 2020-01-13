from flask import Flask, jsonify
from flask import request
from flask_pymongo import PyMongo
import sys
import os
import copy

app = Flask(__name__)

app.config["MONGO_URI"] = "mongodb://jj:jems101@ds139934.mlab.com:39934/escape-db?retryWrites=false"
mongo = PyMongo(app)

EventRecord = {
    "Category": None,
    "Country" : None,
    "Address" : None,
    "LatLong" : None,
    "Event" : None,    
    "Days" : None,
    "Hours": None,
    "Price" : None,
    "Phone Number": None,
    "Booking Url" : None,
    "Email": None,
}
filename = sys.argv[1]

def placeInDataBase (filename):

    if not os.path.isfile(filename):
        print("File Path {} does not exist. Exiting... ".format(filename))
    else:
        file = open(filename)
        line = file.readline()
        count = 1
        while line:
            EventList = line.split("|")
            NewRecord = copy.deepcopy(EventRecord)
            NewRecord["Category"] = EventList[0]
            NewRecord["Country"]  = EventList[1]
            NewRecord["Address"]  = EventList[2]
            NewRecord["LatLong"]  = EventList[3]
            NewRecord["Event"]    = EventList[4]
            NewRecord["Days"]     = EventList[5]
            NewRecord["Hours"]    = EventList[6]
            NewRecord["Price"]    = EventList[7]
            NewRecord["Phone"]    = EventList[8]
            NewRecord["BookingUrl"] = EventList[9]
            NewRecord["Email"]      = EventList[10]
            mongo.db.users.insert_one(NewRecord)
            line = file.readline()
            count+=1

        file.close()
        print("read file succesfully!")

@app.route('/')
def index():
    return '<h1> Hello JJ </h1>'

@app.route('/data')
def detData():
    #Returns Cursor Object 
    query = mongo.db.users.find()
    #Json Object
    payload = []
    for doc in query:
        content = {'id' : doc[0], 'Category': doc[1], 'Country': doc[2], 
        'Address': doc[3], 'LatLong':doc[4], 'Event':doc[5], 'Days': doc[6], 
        'Hours': doc[7], 'Price':doc[8], 'BookingUrl':doc[9], 'Email': doc[10]}
        payload.append(content)
        content = {}
    return jsonify(payload)

@app.route('/user/<name>')
def user(name):
    return '<h1>Hello, {}!</h1>'.format(name)

@app.route('/data', methods=['GET', 'POST'])
def data():
    if request.method == 'POST':
        print(request.form['value'])
        print(request.form['print'])
        return "Got it working"

if __name__ == "__main__":
    app.run()