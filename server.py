from flask import Flask 
from flask import request
from flask_pymongo import PyMongo

app = Flask(__name__)

app.config["MONGO_URI"] = "mongodb://jj:jems101@ds139934.mlab.com:39934/escape-db?retryWrites=false"
mongo = PyMongo(app)

record = {
    "hi": "JJ"
}

@app.route('/')
def index():
    mongo.db.users.insert_one(record)
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