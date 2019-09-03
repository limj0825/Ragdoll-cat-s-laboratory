from flask import Flask, render_template

app = Flask(__name__)

@app.route('/')
def index():
    return 'Welcome To Ragdoll Cat\'s Laboratory, linjia.'

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=80, debug=True)
