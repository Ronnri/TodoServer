from datashape import unicode
from flask import Flask, request, render_template,jsonify
import json

app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def home():
    return render_template('home.html')

@app.route('/signin', methods=['GET'])
def signin_form():
    return render_template('form.html')

@app.route('/test', methods=['POST'])
def testrespost():
    recData = json.loads(request.data)
    if recData['p4'] == "this is a post json":
        return "I've succeeded getting your post\n"
    return "I didn't get your post clearly\n"

@app.route('/test', methods=['GET'])
def testresget():
    jsonData={
        'param1':1,
        'param2':2,
        'param3':3,
        'param4':"i have got your get"
    }
    return jsonify(jsonData)

@app.route('/signin', methods=['POST'])
def signin():
    username = request.form['username']
    password = request.form['password']
    if username=='admin' and password=='1234':
        return render_template('signin-ok.html', username=username)
    return render_template('form.html', message='Bad username or password', username=username)

