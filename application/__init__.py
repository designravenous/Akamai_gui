from flask import Flask, json
from application.config import Akamai_credentials
from urllib.parse import urljoin
from flask import render_template, url_for
from application.forms import TrafficForm, ZoneForm, ResolutionForm
from flask_bootstrap import Bootstrap
import requests
import datetime
from flask_wtf.csrf import CSRFProtect
import re

app = Flask(__name__)
csrf = CSRFProtect(app)
Bootstrap(app)
app.config['SECRET_KEY'] = "Dont_say_a_word"


@app.route('/', methods=['GET', 'POST'])
def index():
    something = " "
    cred = Akamai_credentials(something)
    credentials = cred.Akamai_report()
    zone_credentials = cred.Akamai_zone_read()
    #credentials = Akamai_credentials(something).Akamai_report
    form = TrafficForm(prefix="form")
    form1 = ZoneForm(prefix="form1")
    form2 = ResolutionForm(prefix="form2")
    message = ''
    message2 = '' 
    message3 = ''
    hits_info = []
    zone_outcome = []
    resolution_outcome_www = [] 
    resolution_outcome_bare = []
    if form.validate_on_submit() and form.submit.data:
        if form.start_date.data > form.end_date.data:
            message = "Error! Start date is greater than End date"
        else:
            try:
                domain = str(form.domain_name.data)
                start_day = form.start_date.data
                start = start_day.strftime('%Y%m%d')
                end_day = form.end_date.data
                end = end_day.strftime('%Y%m%d')
                result = credentials[0].get(urljoin(credentials[1],'/data-dns/v1/traffic/'+ str(form.domain_name.data) +'?start=' + start + '&start_time=00:00&end=' + end +'&end_time=23:59'))
                some_text = str(result.text)
                if some_text.__contains__("Zone does not exist"):
                    message = "Zone Does Not Exist"
                else:
                    computer_list = []
                    computer_list.append(some_text)
                    computer_list = [w.replace('\n', ',') for w in computer_list] #List Comprehension
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
                    hits_info = [form.domain_name.data, count_dns, nx_count, form.start_date.data, form.end_date.data]
                    message = 'Success'
            except:
                message = "ERROR occured"
    if form1.validate_on_submit() and form1.submit.data:
        message2 = form1.domain_name.data
        domain = str(form1.domain_name.data)
        try:
            result = zone_credentials[0].get(urljoin(zone_credentials[1],'/config-dns/v1/zones/' + domain))
            stringar = result.text
            if stringar.__contains__("Not Found"):
                message2 = "Zone Not Found"
            else:
                document = json.loads(stringar)
                print(document)
                zone_outcome.append(document['zone']['name'])
                zone_outcome.append(document['zone']['ns'])
                zone_outcome.append(document['zone']['soa'])
                zone_outcome.append(document['zone']['mx'])
                zone_outcome.append(document['zone']['cname'])
                #zone_outcome.extend()
        except:
            message2 = 'error'
    if form2.validate_on_submit() and form2.submit.data:
        message3 = form2.domain_name.data
        domain = str(message3)
        domain_bare_naked = "http://" + domain
        www_domain = "http://www." + domain
        try:
            response_bare_naked = requests.get(domain_bare_naked)
            match_bare_naked = re.search('<title>(.*?)</title>', response_bare_naked.text)
            status_bare_naked = response_bare_naked.status_code
            resolution_bare_naked = response_bare_naked.url 
            resolution_outcome_bare.extend([domain, status_bare_naked, resolution_bare_naked])
        except:
            pass
        try:
            response_domain = requests.get(www_domain)
            status_www = response_domain.status_code
            resolution_www = response_domain.url
            resolution_outcome_www.extend([domain, status_www, resolution_www])
        except:
            pass

    return render_template('index.html', form=form, message=message, message2=message2, message3=message3, form1=form1, hits_info=hits_info, resolution_outcome_bare=resolution_outcome_bare, resolution_outcome_www=resolution_outcome_www, title="DNS", form2=form2)


    

  

