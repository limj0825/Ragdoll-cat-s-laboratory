from flask import Flask, render_template
from pymongo import MongoClient
from config import db_config, app_config
from flask import request
from models.db_utility import auth_db
from models.app_utility import success, failure

db = MongoClient(host=db_config['host'], port=db_config['port'])[
    db_config['db_name']
]
app = Flask(__name__)
app.config['SECRET_KEY'] = app_config['secret_key']
message = db['message']


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/api/message', methods=['GET'])
def messages():
    try:
        name = request.args.get('name')
        text = request.args.get('text')
        message.insert_one({'name': name, 'text': text})
        return success("")
    except Exception as e:
        return failure(repr(e))


@app.route('/admin/message')
def show():
    data = message.find()
    my_data = []
    for x in data:
        my_data.append(x['name'])
        my_data.append(x['text'])
    return render_template('message.html', data=my_data)


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=80, debug=True)
