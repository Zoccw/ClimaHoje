import os
import requests
from dotenv import load_dotenv

load_dotenv()
API_KEY = os.getenv("CHAVE_API")
geourl = "http://api.openweathermap.org/geo/1.0/direct"
climaurl = "https://api.openweathermap.org/data/3.0/onecall"

# local = input()
def getLatLon(local):
    parametros = {"q": local, "appid": API_KEY}
    latlon = requests.get(geourl, parametros)
    if latlon.status_code == 200:
            dados = latlon.json()
            if not dados:
                print("lugar não encontrado")
                return None
            else:
                print(dados)
                return dados
    else:
        print(f'Erro: {latlon.status_code}')
        return None

# info = getLatLon(local)
# lat = info[0]["lat"]
# lon = info[0]["lon"]

def getWeather(lat, lon):
    parametros_clima = {
        "lat": lat,
        "lon": lon,
        "lang": "pt_br",
        "appid": API_KEY,
        "units": "metric"
    }
    weather = requests.get(climaurl, parametros_clima)
    if weather.status_code == 200:
        data = weather.json()
        print(data)
        return data

    else:
        print(f'Erro: {weather.status_code}')
        return None


# getLatLon(local)
#
# getWeather(lat, lon)
