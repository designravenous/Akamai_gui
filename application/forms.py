from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired
from wtforms.fields.html5 import DateField

class TrafficForm(FlaskForm):
    start_date = DateField('Start date:', format='%Y-%m-%d') 
    submit = SubmitField('Go!', render_kw={'class':'btn btn-primary'})