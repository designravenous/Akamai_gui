from flask import Flask
from flask import render_template
from application.forms import TrafficForm
from flask_bootstrap import Bootstrap

app = Flask(__name__)
Bootstrap(app)
app.config['SECRET_KEY'] = "Dont_say_a_word"

@app.route('/', methods=['GET', 'POST'])
def index():
    form = TrafficForm()
    message = ''
    if form.validate_on_submit():
        if form.start_date.data > form.end_date.data:
            message = "Error! Start date is greater than End date"
        else:
            message ="You entered domain:{}, start: {}, end:{}".format(form.domain_name.data,form.start_date.data, form.end_date.data)
    return render_template('index.html', form=form, message=message)

