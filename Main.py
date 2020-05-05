from flask import Flask, render_template, url_for, request, redirect
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///vk_bot-master/Goods.db'
db = SQLAlchemy(app)

class GG(db.Model):
    ID = db.Column(db.Integer, primary_key=True)
    Name = db.Column(db.String(200))
    Address = db.Column(db.String())
    Goods = db.Column(db.String())
    Period = db.Column(db.String())
    Coment = db.Column(db.String())
    Photo = db.Column(db.String())

	

@app.route('/index')
def index():
    tasks = GG.query.all()
    return render_template('base.html', tasks = tasks)


@app.route('/about')
def about():
    return render_template('about.html')


@app.route('/contacts')
def contacts():
    return render_template('contacts.html')


@app.route('/couriers')
def contacts1():
    return render_template('couriers.html')


@app.route('/login')
def login():
    return render_template('login.html')


@app.route('/registration')
def registration():
    return render_template('registration.html')


@app.route('/delete/<ID>')
def delete(ID):
    GG.query.filter_by(ID=int(ID)).delete()
    db.session.commit()
    return redirect(url_for('index'))


@app.route('/create-task', methods=['POST'])
def create():
    new_task1 = GG(Name=request.form['name'])
    new_task2 = GG(Address=request.form['address'])
    new_task3 = GG(Goods=request.form['goods'])
    new_task4 = GG(Period=request.form['period'])
    new_task5 = GG(Coment=request.form['coment'])
    new_task6 = GG(Photo=request.form['photo'])
    db.session.add(new_task1)
    db.session.add(new_task2)
    db.session.add(new_task3)
    db.session.add(new_task4)
    db.session.add(new_task5)
    db.session.add(new_task6)
    db.session.commit()
    return redirect(url_for('contacts1'))


if __name__ == '__main__':
    app.run(port=8080, host='0.0.0.0', debug=True)
