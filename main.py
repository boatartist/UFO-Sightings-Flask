import random, string
from flask import Flask, render_template, request, redirect, url_for
from ufo_db import *
import sqlite3
from process import *
import datetime
import add_entry
#column headings for sql database
headers = {
  'date_time': 'text',
  'city_area': 'text',
  'state': 'text',
  'country': 'text',
  'ufo_shape': 'text',
  'encounter_length': 'int',
  'described_encounter_length': 'text',
  'description': 'text',
  'date_documented': 'text',
  'latitude': 'float',
  'longitude': 'text'
}
#dictionary of recognised countries
countries = {
  'AE': 'united arab emirates',
  'AF': 'afghanistan',
  'AL': 'albania',
  'DZ': 'algeria',
  'AR': 'argentina',
  'AM': 'armenia',
  'AU': 'australia',
  'AT': 'austria',
  'BD': 'bangladesh',
  'BB': 'barbados',
  'BY': 'belarus',
  'BE': 'belgium',
  'BM': 'bermuda',
  'BO': 'bolivia',
  'BW': 'botswana',
  'BR': 'brazil',
  'BG': 'bulgaria',
  'KH': 'cambodia',
  'CM': 'cameroon',
  'CA': 'canada',
  'CL': 'chile',
  'CN': 'china',
  'CO': 'colombia',
  'CR': 'costa rica',
  'HR': 'croatia',
  'CU': 'cuba',
  'CZ': 'czech republic',
  'DK': 'denmark',
  'EC': 'ecuador',
  'EG': 'egypt',
  'ET': 'ethiopia',
  'FJ': 'fiji',
  'FI': 'finland',
  'FR': 'france',
  'DE': 'germany',
  'GR': 'greece',
  'GL': 'greenland',
  'GT': 'guatemala',
  'HK': 'hong kong',
  'HU': 'hungary',
  'IS': 'iceland',
  'IN': 'india',
  'ID': 'indonesia',
  'IR': 'iran',
  'IE': 'ireland',
  'IL': 'israel',
  'IT': 'italy',
  'JM': 'jamaica',
  'JP': 'japan',
  'JO': 'jordan',
  'KE': 'kenya',
  'KR': 'south korea',
  'LB': 'lebanon',
  'LR': 'liberia',
  'LY': 'libya',
  'LT': 'lithuania',
  'MG': 'madagascar',
  'MY': 'malaysia',
  'MX': 'mexico',
  'MN': 'mongolia',
  'MA': 'morocco',
  'NP': 'nepal',
  'NL': 'netherlands',
  'NC': 'new caledonia',
  'NZ': 'new zealand',
  'NG': 'nigeria',
  'NO': 'norway',
  'PK': 'pakistan',
  'PG': 'papua new guinea',
  'PE': 'peru',
  'PH': 'philippines',
  'PL': 'poland',
  'PT': 'portugal',
  'QA': 'qatar',
  'RO': 'romania',
  'RU': 'russia',
  'SA': 'saudi arabia',
  'RS': 'serbia',
  'SG': 'singapore',
  'ZA': 'south africa',
  'ES': 'spain',
  'LK': 'sri lanka',
  'SE': 'sweden',
  'CH': 'switzerland',
  'TW': 'taiwan',
  'TH': 'thailand',
  'TR': 'turkey',
  'UA': 'ukraine',
  'AE': 'united arab emirates',
  'GB': 'united kingdom',
  'US': 'united states',
  'VN': 'vietnam',
  'ZW': 'zimbabwe',
  'NA': 'unknown'
}

