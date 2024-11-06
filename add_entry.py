import sqlite3
import csv
#function to process new entry and add to database
def add_entry(date_time, city, state, country, shape, encounter_length, described_encounter_length, description, date_documented, latitude, longitude, date_int):
  conn = sqlite3.connect('ufo.db')
  cursor = conn.cursor()
  command = 'INSERT INTO ufo_sightings VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?);'
  values = ((str(date_time)), (str(city)), (str(state)), (str(country)), str(shape), int(encounter_length), str(described_encounter_length), str(description), str(date_documented), float(latitude), float(longitude), int(date_int))
  #adding to table
  cursor.execute(command, values)
  #retrieving all data
  cursor.execute('SELECT date_time, city_area, state, country, ufo_shape, encounter_length, described_encounter_length, description, date_documented, latitude, longitude FROM ufo_sightings;')
  colnames = [desc[0] for desc in cursor.description]
  rows = cursor.fetchall()
  conn.commit()
  #writing all data to file
  with open('ufo_sightings1.csv', 'w', newline='') as file:
    writer = csv.writer(file)
    writer.writerow(colnames)  # write header
    for row in rows:
        writer.writerow(row)