import csv
import sqlite3

#function to convert csv file to database
def make_db(new_name, old_name, tablename, headings, countries):
  headers = []
  headings_n = {}
  #some heading names are not SQl compatible
  for name, type in headings.items():
    name = name.replace(' ','_')
    name = name.replace(',','_')
    name = name.replace('.','_')
    print(name)
    headers.append(f'{name} {type}')
    headings_n[name]=type
  #the 'date_int' column isn't in the original database, so it's added at the end
  headings_n['date_int']='int'
  headers.append(f'date_int int')
  headings = headings_n
  #making the table
  connection = sqlite3.connect(new_name)
  cursor = connection.cursor()
  cursor.execute(f'DROP TABLE IF EXISTS {tablename}')
  joined = ', '.join(headers)
  print(joined)
  cursor.execute(f'CREATE TABLE {tablename} ({joined})')
  file = open(old_name, 'r')
  csv_reader = csv.DictReader(file, delimiter=',')
  for row in csv_reader:
    city = ''
    data = []
    for name in headings.keys():
      try:
        n = row[name]
      except:
        n = row['date_time']
        n = n.split(' ')
        n = n[0].split('/')
        days = int(n[0])
        months = int(n[1])*100
        years = int(n[2])*10000
        n = days + months + years
      if name == 'country':
        n = n.upper()
        if n == 'NA':
          if city:
            if '(' in city:
              for count, countro in countries.items():
                if countro in city:
                  ind = city.index('(')
                  if city[ind+1:ind+len(countro)+1] == countro:
                    n = count
      if name == 'date_time':
        n = n.split(' ')
        date = n[0].split('/')
        date = f"{date[1]}/{date[0]}/{date[2]}"
        n=f'{date} {n[1]}'
      if name == 'city_area':
        n = n.lower()
        city = n
      #replacing codes with symbols for descriptions
      if isinstance(n, str):
        n = n.replace('&#44', ',')
        n = n.replace('&amp;', '&')
        n = n.replace('&#33', '!')
        n = n.replace('&#39', "'")
        n = n.replace('&quot;', '"')
        n = n.replace('&eacute', 'é')
        n = n.replace('&auml;', 'ä')
        n = n.replace('&ouml;' , 'ö')
        n = n.replace('&aacute;', 'á')
        n = n.replace('&#382;', 'ž')
        n = n.replace('&#283;', 'ě')
        n = n.replace('&#345;', 'ř')
        n = n.replace('&iacute;', 'í')
        n = n.replace('&yacute;', 'ý')
        n = n.replace('&#36', '$')
        n = n.replace('&oacute;', 'ó')
        n = n.replace('&eth;', 'ð')
      data.append(n)
    q_marks = ','.join('?'*len(data))
    #adding values to table
    cursor.execute(f'INSERT INTO {tablename} VALUES({q_marks})', data)
  file.close()
  connection.commit()
