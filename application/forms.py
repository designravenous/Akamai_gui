from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired
from wtforms.fields.html5 import DateField

class TrafficForm(FlaskForm):
    domain_name = StringField('Domain', validators=[DataRequired()], render_kw={'class':'text-center'})
    start_date = DateField('Start date:', format='%Y-%m-%d',validators=[DataRequired()], render_kw={'class':'text-center'}) 
    end_date = DateField('End date:', format='%Y-%m-%d', validators=[DataRequired()], render_kw={'class':'text-center'})
    submit = SubmitField('Get Hits', render_kw={'class':'btn btn-primary'})

class ZoneForm(FlaskForm):
    domain_name = StringField('Domain', validators=[DataRequired()])
    submit = SubmitField('Get Zone',render_kw={'class':'btn btn-primary'})