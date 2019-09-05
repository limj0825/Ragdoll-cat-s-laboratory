from flask import Flask, render_template
import pymongo
from pymongo import MongoClient
'''from config import db_config, app_config

db = MongoClient(host=db_config['host'], port=db_config['port'])[
    db_config['db_name']
]'''
app = Flask(__name__)
#app.config['SECRET_KEY'] = app_config['secret_key']


@app.route('/')
def index():
    mystr = 'mr.lee'
    dicts = {'tp': 123}
    return render_template('index.html', mystr=mystr, dicts=dicts)


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=80, debug=True)
