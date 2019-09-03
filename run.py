from flask import Flask, render_template

app = Flask(__name__)


@app.route('/')
def index():
    mystr = 'mr.lee'
    return render_template('base.html', mystr=mystr)


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=80, debug=True)