cities = [
  'tokyo (japan)',
  'delhi (india)',
  'shanghai (china)',
  'sao paulo (brazil)',
  'mexico city (mexico)',
  'cairo (egypt)',
  'dhaka (bangladesh)',
  'mumbai (india)',
  'beijing (china)',
  'osaka (japan)',
  'new york (united states)',
  'karachi (pakistan)',
  'buenos aires (argentina)',
  'istanbul (turkey)',
  'kolkata (india)',
  'manila (philippines)',
  'lagos (nigeria)',
  'rio de janeiro (brazil)',
  'tianjin (china)',
  'los angeles (united states)',
  'moscow (russia)',
  'shenzhen (china)',
  'lahore (pakistan)',
  'bangalore (pakistan)',
  'paris (france)',
  'bogota (colombia)',
  'jakarta (indonesia)',
  'chennai (india)',
  'lima (peru)',
  'bangkok (thailand)',
  'seoul (south korea)',
  'nagoya (japan)',
  'hyderabad (india)',
  'london (united kingdom)',
  'tehran (iran)',
  'chicago (united states)',
  'ho chi minh (vietnam)',
  'kuala lumpur (malaysia)',
  'hong kong (china)',
  'baghdad (iraq)',
  'madrid (spain)',
  'houston (united states)',
  'dallas (united states)',
  'toronto (canada)',
  'miami (united states)',
  'singapore (singapore)',
  'philadelphia (united states)',
  'atlanta (united states)',
  'barcelona (spain)',
  'washington (united states)',
  'alexandria (egypt)',
  'melboune (australia)',
  'sydney (australia)',
  'cape town (south africa)',
  'rome (italy)',
  'montreal (canada)',
  'dakar (senegal)',
  'kuwait (kuwait)',
  'milan (italy)',
  'athens (greece)',
  'dubai (united arab emirates)',
  'lisbon (portugal)',
  'manchester (united kingdom)',
  'damascus (syria)',
  'brisbane (australia)',
  'phnom penh (cambodia)',
  'perth (australia)',
  'panama city (panama)',
  'vienna (austria)',
  'warsaw (poland)',
  'hamburg (germany)',
  'budapest (hungary',
  'bucharest (romania)',
  'stockholm (sweden)',
  'glasgow (united kingdom)',
  'auckland (new zealand)',
  'phoenix (united states)',
  'marseille (france)',
  'munich (germany)',
  'kathmandu (nepal)',
  'abu dhabi (united arab emirates)',
  'philadelphia (united states)',
  'copenhagen (denmark)',
  'adelaide (australia)',
  'helsinki (finland)',
  'prague (czech republic)',
  'dublin (ireland)',
  'islamabad (pakistan)',
  'amsterdam (netherlands)',
  'oslo (norway)',
  'jerusalem (israel)',
  'nice (france)',
  'liverpool (united kingdom)'
]
cities_new = []
cities_dict = {}
for city in cities:
  city_n = city[:-1]
  city_n = city_n.split(' (')
  city_n = city_n[0]
  cities_new.append(city_n)
  cities_dict[city_n] = city

print(cities_dict)
#making list out of dictionary
countrys = []
for code, name in countries.items():
  countrys.append([code, name])
  
#converting csv file to database. This is slightly unneccessary, but prevents errors due to accidental file corruption
make_db('ufo.db', 'ufo_sightings1.csv', 'ufo_sightings', headers, countries)


app = Flask(  # Create a flask app
  __name__,
  template_folder='templates',  # Name of html file folder
  static_folder='static'  # Name of directory for static files
)
#home page, rendered from template
@app.route('/')
def home():
  return render_template('home.html', static_url_path='/static')
  
