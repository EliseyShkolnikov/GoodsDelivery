from flask import Flask, url_for, request, render_template

app = Flask(__name__)


@app.route('/')
def index():
    return render_template('base.html')
@app.route('/contacts')
def contacts():
    return render_template('contacts.html')


if __name__ == '__main__':
    app.run(port=8080, host='127.0.0.1')
