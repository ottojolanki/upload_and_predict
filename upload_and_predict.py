from flask import Flask, render_template

app = Flask(__name__)


@app.route('/')
def index():
    return render_template('hello.html')


@app.route('/person/<name>')
def hi_you(name):
    return render_template('hello_person.html', person=name)