#page for recording sightings
@app.route('/enter', methods = ['GET', 'POST'])
def enter():
  #when the form on the webpage is submitted
  if request.method == 'POST':
    print('new sighting recorded')
    #date in yyyy-mm-dd format
    date = request.form.get('date')
    #convert date
    date = date.split('-')
    date = f'{date[2]}/{date[1]}/{date[0]}'
    #24 hour time hh:mm
    time = request.form.get('time')
    #date & time
    date_time = f'{date} {time}'
    #city name
    city = request.form.get('city').lower()
    #state, ideally acronym
    state = request.form.get('state').upper()
    #country 2 letter code
    country = request.form.get('country').upper()
    #shape
    shape = request.form.get('shape')
    #number of seconds
    encounter_length = request.form.get('encounter_length')
    #description of length (ie. '5 hours 2 minutes')
    described_encounter_length = request.form.get('described_encounter_length')
    #description, crop to max 30 words
    description = request.form.get('description')
    description = description.split()
    if len(description) > 30:
      description = description[:30]
    description = ' '.join(description)
    #latitude and longitude in as many digits as desired 
    latitude = float(request.form.get('latitude'))
    longitude = float(request.form.get('longitude'))
    #get date documented
    date_documented = datetime.date.today()
    #dates in csv file are recorded mm/dd/yyyy, so converting to that format
    date_documented = date_documented.strftime("%m/%d/%Y")
    
    #date_int from mm/dd/yyyy format
    date = date_time.split(' ')
    date = date[0].split('/')
    days = int(date[1])
    months = int(date[0])*100
    years = int(date[2])*10000
    date_int = days + months + years
    #adding entry to database
    add_entry.add_entry(date_time, city, state, country, shape, encounter_length, described_encounter_length, description, date_documented, latitude, longitude, date_int)
    #redirecting to main page
    return redirect(url_for('home'))
    
  else:
    #render page
    return render_template('entry.html', static_url_path='/static', countries = countrys, cities=cities)

#"map" page for viewing sightings
@app.route('/map', methods = ["GET", "POST"])
def map():
  #the default state for all variables
  filters = 0
  country = ''
  date = ''
  duration = None
  city = ''
  date_type = ''
  proper_date = ''
  time = None
  #if 'submit' button pressed
  if request.method == 'POST':
    print('new request')
    #get country code, which != country name
    countr = request.form.get('countryCheck')
    if countr == 'on':
      country = request.form.get('country')
      filters += 1
    #get city description. This can be any length, but is always lowercase
    cit = request.form.get('cityCheck')
    if cit == 'on':
      city = request.form.get('city').lower()
      filters += 1
    #get date and convert to dd/mm/yyyy format 
    dat = request.form.get('dateCheck')
    if dat == 'on':
      date_type = request.form.get('date_type')
      date = request.form.get('firstdate')
      print(date)
      date = date.split('-')
      proper_date = f'{date_type} {date[2]}/{date[1]}/{date[0]}'
      days = int(date[2])
      months = int(date[1])*100
      years = int(date[0])*10000
      date = days + months + years
      if date_type == 'between':
        second = request.form.get('seconddate')
        second = second.split('-')
        proper_date = proper_date + f' and {second[2]}/{second[1]}/{second[0]}'
        days = int(second[2])
        months = int(second[1])*100
        years = int(second[0])*10000
        second = days + months + years
        date = [date, second]
      else:
        date = [date]
      print(date)
      filters += 1
    #get maximum duration of sighting
    #too lazy to improve this filter
    dur = request.form.get('durationCheck')
    if dur == 'on':
      duratio = request.form.get('duration')
      if duratio:
        duration = duratio
        filters += 1
    #get exact time of event
    tim = request.form.get('timeCheck')
    if tim == 'on':
      time = request.form.get('firsttime')
      print(time)
      filters += 1
  #as long as there is at least 1 filter, then process the data
  if filters >= 1:
    new_rows, names = process(country, date, duration, city, date_type, proper_date, time, countries)
  #if there aren't any filters, set it to default
  else:
    if not country:
      country = 'AU'
    if not date:
      date = ''
      date_type = ''
    if not duration:
      duration=None
    if not city:
      city = 'sydney'
    new_rows, names = process(country, date, duration, city, date_type, proper_date, time, countries)
  print(country, date, duration, city)
  print(filters)
  #reload the webpage with new data
  return render_template('map.html',
                         static_url_path='/static',
                         data=new_rows, names=names, cities=cities_dict)

if __name__ == "__main__":  # Makes sure this is the main process
  app.run(  # Starts the site
    host='0.0.0.0',  # EStablishes the host, required for repl to detect the site
    port=random.randint(2000,
                        9000)  # Randomly select the port the machine hosts on.
  )
