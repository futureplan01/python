from flask import Flask, jsonify, request
from flask_pymongo import PyMongo
from flask_api import status
from flask_cors import CORS
from flask_bcrypt import Bcrypt
import requests
import eventDB
import authDB
import sys
import os
import copy

app = Flask(__name__)
CORS(app)
bcrypt = Bcrypt(app)

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
        mongo = eventDB.getMongo()
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
    mongo = eventDB.getMongo()
    query = mongo.db.users.find()
    #Json Object
    payload = []
    for doc in query:
        content = {'id' : doc['_id'].__str__(), 'Category': doc['Category'], 'Country': doc['Country'], 
        'Address': doc['Address'], 'LatLong':doc['LatLong'], 'Event':doc['Event'], 'Days': doc['Days'], 
        'Hours': doc['Hours'], 'Price':doc['Price'], 'BookingUrl':doc['BookingUrl'], 'Email': doc['Email']}
        payload.append(content)
        content = {}
    return jsonify(payload)
@app.route('/all-users')
def getUsers():
    mongo = authDB.getMongo()
    query = mongo.db.users.find()
    payload = []
    for doc in query:
        content= {
            "id": doc["_id"].__str__(),
            'email': doc['email'],
            'password': doc['password']
        }
        payload.append(content)
        content= {}
    return jsonify(payload)


#AUTHENTICATION 
@app.route('/sign-up', methods = ['POST', 'GET'])
def signUp():
    if(request.method == 'POST'):
        email = request.form.get('email')
        name = request.form.get('name')
        password  = request.form.get('password')
        mongo = authDB.getMongo()
        user = mongo.db.users.find({"email": email})
        if user == None :
            pw_hash = bcrypt.generate_password_hash(password)
            document = {
                "name": name,
                "email": email,
                "password": pw_hash
            }
            mongo.db.users.insert_one(document)
            return "Successful", status.HTTP_200_OK
            
        else:
            return "User Exist Already", status.HTTP_400_BAD_REQUEST

@app.route('/log-in', methods = ['POST', 'GET'])
def login():
    if(request.method == 'POST'):
        email = request.form.get('email')
        password  = request.form.get('name')
        mongo = authDB.getMongo()
        user = mongo.db.users.find({"email": email, "password": password})
        return status.HTTP_200_OK


    
@app.route('/get-countries')
def getCountry():
    """Select all distinct countries in our database"""
    mongo = eventDB.getMongo()
    query = mongo.db.users.distinct("Country")
    return jsonify(query)

@app.route('/tripify')
def getTripify():
    """Get's data from Tripify"""
    url = "https://tripadvisor1.p.rapidapi.com/locations/search"
    querystring={"location_id":"1", "limit":"30", "sort":"relevance", "offset":"0","lang":"en_US","currency":"USD","units":"km","query":"Iceland"}

    headers = {
        'x-rapidapi-host': "tripadvisor1.p.rapidapi.com",
        'x-rapidapi-key': "2a5f001934msh599ca02108c760bp1123ebjsn5f84d9230540"
    }

    response = requests.request("GET",url,headers=headers,params=querystring)
    return response.text

@app.route('/country-events', methods = ['POST', 'GET'])
def countryEvents():
    if request.method == 'POST':
        """Needs Country Name, Gets all events for that country"""
        mongo = eventDB.getMongo()
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