from flask import Flask, render_template, request
from flask_bootstrap import Bootstrap


app = Flask(__name__, static_folder='static')
bootstrap = Bootstrap(app)


@app.route('/')
def main():
    return render_template('/index_main.html')

@app.route('/research')
def ResearchArea():
    return render_template('/ResearchArea_.html')

@app.route('/project')
def Projects():
    return render_template('/project.html')

@app.route('/professor')
def Professor():
    return render_template('/Professor_.html')

@app.route('/members')
def CurrentMembers():
    return render_template('/team.html')

@app.route('/alumni')
def Alumni():
    return render_template('/Alumni.html')

@app.route('/journal')
def Journals():
    return render_template('/journal.html')

@app.route('/conference')
def Conferences():
    return render_template('/conference.html')

@app.route('/patent')
def Patent():
    return render_template('/patent.html')

@app.route('/undergraduate')
def Undergradute():
    return render_template('/undergraduate.html')

@app.route('/undergraduate/KECE207')
def Undergradute_KECE207():
    return render_template('/undergraduates/KECE207.html')

@app.route('/undergraduate/KECE340')
def Undergradute_KECE340():
    return render_template('/undergraduates/KECE340.html')

@app.route('/undergraduate/KECE343')
def Undergradute_KECE343():
    return render_template('/undergraduates/KECE343.html')

@app.route('/graduate')
def Gradute():
    return render_template('/graduate.html')

@app.route('/graduate/ECE656')
def Gradute_ECE656():
    return render_template('/graduates/ECE656.html')

@app.route('/graduate/ECE519')
def Gradute_ECE519():
    return render_template('/graduates/ECE519.html')

@app.route('/notice')
def Notice():
    return render_template('/index_main copy.html')

@app.route('/news')
def News():
    return render_template('/team.html')

@app.route('/project_1')
def Current1():
    return render_template('/pj_1.html')

@app.route('/project_2')
def Current2():
    return render_template('/pj_2.html')

@app.route('/project_3')
def Current3():
    return render_template('/pj_3.html')

@app.route('/project_4')
def Current4():
    return render_template('/pj_4.html')

@app.route('/project_5')
def Current5():
    return render_template('/pj_5.html')

@app.route('/project_6')
def Current6():
    return render_template('/pj_6.html')

@app.route('/news1')
def news1():
    return render_template('/news1.html')

if __name__ == '__main__':
    app.run(host="0.0.0.0", port=8080, debug=False)

