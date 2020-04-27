from flask import Flask, url_for, request, render_template

app = Flask(__name__)


@app.route('/index')
def index():
    return render_template('base.html')


@app.route('/couriers')
def couriers():
    return render_template('couriers.html')


@app.route('/about')
def about():
    return render_template('about.html')


@app.route('/contacts')
def contacts():
    return render_template('contacts.html')


@app.route('/contacts?')
def contacts1():
    _name = request.form['Name']
    f = open('text.txt', 'w')
    f.write(_name)


@app.route('/login')
def login():
    return render_template('login.html')


@app.route('/registration')
def registration():
    return render_template('registration.html')


if __name__ == '__main__':
    app.run(port=8080, host='0.0.0.0', debug=True)
