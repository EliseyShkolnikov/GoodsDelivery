from flask import Flask, url_for, request, render_template
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///vk_bot-master/Goods.db'
db = SQLAlchemy(app)

class Task(db.Model):
    ID = db.Column(db.Integer, primary_key=True)
    Name = db.Column(db.String())
    Address = db.Column(db.String())
    Goods = db.Column(db.String())
    Period = db.Column(db.String())
    Coment = db.Column(db.String())
    Photo = db.Column(db.String())
	
@app.route('/index')
def index():
	tasks = Task.query.all()
    return render_template('base.html', tasks = tasks)

@app.route('/about')
def about():
    return render_template('about.html')


@app.route('/contacts')
def contacts():
    return render_template('contacts.html')


@app.route('/couriers', methods=['GET', 'POST'])
def contacts1():
    return render_template('couriers.html')


@app.route('/login')
def login():
    return render_template('login.html')


@app.route('/registration')
def registration():
    return render_template('registration.html')


if __name__ == '__main__':
    app.run(port=8080, host='0.0.0.0', debug=True)
