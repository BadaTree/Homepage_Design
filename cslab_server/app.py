from flask import Flask, render_template
from flask_bootstrap import Bootstrap

app = Flask(__name__, static_folder='static')
bootstrap = Bootstrap(app)

@app.route('/')
def index():
    return render_template('/index_temp.html')

# @app.route('./home')
# def index1():
#     return render_template('/index.html')

if __name__ == '__main__':
    app.run(debug=True, port=8038, host='0.0.0.0')
