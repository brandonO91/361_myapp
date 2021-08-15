from flask import Flask, render_template, request, redirect
from flask.helpers import url_for
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, PasswordField
from flask_sqlalchemy import SQLAlchemy
from os import environ #detect if heroku url is available
from flask_restful import Resource, Api
import requests #pip install requests
import json

app = Flask(__name__)
api = Api(app)

app.config['SECRET_KEY'] = 'mysecret'
app.config['SQLALCHEMY_DATABASE_URI'] = environ.get('DATABASE_URL') or 'sqlite:///myDB.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)


todos = ["Learn Flask", "Setup venv", "Build a cool app"]

class Technique(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    userName = db.Column(db.String(50), index=True)
    todo_text = db.Column(db.String(100), index = True)

class Login(FlaskForm):
    userName = StringField("User Name")
    password = PasswordField("Password")
    submit = SubmitField("Login") #will be a post request to given url

class NewUser(FlaskForm):
    userName = StringField("User Name")
    password = PasswordField("Password")
    retypePassword = PasswordField("Retype Password")
    submit = SubmitField("Create User")

db.create_all()

# to send data to api micro use json object with {"username" = "****", "password" = "****"} to 18.191.218.11:5000/register
# if creating use 18.191.218.11:5000/login with same info
# correct will return {"msg":"Login successful", "status":200}
@app.route('/', methods=["GET", "POST"])
def index():
    if 'userName' in request.form: # if there is a todo field within form from request
        # print(request.form['userName'])
        # print(request.form['password'])
        if len(request.form['password']) >= 8 and len(request.form['password']) <= 18:
            url = 'http://18.191.218.11:5000/login'
            user = {}
            userName = request.form['userName']
            password = request.form['password']
            user["username"] = userName
            user["password"] = password
            user = json.dumps(user)
            status = requests.post(url, json = user)
            print(status.json())
            return redirect(url_for("technique", userName=request.form['userName']))
        # db.session.add(Todo(todo_text=request.form['todo']))  #  create new new submission to DB from todo label
        # db.session.commit()
        else:
            return "<h1>incorrect password type</h1>"
    return render_template('index.html', template_form=Login())

@app.route('/newUser', methods=["GET", "POST"])
def newUser():
    if 'userName' in request.form:
        if len(request.form['password']) >= 8 and len(request.form['password']) <= 18:
            if request.form['password'] == request.form['retypePassword']:
                url = 'http://18.191.218.11:5000/register'
                user = {}
                userName = request.form['userName']
                password = request.form['password']
                user["username"] = userName
                user["password"] = password
                user = json.dumps(user)
                status = requests.post(url, json = user)
                print(user)
                print(status.json())
                print(status.ok)
                print(status.status_code)
                return redirect(url_for("index"))
    return render_template("newUser.html", template_form=NewUser())

@app.route('/<userName>', methods=["GET", "POST"])
def technique(userName):
    return userName

# create folder to hold project
# created a venv for myapp -> python3 -m venv myapp
# source bin/activate

# dependencies ---
# pip install flask
# pip install flask_wtf
# pip install flask_sqlalchemy

# setting up DB ---
# db.create_all() -> just delete file to clear DB?
# add by hand instances by going to create_todos.py and run ->python3 create_todos.py
# check out creat_todos.py for examples

# heroku setup ---
# check and if not installed do so with heroku cli
# make sure app root has git initiate ->git init
# create heroku app that is connect with CLI-> heroku create
# creating a heroku app will create a url
# modify the app to establish a DB that can be used with heroku (postgres)
# -> pip install psycopg2 --allows sqlalchemy to interact with postgres
# if pip install psycopg2 doesnt work, use -> pip install --upgrade setuptools
# if that doesnt work try -> pip install --upgrade pip
# if psycopg2 is giving errors when pushing to heroku try -> pip uninstall psycopg2 -> pip list --outdated -> pip install --upgrade wheel -> pip install --upgrade setuptools -> pip install psycopg2
# -> heroku addons:create heroku-postgresql:hobby-dev -- can get url for DB from setting in heroku app
# create server that can be used with heroku -> pip install gunicorn
# create a file that will heroku what dependencies are needed (will need to be done every time one is added)
# -> pip freeze > requirements.txt
# then create procfile which will tell heroku how to run app
# Procfile -> web: (server to use) (where main app is):(what we call our main app ex. app)
# make sure everything is added, commited to git repo
# -> git push heroku master (did not push all files up, will see if causes errors)
# create db on heroku app
# -> heroku run python -> from app import db


