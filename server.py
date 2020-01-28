from flask import Flask, jsonify, request
from flask_pymongo import PyMongo
from flask_api import status
from flask_cors import CORS
import db
import sys
import os
import copy

app = Flask(__name__)
CORS(app)

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



def placeInDataBase ():
    
    """Read Text file from directory and places the data into a database"""
    filename = sys.argv[1]
    if not os.path.isfile(filename):
        print("File Path {} does not exist. Exiting... ".format(filename))
    else:
        file = open(filename)
        line = file.readline()
        count = 1
        mongo = db.getMongo()
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

@app.route('/all-events')
def getData():
    """Returns all events in the Database"""
    mongo = db.getMongo()
    query = mongo.db.users.find()
    #Json Object
    payload = []
    for doc in query:
        print(doc)
        content = {'id' : doc['_id'].__str__(), 'Category': doc['Category'], 'Country': doc['Country'], 
        'Address': doc['Address'], 'LatLong':doc['LatLong'], 'Event':doc['Event'], 'Days': doc['Days'], 
        'Hours': doc['Hours'], 'Price':doc['Price'], 'BookingUrl':doc['BookingUrl'], 'Email': doc['Email']}
        payload.append(content)
        content = {}
    return jsonify(payload)


@app.route('/get-countries')
def getCountry():
    """Select all distinct countries in our database"""
    mongo = db.getMongo()
    query = mongo.db.users.distinct("Country")
    return jsonify(query)



@app.route('/country-events', methods = ['POST', 'GET'])
def countryEvents():
    if request.method == 'POST':
        """Needs Country Name, Gets all events for that country"""
        mongo = db.getMongo()
        # gets form data
        # if key doesn't exist, returns None
        country = request.form.get('Country')
        category = request.form.get('Category')
        print("Country: ", country)
        print("Categoy: ", category)
        if country == None:
            return status.HTTP_400_BAD_REQUEST

        if category == None or category == "All":
            query = mongo.db.users.find({"Country": country})
        else:
            query = mongo.db.users.find({"Country": country, "Category": category})

        print(query)
        payload = []
        for doc in query:
            content = {'id' : doc['_id'].__str__(), 'Category': doc['Category'], 'Country': doc['Country'], 
            'Address': doc['Address'], 'LatLong':doc['LatLong'], 'Event':doc['Event'], 'Days': doc['Days'], 
            'Hours': doc['Hours'], 'Price':doc['Price'], 'BookingUrl':doc['BookingUrl'], 'Email': doc['Email']}
            payload.append(content)
        return jsonify(payload)


if __name__ == "__main__":
    app.run()