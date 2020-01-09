from flask import Flask 
from flask import request
app = Flask(__name__)

@app.route('/')
def index():
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