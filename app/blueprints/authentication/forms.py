from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import EqualTo, DataRequired, Length
from flask_wtf import FlaskForm

class ProfileForm(FlaskForm):
    username = StringField()
    display = StringField(Length(min=1, max=20))
    password = PasswordField()
    confirm_password = PasswordField(EqualTo('password'))
    submit = SubmitField('Submit')

class InfoForm(FlaskForm):
    display = StringField(Length(min=1, max=20))
    team = StringField(Length(min=1, max=1))
    submit = SubmitField('Submit')