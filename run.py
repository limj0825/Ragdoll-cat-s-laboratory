from flask import Flask, render_template
from pymongo import MongoClient
from config import db_config, app_config
from flask import request, abort
from models.db_utility import auth_db
from models.app_utility import success, failure
import math
import time

db = MongoClient(host=db_config['host'], port=db_config['port'])[
    db_config['db_name']
]
app = Flask(__name__)
app.config['SECRET_KEY'] = app_config['secret_key']
message = db['message']
records = db['records']


@app.before_request
def judge():
    now_time = math.ceil(time.time())
    ip = request.remote_addr
    if records.count_documents({'name': 'ip'}) == 0:
        records.insert_one({'name': 'ip', 'denied': []})
    denied = list(records.find_one({'name': 'ip'})['denied'])
    if ip in denied:
        ip_records = list(records.find_one({'name': ip})['notes'])
        if now_time - ip_records[0] >= 3600:
            records.update_one({'name': ip}, {"$set": {"notes": []}})
            denied.remove(ip)
            records.update_one({'name': 'ip'}, {"$set": {"denied": denied}})
        else:
            abort(401)
    else:
        if records.count_documents({'name': ip}) == 0:
            records.insert_one({'name': ip, 'notes': []})
        notes = records.find_one({'name': ip})['notes']
        while len(notes) > 0 and now_time - notes[0] >= 30:
            notes = notes[1:]
        notes.append(now_time)
        records.update_one({'name': ip}, {"$set": {"notes": notes}})
        if len(notes) >= 60:
            denied.append(ip)
            records.update_one({'name': 'ip'}, {"$set": {"denied": denied}})
            abort(401)
        else:
            pass


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/api/message', methods=['GET'])
def messages():
    try:
        ip = request.remote_addr
        name = request.args.get('name')
        text = request.args.get('text')
        now_time = time.asctime(time.localtime(time.time()))
        message.insert_one({'name': name, 'text': text, 'ip': ip, 'time': now_time})
        return success("")
    except Exception as e:
        return failure(repr(e))


@app.route('/admin/message')
def show():
    data = message.find()
    my_data = []
    for x in data:
        if 'time' in x:
            my_data.append(x['time'])
        else:
            my_data.append("Mon Jan 1 00:00:00 1970")
        if 'ip' in x:
            my_data.append(x['ip'])
        else:
            my_data.append('0.0.0.0')
        my_data.append(x['name'])
        my_data.append(x['text'])
    return render_template('message.html', data=my_data)


@app.route('/admin')
def admin():
    return render_template('admin.html')


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=80, debug=True, threaded=True)
