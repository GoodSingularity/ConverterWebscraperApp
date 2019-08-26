from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField
from wtforms.validators import DataRequired
class WebscraperForm(FlaskForm): # i think here it should be Form rather than FlaskForm

    file = StringField('file name', validators=[DataRequired()])
