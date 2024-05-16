import mysql.connector
from geopy.distance import geodesic as GD
import random
from flask import Flask, request, jsonify, render_template
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

# Database configuration
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

valitut = []  # Selected countries
palat = []  # Selected cities with map pieces

def haetaan_maat(maata):
    sql = 'SELECT name, city, latitude_deg, longitude_deg FROM europe;'
    cursor = mydb_connect.cursor()
    cursor.execute(sql)
    result = cursor.fetchall()

    while len(valitut) < maata:
        rnd = random.choice(result)
        if rnd not in valitut:
            valitut.append(rnd)
    maat = [i[0] for i in valitut]
    return maat

def haetaan_kaupungit():
    return [i[1:] for i in valitut]

def haetaan_kaupunki():
    return [i[1:] for i in valitut if i[0] == sijainti]

def matka(sijainti, maaranpaa):
    sql1 = f'SELECT latitude_deg, longitude_deg FROM europe WHERE name = "{sijainti}"'
    cursor1 = mydb_connect.cursor()
    cursor1.execute(sql1)
    result1 = cursor1.fetchone()
    sql2 = f'SELECT latitude_deg, longitude_deg FROM europe WHERE name = "{maaranpaa}"'
    cursor2 = mydb_connect.cursor()
    cursor2.execute(sql2)
    result2 = cursor2.fetchone()
    etaisyys = GD(result1, result2).km

    if sijainti[0] == maaranpaa:
        return rahaa
    LIPUN_H = round(etaisyys * 0.4 + 30)
    laskutus = rahaa - LIPUN_H
    return laskutus

def lennetaan(sijainti, maata, kartapalat, palasia):
    print(f"\nMihin maahan haluat lentää? Sinulla on rahaa {rahaa}€")
    for row in maata:
        print(row, end=' ')
        laskutus = matka(sijainti, row)

    maaranpaa = input("Kirjoita maan nimi johon haluat lentää: ")
    if maaranpaa in kartapalat:
        print("\nOnneksi olkoon! Löysit kartan palasen!")
        palasia += 1
        print(palasia)
        print(countpalaset(palasia))
    else:
        print("\nValitettavasti tästä maasta ei löytynyt kartan palasta")
    laskutus = matka(sijainti, maaranpaa)
    return maaranpaa, laskutus, kartapalat, palasia

def pelaa_uhkapelia(rahaa):
    if rahaa <= 500:
        print("\nSinulla on alle 500€, saat pelata uhkapeliä!")

    Aloitus = input("Haluatko pelata? (k/e): ").lower()
    if Aloitus == "k":
        while True:
            print("\nSinulla on", rahaa, "€.")
            panos = int(input("Kuinka paljon haluat panostaa? (1-" + str(rahaa) + "): "))
            if panos <= 0 or panos > rahaa:
                print("Virheellinen panos. Panoksen on oltava välillä 1-" + str(rahaa) + "€.")
                continue
            kolikko = random.randint(1, 2)
            if kolikko == 1:
                rahaa += panos
                print("Voitit! Sinulla on nyt", rahaa, "€.")
            else:
                rahaa -= panos
                print("Hävisit. Sinulla on nyt", rahaa, "€.")
            if rahaa <= 0:
                break
            jatka = input("Haluatko jatkaa pelaamista? (k/e): ").lower()
            if jatka != "k":
                print("Kiitos pelaamisesta!")
                break
    elif Aloitus == "e":
        print("Kiitos pelaamisesta!")
    return rahaa

def maa_kartanpalat(maata):
    return random.sample(maata, 5)

def inventaario(rahaa, esineet, palasia):
    print("\nInventaario:")
    print(f"Rahaa: {rahaa}€")
    print("Maat jossa olit:")
    for esine in esineet:
        print(f" - {esine} [X]")
    print(f"Löydetyt kartan palasia: {palasia}/5")

def countpalaset(palasia):
    return palasia + 1

def aloitus():
    return random.choice(maata)

# Initialize default values
listmaat = haetaan_maat(10)
rahaa = 1500
esineet = []
palasia = 0

maittenmaara = 10
maata = haetaan_maat(maittenmaara)
kartapalat = maa_kartanpalat(maata)
sijainti = aloitus()

@app.route('/maat')
@cross_origin()
def maat():
    return jsonify({"maat": listmaat})

@app.route('/maat/kaupungit')
@cross_origin()
def kaupungit():
    return jsonify({"kaupungit": haetaan_kaupungit()})

@app.route('/rahaa')
@cross_origin()
def rahat():
    return jsonify({"rahaa": rahaa})

@app.route('/maat/aloitus')
@cross_origin()
def aloituskaupunki():
    return jsonify({"kaupungit": haetaan_kaupunki()})

@app.route('/location', methods=['GET', 'POST'])
@cross_origin()
def location():
    if request.method == 'POST':
        return 'OK', 200
    else:
        return jsonify({'greeting':'Hello from Flask!'})

@app.route('/test')
@cross_origin()
def test_page():
    return render_template('index.html')

if __name__ == '__main__':
    app.run(use_reloader=True, host='127.0.0.1', port=3000)
