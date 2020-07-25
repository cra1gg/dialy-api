import phonenumbers
from phonenumbers import carrier
import flask
import json
from phonenumbers import geocoder
app = flask.Flask(__name__)
app.config["DEBUG"] = True


app = Flask('')
app._static_folder = "templates/static/"
CORS(app)

def run():
    app.run(host='0.0.0.0',port=8080)

@app.route('/')
def home():
    return render_template("index.html")

@app.route('/lookup/<phonenum>', methods=['GET'])
def lookup(phonenum):
    returndict = {}
    phoneobj = phonenumbers.parse(phonenum)
    returndict['valid'] = phonenumbers.is_valid_number(phoneobj)
    returndict['local_format'] = phonenumbers.format_in_original_format(phoneobj, 'local')
    returndict['intl_format'] = phonenumbers.format_out_of_country_keeping_alpha_chars(phoneobj, 'world')
    returndict['carrier'] = carrier.name_for_number(phoneobj, "en")
    returndict['country_code'] = geocoder.region_code_for_number(phoneobj)
    returndict['country_name'] = geocoder.country_name_for_number(phoneobj, "en")
    returndict['location'] = geocoder.description_for_number(phoneobj, "en")
    returndict['line_type'] = get_type(phonenumbers.number_type(phoneobj))
    return json.dumps(returndict)

def get_type(numtype):
    if numtype == 0:
        return "Landline"
    elif numtype == 1:
        return "Mobile Phone"
    elif numtype == 2:
        return "Landline or Mobile Phone"
    elif numtype == 3:
        return "Toll Free Number"
    elif numtype == 6:
        return "VOIP"
    elif numtype == 7:
        return "Personal Number"
    elif numtype == 8:
        return "Pager"
    elif numtype == 10:
        return "Voicemail"
    else:
        return "Unknown"

def keep_alive():  
    t = Thread(target=run)
    t.start()
