#Testaan api:n käyttöä
import mysql.connector
from geopy.distance import geodesic as GD
import random
from flask import Flask, request, jsonify, render_template
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

valitut = [] # arvotut maat
palat = [] # arvotut kaupungit joissa palat

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
        kaupungit.append(i[1:]) # kaikki loppukentät
    #print(kaupungit)
    return kaupungit

def haetaan_kaupunki():
    kaupunki = []
    for i in valitut:
        if (i[0] == sijainti):
            kaupunki.append(i[1:])
        #kaupunki.append(i[1:]) # kaikki loppukentät
    #print(kaupunki)
    return kaupunki

"""
def haetaan_koordinaatit():
    koordinaatit = []
    for i in valitut:
        koordinaatit.append(i[2:]) ## vain kaksi viimeistä kenttää
        print(koordinaatit)
    return koordinaatit
"""
def matka(sijainti, maaranpaa):
    #print("DEBUG: matka")
    while True:
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
            break
        # Laske lipun hinta
        LIPUN_H = round(etaisyys * 0.4 + 30)
        laskutus = rahaa - LIPUN_H
        print(f"{'':5s} - {'':10s} lippu on {LIPUN_H} €")
        return laskutus

def lennetaan(sijainti, maata, kartapalat, palasia):
    print("DEBUG: lennetaan")
    print(f"\nMihin maahan haluat lentää?")
    print(f"Sinulla on rahaa {rahaa}€")
    print(f"\n {'':8.8s} {'Maat:':25.25s}")
    print(f"\nOlet maasa {sijainti}")

    #debug here
    for row in maata:
        #print("DB row: "+row)
        #for element in row:
        print(row, end=' ')
        laskutus = matka(sijainti, row)

    maaranpaa = input("Kirjoita maan nimi johon haluat lentää: ")
    print("Testi")
    print("def_lennetaan" )
    print(maaranpaa)
    #print(kartapalat)
    for i in kartapalat:
        print(i)


    if maaranpaa in kartapalat:
        print("\nOnneksi olkoon! Löysit kartan palasen!")
        palasia += 1
        print(palasia)
        print(countpalaset(palasia))
    else:
        print("\nValitettavasti tästä maasta ei löytynyt kartan palasta")
    laskutus = matka(sijainti, maaranpaa)
    return maaranpaa, laskutus, kartapalat, palasia

# Jos pelaajalla jää alle 500 euroa hän saa pelata uhkapelejä
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
                #print("Sinulla ei ole enää rahaa. GAME OVER.")
                break
            jatka = input("Haluatko jatkaa pelaamista? (k/e): ").lower()
            if jatka != "k":
                print("Kiitos pelaamisesta!")
                break
    elif Aloitus == "e":
        print("Kiitos pelaamisesta!")
    return rahaa

# Tämä koodi heitä randomisti kartan pala euroopan maihin
def maa_kartanpalat(maata):
    kartanpalat = random.sample(maata, 5)
    #print("Tämä tulee maa_kartanpalat")
    #print(kartanpalat)
    return kartanpalat

# Tässä on pelajan inventaario
def inventaario(rahaa, esineet, palasia):
    print("\nInventaario:")
    print(f"Rahaa: {rahaa}€")
    print("Maat jossa olit:")
    for esine in esineet:
        print(f" - {esine} [X]")
    print(f"Löydetyt karta palasia: {palasia}/5")

def countpalaset(palasia):
    return palasia + 1

def aloitus():
    sijainti = random.choice(maata)
    return sijainti
# Alusta oletusarvot
listmaat = haetaan_maat(10)
rahaa = 1500
esineet = []
palasia = 0

# Pysty säätää paljon maita pitää hakee
maittenmaara = 10
maata = haetaan_maat(maittenmaara)
# Valitse randomisti maa jossa pelaaja aloittaa pelin
print(f"Arvotut maat: {maata}")
kartapalat = maa_kartanpalat(maata)
print(f"Kartanpalat: {kartapalat}")
#print(kartapalat)

sijainti  = aloitus()
print(f"Olet maasa: {sijainti}")



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
        "kaupungit": kaupungit
    }
    print(vastaus)
    return vastaus

@app.route('/rahaa')
@cross_origin()
def rahat():
    rahat = rahaa
    vastaus = {
        "rahaa": rahat
    }
    print(vastaus)
    return vastaus

@app.route('/maat/aloitus')
@cross_origin()
def aloituskaupunki():
    aloituskaupunki = haetaan_kaupunki()
    vastaus = {
        "kaupungit": aloituskaupunki
    }
    print(vastaus)
    return vastaus

"""
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
"""


print("Pääsekö tämä tänne?")

@app.route('/location', methods=['GET', 'POST'])
@cross_origin()
def location():

    # POST request
    if request.method == 'POST':
        print(f'Uusi sijainti.. {request.get_json()}')
        print(request.get_json())  # parse as JSON
        return 'OK', 200

    # GET request
    else:
        message = {'greeting':'Hello from Flask!'}
        return jsonify(message)  # serialize and use JSON headers

@app.route('/test')
@cross_origin()
def test_page():
    # look inside `templates` and serve `index.html`
    return render_template('index.html')


if __name__ == '__main__':
    app.run(use_reloader=True, host='127.0.0.1', port=3000)