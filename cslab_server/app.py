from flask import Flask, render_template
from flask_bootstrap import Bootstrap

app = Flask(__name__, static_folder='static')
bootstrap = Bootstrap(app)

@app.route('/')
def main():
    return render_template('/index.html')

@app.route('/research')
def ResearchArea():
    return render_template('/ResearchArea.html')

@app.route('/project')
def Projects():
    return render_template('/index_copy.html')

@app.route('/professor')
def Professor():
    return render_template('/Professor.html')

@app.route('/members')
def CurrentMembers():
    return render_template('/member.html')

@app.route('/alumni')
def Alumni():
    return render_template('/index_copy.html')

@app.route('/journal')
def Journals():
    return render_template('/index_copy.html')

@app.route('/conference')
def Conferences():
    return render_template('/index_copy.html')

@app.route('/patent')
def Patent():
    return render_template('/index_copy.html')

@app.route('/undergradute')
def Undergradute():
    return render_template('/index_copy.html')

@app.route('/gradute')
def Gradute():
    return render_template('/index_copy.html')

@app.route('/notice')
def Notice():
    return render_template('/index_copy.html')

@app.route('/news')
def News():
    return render_template('/index_copy.html')

if __name__ == '__main__':
    app.run(port=800)
