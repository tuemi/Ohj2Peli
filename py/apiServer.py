#Testaan api:n käyttöä
import mysql.connector
from geopy.distance import geodesic as GD
import random
from flask import Flask, request

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
# Hakee tietokannasta tiety maiden määrä

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
        #elif random.choice(result) in valitut:
            #valitut.remove(random.choice(result))
       # print(rnd)
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
def maat():


    vastaus = {
        "Täässä on maat": listmaat
    }
    return vastaus

@app.route('/maat/kaupungit')
def kaupungit():
    kaupungit = haetaan_kaupungit()

    vastaus = {
        "Täässä on kaupungit": kaupungit
    }
    return vastaus

@app.route('/maat/kaupungit/koordinaatit')
def koordinaatit():
    koordinaatit = haetaan_koordinaatit()

    vastaus = {
        "koordinaatit": koordinaatit
    }
    return vastaus

@app.route('/test')
def test():
    vastaus = {"test": "abvc"}
    return vastaus

if __name__ == '__main__':
    app.run(use_reloader=True, host='127.0.0.1', port=3000)