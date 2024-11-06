import sqlite3

#function for processing inputted data and outputting all values
def process(country, date, duration, city, date_type, proper_date, time, countries):
  print(country)
  names = []
  for code, name in countries.items():
    names.append([code, name])
  city = city.lower()
  #connect to sqlite3
  connection = sqlite3.connect('ufo.db')
  cursor = connection.cursor()
  where = ''
  conditions = []
  descriptors = []
  #add WHERE statement as long as there are filters
  if country or date or duration or city or time:
    where = 'WHERE '
  #add SQL conditions for every filter
  if city:
    conditions.append(f'city_area LIKE "%{city}%" ')
    city = f'in {city}'
    descriptors.append(city)
  if country:
    conditions.append(f'country = "{country}" ')
    if country in countries.keys():
      country = countries[country]
    country = f'in {country}'
    descriptors.append(country)
  if date != '':
    descriptors.append(proper_date)
    print('date found')
    #different date specifications. based on date_int, which is a number of format yyyymmdd that allows for mathematical 
    if date_type == 'on':
      conditions.append(f'date_int = {date[0]} ')
    if date_type == 'between':
      conditions.append(f'{date[1]} > date_int ')
      conditions.append(f'date_int > {date[0]} ')
    if date_type == 'until':
      conditions.append(f'{date[0]} > date_int ')
    if date_type == 'after':
      conditions.append(f'{date[0]} < date_int ')
  if duration:
    conditions.append(f'encounter_length <= {duration} ')
    duration = f'lasting {duration}'
    descriptors.append(duration)
  if time:
    conditions.append(f'date_time LIKE "%{time}" ')
    time = f'at {time}'
    descriptors.append(time)
  #SQL command, with conditions included. Top 200 entries only
  command = (
    f"SELECT latitude, longitude, date_time, country, description, ufo_shape, encounter_length, city_area, date_int FROM ufo_sightings {where}{(' AND '.join(conditions))}ORDER BY country, date_time LIMIT 200"
  )
  print(command)
  cursor.execute(command)
  
  description = ' '.join(descriptors)
  #retrieving all outputted data as a list of lists, with every item being one of these lists
  rows = cursor.fetchall()
  new_rows = []
  #custom icon names and centre points
  images = {
    'light': [15, 15],
    'disk': [15, 30],
    'circle': [15, 15],
    'cigar': [10, 30],
    'triangle': [15, 30],
    'teardrop': [15, 0]
  }
  for row in rows:
    #converting encounter_length (int) to hh:mm:ss format. This is used instead of the described_encounter_length, as it is more reliable than the human data
    try:
      seconds = int(row[6])
      hours = int(seconds / 3600)
      minutes = int((seconds % 3600) / 60)
      seconds = seconds - (minutes * 60) - (hours * 3600)
      length = ("%02d:%02d:%02d" % (hours, minutes, seconds))
    except:
      length = "N/A"
    #combining all the retrieved data into a list to be given to the html file, including the new icon names
    if row[5].lower() in images.keys():
      new_row = row[:5] + (f'{row[5].lower()}.png', (images[row[5].lower()]),
                           (row[5].lower()), length, row[7], row[8])
    else:
      new_row = row[:5] + ('alien.png', [15, 30], row[5], length, row[7], row[8])
    new_rows.append(new_row)
  new_rows.append(description)
  #this is what is returned
  return new_rows, names