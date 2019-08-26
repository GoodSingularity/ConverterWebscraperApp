from flask import Flask, request
from flask import jsonify
from src.url_to_json.webscraper import webscraper
from src.json_to_xml.converter import converter

import os
from flask import session
from flask import url_for, redirect, render_template
from flask_wtf import FlaskForm,RecaptchaField
from flask_wtf.file import FileField,FileAllowed,FileRequired
from wtforms import StringField, validators,SelectField
from werkzeug import secure_filename
from wtforms.validators import url, InputRequired
from flask_session import Session
from datetime import timedelta

SECRET_KEY = os.urandom(32)
app = Flask(__name__, static_url_path='/static')
app.config['SECRET_KEY'] = SECRET_KEY
app.config['SESSION_TYPE'] = 'filesystem'
app.config['SESSION_PERMANENT'] = True
app.config['SESSION_TYPE'] = 'filesystem'
app.config['PERMANENT_SESSION_LIFETIME'] = timedelta(hours=5)
CONVERTER = './src/json_to_xml'
WEBSCRAPER = './src/url_to_json'
app.config['CONVERTER'] = CONVERTER
app.config['WEBSCRAPER'] = WEBSCRAPER
app.config['RECAPTCHA_USE_SSL'] = False
app.config['RECAPTCHA_PUBLIC_KEY'] = '6LfG57QUAAAAAHF777ozpvNrT0qExdmndXNDsNLj'
app.config['RECAPTCHA_PRIVATE_KEY'] = '6LfG57QUAAAAADabD61-DOnExVFaKjLZgSn6KXpX'
app.config['RECAPTCHA_OPTIONS'] = {'theme': 'white'}

def split(s):
    half, rem = divmod(len(s), 2)
    return s[:half + rem], s[half + rem:]
class WebscraperForm(FlaskForm):
    regexpr = StringField('Regular reg_expr',validators=[InputRequired(),validators.Length(min=1, max=100)])
    url = StringField(validators=[url(), InputRequired(),validators.Length(min=8)])
    recaptcha = RecaptchaField()

class ConverterForm(FlaskForm):
    file = FileField('json file', validators=[
        FileRequired(),
        FileAllowed(['json', 'Json'], 'Json only!')
    ])
    vr = SelectField(u'Xml version', choices=[('mxb', "mxb"), ('mx3','mx3'), ('mx4', 'mx4')])
    recaptcha = RecaptchaField()

@app.route("/", methods=['GET', 'POST'])
def index():
    session['load'] = 0

    formwebscraper = WebscraperForm()
    formconverter = ConverterForm()

    title = "WebscraperJsonXML"
    message="Hello World!"
    if formwebscraper.validate_on_submit():
        #converterfile = secure_filename(formconverter.file.data.filename)
        url = formwebscraper.url.data
        regexpr = formwebscraper.regexpr.data
        session['regexpr'] = regexpr
        session['url'] = url
        return render_template('webscraper.html',title=title, message=message)
    elif formconverter.validate_on_submit():
        converterfile = secure_filename(formconverter.file.data.filename)
        #converterfile = secure_filename(formconverter.file.data.filename)
        session['filename'] = converterfile
        session['jsonify'] = session['filename'].split(".")[0]+".json"
        session['xmlify'] = session['filename'].split(".")[0]+".xml"
        session['filename'] = converterfile
        formconverter.file.data.save("/app/src/json_to_xml/"+str(session['jsonify']))
        session['version']=formconverter.vr.data
        return render_template('converter.html',title=title, message=message)
    return render_template('index.html', formconverter=formconverter, formwebscraper=formwebscraper, title=title, message=message)


@app.route('/url_to_json')
def url_to_json():
    session['load'] = 0
    url = session['url']
    reg = session['regexpr']
    data=webscraper(url, reg)
    return data

@app.route('/json_to_xml')
def json_to_xml():
    session['load'] = 0
    json = session['jsonify']
    xml = session['xmlify']
    ver = session['version']

    data=converter(json, xml, ver)
    return data
if __name__ == "__main__":
    app.run(host='0.0.0.0')

"""
previous version of website
@app.route("/", methods=['GET', 'POST'])
def home():
    session['load'] = 0

    formwebscraper = WebscraperForm()
    formconverter = ConverterForm()

    title = "WebscraperJsonXML"
    message="Hello World!"

    if formwebscraper.validate_on_submit():
        #converterfile = secure_filename(formconverter.file.data.filename)
        url = formwebscraper.url.data
        regexpr = formwebscraper.regexpr.data
        session['regexpr'] = regexpr
        session['url'] = url
        return render_template('webscraper.html',title=title, message=message)
    elif formconverter.validate_on_submit():
        converterfile = secure_filename(formconverter.file.data.filename)
        #converterfile = secure_filename(formconverter.file.data.filename)
        session['filename'] = converterfile
        session['jsonify'] = session['filename'].split(".")[0]+".json"
        session['xmlify'] = session['filename'].split(".")[0]+".xml"
        session['filename'] = converterfile
        formconverter.file.data.save("/app/src/json_to_xml/"+str(session['jsonify']))
        session['version']=formconverter.vr.data
        return render_template('converter.html',title=title, message=message)

    return render_template('home.html', formconverter=formconverter, formwebscraper=formwebscraper, title=title, message=message)
"""
