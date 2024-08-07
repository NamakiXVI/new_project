from flask import Flask, render_template, request, redirect, url_for, jsonify, render_template_string, make_response
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import text
import requests
import platform
import os
import subprocess
import json
from datetime import datetime
import time

app = Flask(__name__, static_url_path='/static')
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///db.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

getTranslation = None
result = None
language = None
user_ip_address = None

get_user_ip = None
ip = None
country = None
region = None
city = None

creator = None
description = None
video_url = None
json_ = None
video_share = None


class Messages(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    user = db.Column(db.String(200), nullable = True)
    content = db.Column(db.String(1000), nullable = True)
    user_ip = db.Column(db.String(100), nullable = True)
    user_country = db.Column(db.String(100), nullable = True)
    user_region = db.Column(db.String(100), nullable = True)
    user_city = db.Column(db.String(100), nullable = True)
    creation_date = db.Column(db.DateTime(), default = datetime.utcnow)

class collect_data(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    user_content = db.Column(db.String(200), nullable = True)
    translation = db.Column(db.String(200), nullable = True)
    user_ip = db.Column(db.String(200), nullable = True)
    creation_date = db.Column(db.DateTime(), default = datetime.utcnow)

class tiktoks(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    video_url = db.Column(db.String(200), nullable = True)
    video_title = db.Column(db.String(200), nullable = True)
    video_creator = db.Column(db.String(200), nullable = True)
    video_share = db.Column(db.String(200), nullable = True)
    creation_date = db.Column(db.DateTime(), default = datetime.utcnow)

with app.app_context():
    db.create_all()

def delete_rows_by_condition(condition):
    rows_to_delete = tiktoks.query.filter(condition).all()

    for row in rows_to_delete:
        db.session.delete(row)

    db.session.commit()

def get_tiktoks(i):
    global creator
    global description
    global video_url
    global video_share

    if json_ is not None:
        creator = json_['aweme_list'][i]['author']['nickname']
        description = json_['aweme_list'][i]['desc']
        video_share = json_['aweme_list'][i]['share_url']
        video_url = json_['aweme_list'][i]['video']['play_addr']['url_list'][2]
    else:
        print(f"Error: json is None")

def tiktok_api():
    global json_

    url = "https://tiktok-all-in-one.p.rapidapi.com/feed"

    querystring = {"region":"DE","device_id":"7523368224928586621"}

    headers = {
        "X-RapidAPI-Key": "306409bd58mshc2423484a8dac13p1e127djsnd8a340bc12d5",
        "X-RapidAPI-Host": "tiktok-all-in-one.p.rapidapi.com"
    }

    response = requests.get(url, headers=headers, params=querystring)
    print(response.status_code)

    if response.status_code == 200:
        json_ = response.json()
        save_file = open("static/json_data/data.json" , "w")  
        json.dump(json_, save_file, indent = 6)  
        save_file.close()  
    else:
        print(response.status_code)
        tiktok_api()

    return json_

def get_user_info(ip_address):
    global ip
    global country
    global region
    global city

    try:
        url_ = 'https://ipinfo.io/' + str(ip_address) + '/json?token=9eafaf94800f36'

        response_ = requests.get(url_)

        print(response_.json())

        data_ = response_.json()

        country = data_['country']
        region = data_['timezone']
        city = data_['city']
        
        print(country)
        print(region)
        print(city)
    except:
        print('Error on Value of IP Address: ' + str(ip_address))

def tiktok_filtern(condition):
    rows_to_delete = tiktoks.query.filter(condition).all()

    for row in rows_to_delete:
        db.session.delete(row)

    db.session.commit()

def Translate(tString, cc):
    global result

    url = "https://translated-mymemory---translation-memory.p.rapidapi.com/get"

    querystring = {"langpair":"en|" + str(cc),"q": tString,"mt":"1","onlyprivate":"0","de":"a@b.c"}

    headers = {
	    "X-RapidAPI-Key": "0b2bd932d3mshc9d3922e8e75d40p1f9239jsn1c1d21dfd9e1",
	    "X-RapidAPI-Host": "translated-mymemory---translation-memory.p.rapidapi.com"
    }

    response = requests.get(url, headers=headers, params=querystring)
    data = response.json()
    result = data["responseData"]["translatedText"]

@app.route("/to-do_list", methods=['GET', 'POST'])
def to_do():
    return render_template("to-do-list.html")

@app.route("/valentinesday", methods=['GET', 'POST'])
def valentine():
    return render_template("docs.html")

@app.route("/", methods=['GET', 'POST'])
def deploy():
    if request.method == 'POST':
        getTranslation = request.form['tString']
        getLanguage = request.form['language']
        Translate(getTranslation, getLanguage)

        if user_ip_address == '' or None:
            print('no ip address received yet')
        else:
            new_data = collect_data(
                user_content = request.form['tString'],
                translation = result,
                user_ip = user_ip_address,
            )

            db.session.add(new_data)
            db.session.commit()

    return render_template('translate_web.html', result=result)

@app.route("/get_user-data", methods=['POST'])
def ip_transfer():
    global got_ip
    global user_ip_address

    data = request.get_json()
    user_ip_address = data.get('ip')

    return user_ip_address

@app.route("/chat", methods=['GET', 'POST'])
def login_page():
    if request.method == 'POST':
        time.sleep(1)

        new_Message = Messages(
            user = request.form['name'],
            content =  request.form['name'] + ' joined the chat',
        )

        db.session.add(new_Message)
        db.session.commit()

        return redirect(url_for('start_page', name=new_Message.user))

    print('website deployed')
    return render_template('login.html')

@app.route("/chat/<name>", methods=['GET', 'POST'])
def start_page(name):

    if request.method == 'POST':

        new_Message = Messages(
            user = name,
            content = request.form['content'],
            user_ip = get_user_ip,
            user_country = country,
            user_region = region,
            user_city = city,
        )
        db.session.add(new_Message)
        db.session.commit()

    messages_ = Messages.query.order_by(Messages.creation_date).all()
    return render_template('index.html', messages_=messages_, name=name)

@app.route("/mateo", methods=['GET', 'POST'])
def start_new_project():

    arr = tiktoks.query.order_by(tiktoks.id).all()
    tiktok_api()

    if len(arr) >= 150:
        db.session.execute(text('DROP TABLE IF EXISTS tiktoks'))
        db.session.commit()
        db.create_all()

    for i in range(0, 7):
        get_tiktoks(i)

        new_tiktok = tiktoks(
            video_url = video_url,
            video_title = description,
            video_creator = creator,
            video_share = video_share,
        )

        db.session.add(new_tiktok)
        db.session.commit()

    tiktok_filtern(tiktoks.video_url == None)

    tiktoks_ = tiktoks.query.order_by(tiktoks.id.desc()).all()
    return render_template('newtiktok.html', tiktoks_=tiktoks_)

@app.route("/get_user_data", methods=['POST'])
def receive_ip():
    global get_user_ip

    if request.method == 'POST':
        json_ip = request.get_json()
        get_user_ip = str(json_ip.get('ip'))
        get_user_info(get_user_ip)

    return get_user_ip

@app.route("/get_share_url", methods=['GET', 'POST'])
def send_share_url():
    latest_tiktok = tiktoks.query.order_by(tiktoks.id.desc()).first()

    share_url = make_response(
        jsonify
        (
            {
                "id":"test",
            }
        ),
        401,
    )

    return share_url

@app.route("/pu_dessem")
def learn_vul():
    return render_template("pu_dessem.html")
        
@app.route("/chat/get_json=format:401")
def chat_json_response():

    latest_message = Messages.query.order_by(Messages.id.desc()).first()

    chat_data = make_response (

        jsonify
        (
            {
                "id": latest_message.id,
                "user": latest_message.user,
                "content": latest_message.content,
                "user_ip": latest_message.user_ip,
                "user_country": latest_message.user_country,
                "user_region": latest_message.user_region,
                "user_city": latest_message.user_city,
                "creation_date": latest_message.creation_date,
            }
        ),
        200,
    )

    return chat_data

#bissel dumm eine API mithilfe einer API zu erstellen
@app.route("/latest_request/get_json=format:api=request")
def send_json():

    latest_data = collect_data.query.order_by(collect_data.id.desc()).first()

    user_data = make_response (
        jsonify (
        {
            "id": latest_data.id,
            "user_content": latest_data.user_content,
            "translation": latest_data.translation,
            "user_ip": latest_data.user_ip,
            "creation_date": latest_data.creation_date,
        }),
        401,
        )
    
    user_data.headers["Content-Type"] = "application/json"

    return user_data

@app.route('/py')
def index():
    return render_template('python.html')

@app.route('/java')
def java():
    return "Error 404: This Website doesn't exist"

@app.route('/execute', methods=['POST'])
def execute():
    code = request.form['code']
    filename = 'file.py'
    with open(filename, 'w') as f:
        f.write(code)

    if platform.system() == 'Windows':
        result = subprocess.run(['python', filename], capture_output=True, text=True)
    else:
        result = subprocess.run(['python3', filename], capture_output=True, text=True)

#        print("type: " + str(type(type_)))
#        output = subprocess.check_output(["python3", filename])
#        result = output.decode("utf-8")
#        print("output: " + result)
    
    return result.stdout if result.returncode == 0 else result.stderr

@app.route('/compile_execute', methods=['POST'])
def compile_execute():
    code = request.form['code']
    with open('Main.java', 'w') as file:
        file.write(code)
    compile_output = subprocess.getoutput('javac Main.java')
    if compile_output:
        return compile_output
    else:
        execution_output = subprocess.getoutput('java Main')
        return execution_output

if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=5000)

#(c) no copyright by Namaki / Tien Dat Nguyen (pls dont steal my code even though it isnt even mine)









