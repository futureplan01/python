from flask import Flask 
from flask import request
from flask_pymongo import PyMongo
import sys
import os

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
        sys.exit()
    else:
        file = open(filename)
        line = file.readline()
        count = 1
        while line:
            EventList = line.split("|")
            EventRecord["Category"] = EventList[0]
            EventRecord["Country"]  = EventList[1]
            EventRecord["Address"]  = EventList[2]
            EventRecord["LatLong"]  = EventList[3]
            EventRecord["Event"]    = EventList[4]
            EventRecord["Days"]     = EventList[5]
            EventRecord["Hours"]    = EventList[6]
            EventRecord["Price"]    = EventList[7]
            EventRecord["Phone"]    = EventList[8]
            EventRecord["BookingUrl"] = EventList[9]
            EventRecord["Email"]      = EventList[10]
            print(EventRecord)
            line = file.readline()
            count+=1

        file.close()
        print("read file succesfully!")

@app.route('/')
def index():
    placeInDataBase(filename)
    return '<h1> Hello JJ </h1>'

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