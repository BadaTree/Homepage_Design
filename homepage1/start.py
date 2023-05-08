from flask import Flask, send_from_directory

app = Flask(__name__)

@app.route("/hello") # 127.0.0.1
def hello_world():
    return "<p>Hello, World!</p>"

@app.route("/pro") #127.0.0.1
def index1():
    return send_from_directory('html_professos', 'index.html') # 127.0.0.1/html/css/b.css

@app.route('/pro<path:name>') #127.0.0.1/css/b.css
def start1(name):
    return send_from_directory('html_professor',name) # 127.0.0.1/html/css/b.css"

@app.route("/") #127.0.0.1
def index():
    return send_from_directory('./main/html', 'index.html') # 127.0.0.1/html/index.html

@app.route('/<path:name>') #127.0.0.1/css/b.css
def start(name):
    return send_from_directory('.main/html',name) # 127.0.0.1/html/css/b.css