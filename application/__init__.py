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
    if form.validate_on_submit():
        return "Success BOOm"
    return render_template('index.html', form=form)

