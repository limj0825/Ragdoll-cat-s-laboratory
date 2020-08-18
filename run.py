from flask import Flask, render_template
from pymongo import MongoClient
from config import db_config, app_config, my_password
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
rabbit = db['rabbit']
rabbit_message = db['rabbit_message']


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


@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html')


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/api/message', methods=['POST'])
def messages():
    try:
        request_json = request.get_json(force=True)
        ip = request.remote_addr
        name = request_json['name']
        text = request_json['text']
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


@app.route('/api/delete_message', methods=['POST'])
def delete_message():
    try:
        request_json = request.get_json(force=True)
        password = request_json['password']
        assert(password == my_password)
        if 'name' in request_json:
            name = request_json['name']
            count = message.delete_many({'name': name}).deleted_count
        else:
            text = request_json['text']
            count = message.delete_many({'text': text}).deleted_count
    except AssertionError as e:
        return failure("管理员密码错误")
    except Exception as e:
        return failure(repr(e))
    else:
        return success(count)


@app.route('/api/change', methods=['POST'])
def change():
    try:
        request_json = request.get_json(force=True)
        old_password = request_json['old_password']
        now_password = rabbit.find()[0]['password']
        assert(now_password == old_password)
        rabbit.update_one({"password": old_password}, {"$set": {"password": request_json['new_password']}})
    except AssertionError as e:
        return failure("旧密码错误")
    except Exception as e:
        return failure(repr(e))
    else:
        return success("密码修改成功")


@app.route('/vote')
def vote():
    return render_template('vote.html')


@app.route('/admin')
def admin():
    return render_template('admin.html')


@app.route('/laboratory')
def test():
    return render_template('laboratory.html')


@app.route('/<password>')
def rabbit_page(password):
    if rabbit.count() == 0:
        rabbit.insert_one({'password': 'rabbit'})
    now_password = rabbit.find()[0]['password']
    if now_password != password:
        return render_template('404.html')
    data = rabbit_message.find()
    my_data = []
    for x in data:
        my_data.append(x['time'])
        my_data.append(x['ip'])
        my_data.append(x['name'])
        my_data.append(x['text'])
    return render_template('rabbit.html', data=my_data)


@app.route('/api/rabbit_message', methods=['POST'])
def send_message():
    try:
        request_json = request.get_json(force=True)
        ip = request.remote_addr
        name = request_json['name']
        text = request_json['text']
        now_time = time.asctime(time.localtime(time.time()))
        rabbit_message.insert_one({'name': name, 'text': text, 'ip': ip, 'time': now_time})
        return success("")
    except Exception as e:
        return failure(repr(e))


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=80, debug=True, threaded=True)
