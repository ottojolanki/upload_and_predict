from flask import Flask, redirect, render_template, url_for
from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileRequired, FileAllowed
import requests

app = Flask(__name__)

# no uploads over 16MB
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024
app.config['SECRET_KEY'] = 'much secret, wow'

KERAS_API_URL = 'http://127.0.0.1:8000/predict'


class UploadForm(FlaskForm):
    file = FileField('image', validators=[
        FileRequired(),
        FileAllowed(['jpg', 'jpeg', 'png'], 'Images only!')])


@app.route('/upload', methods=['GET', 'POST'])
def upload():
    form = UploadForm()
    if form.validate_on_submit():
        imagedata = form.file.data.read()
        payload = {"image" : imagedata}
        print(type(imagedata))
        result = requests.post(KERAS_API_URL, files=payload).json()
        if result["success"]:
            return result["predictions"][0]["label"]
        else:
            return 'FAIL'
    return render_template('upload.html', form=form)
