import json
from recommender import *

filmoviFile = open('filmovi.json', 'r')
korisniciFile = open('korisnici.json', 'r')

filmoviJSON = json.loads(filmoviFile.read())
korisniciJSON = json.loads(korisniciFile.read())

filmoviFile.close()
korisniciFile.close()

filmovi = list()
korisnici = list()
for f in filmoviJSON:
    filmovi.append(Film(f['id_'], f['naziv'], set(f['tagovi'])))
for k in korisniciJSON:
    korisnici.append(Korisnik(k['username'], set(k['likes']), set(k['tagovi'])))

recc = Recommender(filmovi, korisnici)

username = input("Unesite username: ")
k = int(input("Unesite broj suseda: "))
n = int(input("Unesite broj preporuka: "))

li = recc.recommend(username, k, n)
for l in li:
    print(l.naziv)