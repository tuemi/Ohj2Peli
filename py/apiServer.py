#Testaan api:n käyttöä

from flask import Flask, request
import mysql.connector
import random

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

def haetaan_maat(maata):
    sql = f'select name from country where continent = "EU" ;'
    cursor = mydb_connect.cursor()
    cursor.execute(sql)
    result = cursor.fetchall()
    valitut = []
    while len(valitut) < maata:
        if random.choice(result) not in valitut:
            valitut.append(random.choice(result))
        elif random.choice(result) in valitut:
            result.remove(random.choice(result))
    return valitut


app = Flask(__name__)
@app.route('/maat')
def maat():

    vastaus = {
        "Täässä on maat": haetaan_maat(10)
    }

    return vastaus

if __name__ == '__main__':
    app.run(use_reloader=True, host='127.0.0.1', port=3000)