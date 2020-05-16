from flask import Flask, render_template, jsonify, request
import sys
import sqlite3
import dash
import dash_html_components as html
import pandas as pd
import dash_core_components as dcc
app = Flask(__name__)

mapa = dash.Dash(__name__,server=app,routes_pathname_prefix='/mapa/')

con = sqlite3.connect("Sensor_Database/sensorData.db")
curs = con.cursor()
nombre = []
edad = []
lon = []
lat = []
sexo = []
enfermo = []
for fila in curs.execute("SELECT * FROM data"):
       nombre.append(fila[0])
       edad.append(fila[1])
       lon.append(fila[2])
       lat.append(fila[3])
       sexo.append(fila[4])
       enfermo.append(fila[5])
con.close()
mapa.layout = html.Div([
html.H1('Covid 19 en el valle de Aburrá'),
   dcc.Interval(
            id='interval-component',
            interval=1*1000, # in milliseconds
            n_intervals=0
        ),
    dcc.Graph(id='map', figure={
        'data': [{
            'lat': lat,
            'lon': lon,
            'marker': {
                'color': 150,
                'size': 100,
                'opacity': 0.6
            },
            'customdata': 3.5,
            'type': 'scattermapbox'
        }],
        'layout': {
            'mapbox': {
                'accesstoken': 'pk.eyJ1IjoibGVvbmFyZG9iZXRhbmN1ciIsImEiOiJjazlybGNiZWcwYjZ6M2dwNGY4MmY2eGpwIn0.EJjpR4klZpOHSfdm7Tsfkw',
                'center' : {
                    'lat': 6.240737,
                    'lon': -75.589900
                    },
                'zoom' : 10
            },
            'hovermode': 'closest',
            'margin': {'l': 0, 'r': 0, 'b': 0, 't': 0}

        }
    })
])
db_path = 'Sensor_Database/sensorData.db'
@app.route('/')
def home():
    return "hola mundo"
@app.route('/send_data', methods=['POST'])
def recibir():
    values = request.args
    data = request.form.to_dict(flat=False)
    #print(values)
    print(data)
    a=str(data.get("data"))
    b=  a.split(";")[0].split("'")[1]
    c = 23
    d = 12
    e = 7
    print(b)
    print("nombre = "+a.split(";")[0].split("'")[1])
    print("edad="+a.split(";")[1].split("=")[1])
    print("su longitud es "+a.split(";")[2].split("=")[1])
    print("su latitus es "+a.split(";")[3].split("=")[1])
    print("su sexo es "+a.split(";")[4].split("=")[1])
    print("Enfermedades bases es igual a "+a.split(";")[5].split("=")[1].split("'")[0])
    con = sqlite3.connect(db_path)
    cur = con.cursor()
    cur.execute("INSERT INTO data VALUES(" + "'" + a.split(";")[0].split("'")[1]+"'" + ","  + a.split(";")[1].split("=")[1] + "," + a.split(";")[2].split("=")[1] + "," + a.split(";")[3].split("=")[1] + ","+"'"+a.split(";")[4].split("=")[1] +"'"+ ","  +"'"+a.split(";")[5].split("=")[1].split("'")[0]+"'"+")")
    con.commit()
    con.close()
    return "ok",201

if __name__ == '__main__':
       app.run(debug=True,host='0.0.0.0',port=80)
