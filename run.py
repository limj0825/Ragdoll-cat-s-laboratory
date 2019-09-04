from flask import Flask, render_template

app = Flask(__name__)


@app.route('/')
def index():
    mystr = 'mr.lee'
    dicts = {'tp': 123}
    return render_template('base.html', mystr=mystr, dicts=dicts)


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=80, debug=True)
