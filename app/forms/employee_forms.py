from flask_wtf import FlaskForm
from wtforms import StringField, IntegerField

class EmployeeForm(FlaskForm):
    name = StringField('Name')
    age = IntegerField('Age')
    department = StringField('Department')

class LoginForm(FlaskForm):
    username = StringField('Username')
    password = StringField('Password')

class RegistrationForm(FlaskForm):
    username = StringField('Username')
    password = StringField('Password')