from flask_wtf import FlaskForm
from wtforms import StringField, IntegerField

class EmployeeForm(FlaskForm):
    name = StringField('Name')
    age = IntegerField('Age')
    department = StringField('Department')