from flask import Flask, render_template
from pymongo import MongoClient
from config import db_config, app_config
from models.db_utility import auth_db

db = MongoClient(host=db_config['host'], port=db_config['port'])[
    db_config['db_name']
]
app = Flask(__name__)
app.config['SECRET_KEY'] = app_config['secret_key']
message = db['message']
test = {'name': 'mr.lee', 'message': 'hello world'}
#x = message.insert_one(test)
#print(x)

@app.route('/')
def index():
    return render_template('index.html')


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=80, debug=True)
