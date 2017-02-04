from flask import Flask, render_template, redirect, request
from flask_login import LoginManager, login_user, logout_user
from flask_login import current_user, login_required
from pymongo import MongoClient
from flask_mongoengine import MongoEngine
from flask_mongoengine.wtf import model_form
from wtforms import PasswordField
import socket
import requests

app = Flask(__name__)
app.config["DEBUG"] = True
app.config['MONGODB_SETTINGS'] = {'db': 'users'}
app.config['SECRET_KEY'] = 'NYACT'
app.config['WTF_CSRF_ENABLED'] = True

login_manager = LoginManager()
login_manager.init_app(app)

s=socket.socket()
host=socket.gethostname()
port = 12345
s.bind((host,port))
s.listen(4)
user_access_token = s.recv(123)
s.close

def connect():
    client = MongoClient("ds056789.mlab.com", 56789)
    db = connection["nyact_db"]
    db.authenticate("nyact_db", "ny@ct1vist")
    return temp_handle

handle=connect()
campaigns_db = handle.nyact_db.campaigns_db
users_db= nyact_db.handle.users_db

class User:

    def __init__(self, username):
        self.username = username
    def is_authenticated(self):
        return True

    def is_active(self):
        return True

    def is_anonymous(self):
        return False

    def get_id(self):
        return self.username

    def add_campaigns_bylatlong(lat, long, radius, event_query, type): #radius in meters
        if(lat is None or long is None or radius is None):
            payload={'q':event_query, 'type': type}
            results = requests.get("http://graph.facebook.com/search?", params=payload)
        else:
            latlong = "%s%s%s" %(lat, ",", long)
            payload = {'q': event_query, 'type': type, 'center': latlong,'distance':radius }
            results = requests.get("http://graph.facebook.com/search?", params=payload)
            results.json()
            json_results = json.load(results)
            for(num in range(0,9)):
                for(e[num] in results):
            campaigns_db.insert_one({'event_name': event_name,'date': date, 'location': location, 'type': type, 'event_desc': event_description,'img_link': img})

@app.route("/")
def homepage():
    recommended_campaigns=[10]
    #FUNCTION TO POPULATE CAMPAIGNS_DB!!!
    populate_campaigns_db()
    campaigns_db
    return render_template("index.html")

@login_manager.user_loader
def load_user(name):
    users = db_user.find_one({"username": name})
    if len(users) != 0:
        return User(users['username'])
    else:
        return None


@app.route("/register", methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        username = request.form.get('username', None)
        password = request.form.get('password', None)
        try:
            interest_str = request.form.get('interests', None)
            interests = []
            interests = interest_str.split()
        except:
            return False
        if users_db.find_one({'username': username}) is None:
            users_db.insert_one({'username': username, 'password': password, 'interests': interests})
            return redirect("/login")
        return redirect("/signup")
    else:
        return render_template("signup.html")

@app.route("/login", methods=['GET', 'POST'])
def login():
    if request.method == 'POST'
        username = request.form.get('username', None)
        password = request.form.get('password', None)
        if user is None:
            return redirect("/login")
        elif user["password"] == password:
            return redirect("/")
        else:
            return redirect("/login")
    else:
        return render_template('login.html')

@app.route("/")
def logout():
    logout_user()
    return redirect("/")



@app.route("/newcampaign")
def make_new_campaign():
    event_name = request.form.get('eventname', None)
    date = request.form.get('date', None)
    location = request.form.get('location', None)
    type = request.form.get('type, None')
    img = request.form.get('imglink', None)

    nyact_db.campaigns_db.insert_one({'event_name': event_name,'date': date, 'location': location, 'type': type, 'event_desc': event_description,'img_link': img})

    return redirect("/campaign<event_name>")

@app.route("/campaign<campaign_name>")
def display_campaign(campaign_name):
    campaign = list(campaigns_db.find({'event_name': campaign_name}))
    return render_template("campaign.html", campaign_name = campaign[0])

@app.route("/search<search_id>")
def search(search_id, filter):
    if(filter is None):
        search_results = []
        search_results = list(campaigns_db.find({search_id}))
        return render_template("searchresults.html", search_array=search_results)
    elif(search_id is None):
        return render_template("index.html")
    else:
        search_results = list(campaigns_db.find({filter: search_id}))
        return render_template("searchresults.html", search_array = search_results)




