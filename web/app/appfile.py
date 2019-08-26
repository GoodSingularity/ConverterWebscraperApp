
from flask import Flask
from flask import jsonify
from src.url_to_json.webscraper import webscraper
from src.json_to_xml.converter import converter

import os
from flask import session
from flask import url_for, redirect, render_template
from flask_wtf import FlaskForm
from flask_wtf.file import FileField
from wtforms import StringField
from werkzeug import secure_filename
from wtforms.validators import url
SECRET_KEY = os.urandom(32)
app = Flask(__name__)
app.config['SECRET_KEY'] = SECRET_KEY


class UploadForm(FlaskForm):
    file = FileField()
    url = StringField(validators=[url()])


@app.route("/", methods=['GET', 'POST'])
def home():
    session['load'] = 0

    form = UploadForm()
    title = "WebscraperJsonXML"
    message="Hello World!"
    if form.validate_on_submit():
        filename = secure_filename(form.file.data.filename)
        url = form.url.data
        print(str(url))
        session['filename'] = filename
        session['url'] = url
        return render_template('webscraper.html', url = url, title=title, message=message)
    return render_template('home.html', form=form, title=title, message=message)

@app.route('/url_to_json')
def url_to_json():
    session['load'] = 0
    data=webscraper(session['url'], session['filename'])
    session['data'] = data
    session['json'] = session['filename'].replace("txt", "json")
    session['xml'] = session['filename'].replace("txt", "xml")
    return data

@app.route("/xmlify", methods=['GET', 'POST'])
def xmlify():
    session['load'] = 0
    title = "WebscraperJsonXML"
    message="Hello World!"
    json = session['json']
    xml = session['xml']
    return render_template('converter.html', json=json, xml=xml, title=title, message=message)


@app.route('/json_to_xml')
def json_to_xml():
    session['load'] = 0
    json = session['json']
    xml = session['xml']
    datatwo=converter(json, xml, "mxb")
    session['datatwo'] = datatwo
    return datatwo
if __name__ == "__main__":
    app.run(host='0.0.0.0')
