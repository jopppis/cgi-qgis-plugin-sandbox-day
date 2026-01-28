# Demo

Navicin demo:ssa pääsee kokeilemaan helposti näitä ja dev toolsseista näkee millaisia kutsuja lähtee ja tulee!

https://demo.navici.com

# Geocoding

Hakee pisteen tekstillä. Hyvä integroida esim. hakupalkin näytettäviin tuloksiin.

Osoite: https://mapservices.navici.com/geocoding/geocode

| Parametri | Kuvaus | Pakollinen | Oletus | Vaihtoehdot |
|-----------|--------|------------|--------|-------------|
| address | Haettava osoite | Kyllä | - | - |
| apikey | API-avain | Kyllä | - | - |
| crs | Koordinaattijärjestelmä | Ei | EPSG:3067 | EPSG:xxxx |
| lang | Kieli | Ei | fi, sv | fi |
| source | Lähteet mitä vasten geokoodataan (voi olla monta) | Ei | vrkAddress,digiroadAddress,osmPlace,mmlPlace | vrkAddress,digiroadAddress,osmPlace,mmlPlace |
| type | Tulosten tyyppi | Ei | address,interpolation,place,centroid | address,interpolation,place,centroid |
| limit | Tulosten maksimimäärä | Ei | 3 | - |

```
# Esimerkkikutsu (apikey puuttuu)

https://mapservices.navici.com/geocoding/geocode?address=karvaamokuja&crs=EPSG:3067&lang=fi&source=digiroadAddress%7CvrkAddress&limit=5&apikey=1234
```
# Reverse Geocoding

Hakee pisteelle tiedot aineistosta. Hyvä integroida esim. kartta klikkaukseen jolloin haetaan pisteelle tietoja.

Osoite: https://mapservices.navici.com/geocoding/reverse

| Parametri | Kuvaus | Pakollinen | Oletus | Vaihtoehdot |
|-----------|--------|------------|--------|-------------|
| x | Haettavan pisteen X koordinaatti | Kyllä | - | - |
| y | Haettavan pisteen Y koordinaatti |Kylla | - | - |
| apikey | API-avain | Kyllä | - | - |
| from | Annetun pisteen koordinaattujärjestelmä | Ei | EPSG:3067 | EPSG:xxxx |
| to | Löydettyjen featureiden haluttu koordinaattijärjestelmä | Ei | EPSG:3067 | EPSG:xxxx |
| lang | Kieli | Ei | fi, sv | fi |
| source | Lähteet mistä haetaan pistettä (voi olla monta) | Ei | vrkAddress,digiroadAddress,osmPlace,mmlPlace | vrkAddress,digiroadAddress,osmPlace,mmlPlace |
| type | Tulosten tyyppi | Ei | address,interpolation,place | address,interpolation,place |
| limit | Tulosten maksimimäärä | Ei | 1 | - |

```
# Esimerkkikutsu (apikey puuttuu)

https://mapservices.navici.com/geocoding/reverse?x=382673.223879898&y=6677288.382904084&to=EPSG:3067&from=EPSG:3067&lang=fi&limit=1&maxdistance=100&mmlFilter=48111%2C48112%2C48120&offset=0&source=osmPlace%2CvrkAddress&type=address&apikey=1234
```

# Routing

routing api hakee reitin kahden pisteen välillä, joko ajan tai pituuden mukaan.

| Parametri | Kuvaus | Pakollinen | Oletus | Vaihtoehdot |
|-----------|--------|------------|--------|-------------|
| x | Pisteen X koordinaatti | Kyllä (vähintään 2 kpl) | - | - |
| y | Pisteen Y koordinaatti | Kyllä (vähintään 2 kpl) | - | - |
| apikey | API-avain | Kyllä | - | - |
| from | Lähtökoordinaattijärjestelmä | Ei | EPSG:3067 | EPSG:xxxx |
| to | Tuloskoordinaattijärjestelmä | Ei | EPSG:3067 | EPSG:xxxx |
| method | Kulkutapa (suosutus käyttää vain autoreititykseen) | Ei | car | car, bike, walk |
| mode | Reititykseen käytetty metriikka | Ei | time | time, len |
| lang | Kieli | Ei | fi | fi, sv, en |
| debug | Palauttaa etäisyyden lisäksi geometrian | Ei | no | yes, no |
| longDistanceAlgorithm | Pitkän matkan algoritmi | Ei | tripleBuffer | tripleBuffer, closestMainRoad |


```
# Esimerkkikutsu (apikey puuttuu)

https://mapservices.navici.com/routing/v1/route?x=24.821892&y=60.210487&x=26.8352324&y=61.0618088&from=EPSG:4326&apikey=1234
```

# TSP (Traveling Salesman Problem)

TSP api hakee optimaalisen reitin monen pisteen reitityksessä, joko ajan tai pituuden mukaan.

| Parametri | Kuvaus | Pakollinen | Oletus | Vaihtoehdot |
|-----------|--------|------------|--------|-------------|
| x | Pisteen X koordinaatti | Kyllä (vähintään 2 kpl) | - | - |
| y | Pisteen Y koordinaatti | Kyllä (vähintään 2 kpl) | - | - |
| apikey | API-avain | Kyllä | - | - |
| from | Lähtökoordinaattijärjestelmä | Ei | EPSG:3067 | EPSG:xxxx |
| to | Tuloskoordinaattijärjestelmä | Ei | EPSG:3067 | EPSG:xxxx |
| method | Pisteiden läpikäyntitapa | Ei | loop | loop,roundtrip,fixedstart,fixedend |
| result | Tarkka vai arvio | Ei | estimate | estimate,accurate |
| mode | Reititykseen käytetty metriikka | Ei | time | time, len |
| lang | Kieli | Ei | fi | fi, sv, en |
| output | Mitä tietoja halutaan reitistä | Ei | summary | summary,list,points,lines |


```
# Esimerkkikutsu (apikey puuttuu)

https://mapservices.navici.com/tsp/v1/solve?x=24.821892&y=60.210487&x=26.8352324&y=61.0618088&x=25&y=61=&from=EPSG:4326&apikey=1234
```
