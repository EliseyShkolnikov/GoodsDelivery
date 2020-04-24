from flask import Flask, url_for, request, render_template

app = Flask(__name__)


@app.route('/index')
def index():
    return render_template('base.html')
@app.route('/contacts')
def contacts():
    return render_template('goods.html')
@app.route('/goods')
def contacts():
    return render_template('couriers.html')
@app.route('/couriers')
def contacts():
    return render_template('about.html')
@app.route('/about')
def contacts():
    return render_template('contacts.html')


if __name__ == '__main__':
    app.run(port=8080, host='0.0.0.0', debug=True)
