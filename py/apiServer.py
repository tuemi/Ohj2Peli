#Testaan api:n käyttöä
import mysql.connector
import random
from flask import Flask, request
from flask_cors import CORS, cross_origin

app = Flask(__name__)
cors = CORS(app)
app.config['CORS_HEADERS'] = 'Content-Type'

# Oman database kansion nimi ja salasana
name = 'flight_game'
psw = 'Salasana!'

mydb_connect = mysql.connector.connect(
         host='127.0.0.1',
         port=3306,
         database=name,
         user='root',
         password=psw,
         autocommit=True
         )

valitut = []

def haetaan_maat(maata):
    sql = f'select name,  city, latitude_deg, longitude_deg from europe;'
    cursor = mydb_connect.cursor()
    cursor.execute(sql)
    result = cursor.fetchall()


    while len(valitut) < maata:
        rnd = random.choice(result)
        if rnd not in valitut:
            valitut.append(rnd)
    maat=[]
    for i in valitut:
        maat.append(i[0])

    return maat

def haetaan_kaupungit():
    kaupungit = []
    for i in valitut:
        kaupungit.append(i[1])
    return kaupungit

def haetaan_koordinaatit():
    koordinaatit = []
    for i in valitut:
        koordinaatit.append(i[2:])
        print(koordinaatit)
    return koordinaatit

# Alusta oletusarvot
listmaat = haetaan_maat(10)
rahaa = 1500
esineet = []

# Pysty säätää paljon maita pitää hakee
maittenmaara = 10
maata = haetaan_maat(maittenmaara)
# Valitse randomisti maa jossa pelaaja aloittaa pelin
sijainti_tuple = random.choice(maata)
sijainti = list(sijainti_tuple)
palasia = 0

app = Flask(__name__)
@app.route('/maat')
@cross_origin()
def maat():
    vastaus = {
        "Täässä on maat": listmaat
    }
    return vastaus

@app.route('/maat/kaupungit')
@cross_origin()
def kaupungit():
    kaupungit = haetaan_kaupungit()
    vastaus = {
        "Täässä on kaupungit": kaupungit
    }
    return vastaus

@app.route('/maat/kaupungit/koordinaatit')
@cross_origin()
def koordinaatit():
    koordinaatit = haetaan_koordinaatit()
    vastaus = {
        "koordinaatit": koordinaatit
    }
    return vastaus



@app.route('/test')
@cross_origin()
def test():
    vastaus = {"test": "abvc"}
    return vastaus

#@app.route('/test')
#def test():
#    vastaus = {"test": "abvc"}
#    return vastaus

if __name__ == '__main__':
    app.run(use_reloader=True, host='127.0.0.1', port=3000)