
from flask import Flask, jsonify, render_template
import requests
import re

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/stations')
def stations():
    try:
        # Hae RTK-asemien tiedot
        response = requests.get('http://rtk2go.com:2101/', timeout=5)
        data = response.text
        # Etsi kaikki ";FIN;" sisältävät rivit ja poimi niistä koordinaatit
        fin_stations = re.findall(r'.*;FIN;.*', data)
        stations_data = []
        for station in fin_stations:
            # Etsitään ";FIN;" merkkijonon indeksi
            fin_indeksi = station.find(";FIN;")
            osa = station[fin_indeksi + 5:] # Ohitetaan ";FIN;" ja otetaan loppuosa
            koordinaatit = osa.split(";")[:2] # Jaetaan osa puolipisteillä ja otetaan kaksi ensimmäistä arvoa
            stationInfo=station.split(";")
            stations_data.append({
            'lat': koordinaatit[0],
            'lon': koordinaatit[1],
            'stationName':stationInfo[1],
            'municipality':stationInfo[2]})

            
        return jsonify(stations_data)
    except requests.RequestException as e:
        return jsonify(error=str(e)), 500
if __name__ == '__main__':
    app.run(debug=True)

