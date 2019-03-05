from flask import Flask
from application.config import Akamai_credentials
from urllib.parse import urljoin
from flask import render_template
from application.forms import TrafficForm, ZoneForm
from flask_bootstrap import Bootstrap
import requests
import datetime
from flask_wtf.csrf import CSRFProtect

app = Flask(__name__)
csrf = CSRFProtect(app)
Bootstrap(app)
app.config['SECRET_KEY'] = "Dont_say_a_word"

@app.route('/', methods=['GET', 'POST'])
def index():
    something = " "
    cred = Akamai_credentials(something)
    credentials = cred.Akamai_report()
    #credentials = Akamai_credentials(something).Akamai_report
    form = TrafficForm()
    message = ''
    if form.validate_on_submit():
        if form.start_date.data > form.end_date.data:
            message = "Error! Start date is greater than End date"
        else:
            try:
                domain = str(form.domain_name.data)
                start_day = form.start_date.data
                start = start_day.strftime('%Y%m%d')
                end_day = form.end_date.data
                end = end_day.strftime('%Y%m%d')
                print(credentials[1])
                result = credentials[0].get(urljoin(credentials[1],'/data-dns/v1/traffic/'+ str(form.domain_name.data) +'?start=' + start + '&start_time=00:00&end=' + end +'&end_time=23:59'))
                some_text = str(result.text)
                computer_list = []
                computer_list.append(some_text)
                computer_list = [w.replace('\n', ',') for w in computer_list] #List Comprehensions
                outcome = computer_list[0].split(',')
                for i in range(5):
                    outcome.pop(0)
                count_dns = 0
                nx_count = 0
                for hit in outcome[::3]:
                    count_dns += int(hit)
                for hit in outcome[1::3]:
                    nx_count += int(hit)
                message = "Domain: %s DNS Hits: %d NX Hits:%d Timestamp: %s -> %s" % (form.domain_name.data.upper(),count_dns,nx_count, form.start_date.data,form.end_date.data)
            except:
                message = "ERROR occured"
    return render_template('index.html', form=form, message=message)

  

