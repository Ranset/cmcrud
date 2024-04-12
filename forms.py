
from flask_wtf import FlaskForm
from wtforms.fields import StringField, PasswordField
from wtforms.validators import InputRequired, EqualTo

# Aqu'i empieza sec11

class RegisterForm(FlaskForm):
    name = StringField('Nombre', validators=[InputRequired()])
    username = StringField('Usuario', validators=[InputRequired()])
    email = StringField('Email', validators=[InputRequired()])
    password = PasswordField('Password', validators=[InputRequired(), EqualTo('confirm')])
    confirm = PasswordField('Confirmar', validators=[InputRequired()])


# Aqu'i empieza sec12

class LoginForm(FlaskForm):
    
    username = StringField('Usuario', validators=[InputRequired()])
    password = PasswordField('Password', validators=[InputRequired()])