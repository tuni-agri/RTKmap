
import requests
import re
import json

# talla koodilla haetaan pisteet ja muodostetaan json tiedosto

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

        with open('points.json', 'w') as f:
            json.dump(stations_data, f, indent=4)
            
        return stations_data
    except requests.RequestException as e:
        return {'error': str(e)}



# Aja tämä funktio päivittääksesi points.json-tiedoston tai käytä saatua dataa suoraan
stations_data = stations()
print(json.dumps(stations_data, indent=4))