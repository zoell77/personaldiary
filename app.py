from dotenv import load_dotenv
from flask import Flask, render_template, request, jsonify

from pymongo import MongoClient
from datetime import datetime

import os
from os.path import join, dirname
dotenv_path = join(dirname(__file__), '.env')
load_dotenv(dotenv_path)

MONGODB_URI = os.environ.get("MONGODB_URI")
DB_NAME =  os.environ.get("DB_NAME")

client = MongoClient(MONGODB_URI)
db = client[DB_NAME]

app = Flask(__name__)


@app.route('/')
def home():
    return render_template('index.html')

@app.route('/diary', methods=['GET'])
def show_diary():
    articles = list(db.diary.find({},{'_id':False}))
    return jsonify({'articles': articles})

@app.route('/diary', methods=['POST'])
def save_diary():
    title_receive = request.form.get('title_give')
    content_receive = request.form.get('content_give')
    today = datetime.now()
    mytime = today.strftime('%Y-%m-%d-%H-%M-%S')
    file = request.files["file_give"]
    extension = file.filename.split('.')[-1]
    filename = f'fileimage-{mytime}.{extension}'
    file.save(f'static/{filename}')
    
    profile = request.files['profile_give']
    extension = profile.filename.split('.')[-1]
    profilename = f'fileprofile-{mytime}.{extension}'
    profile.save(f'static/{profilename}')  
    time = today.strftime('%H.%m.%d.%Y')
    doc = {
        'file' : filename,
        'profile' : profilename, 
        'title' : title_receive,
        'content' : content_receive,
        'time' : time
        
    }
    db.diary.insert_one(doc)
    return jsonify({'msg': 'POST request complete!'})



if __name__ == '__main__':
    app.run('0.0.0.0', port=5000, debug=True)