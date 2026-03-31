from flask import Flask, render_template, Request, url_for, request
from datetime import datetime, time, timedelta, timezone
import main

def check_dados(dados, *caminho):
    for chave in caminho:
        try:
            dados = dados[chave]
        except (KeyError, IndexError, TypeError):
            print(f"Erro ao acessar chave '{chave}' nos dados: {dados}")
            return None
    return dados

app = Flask(__name__, static_folder='static')
@app.after_request
def add_cache_headers(response):
        response.headers['Cache-Control'] = 'public, max-age=2629743'
        return response

@app.route('/', methods=['POST', 'GET'])
def index():
    clima_atual = None
    local = None
    tempo = None
    periodo = None
    condicao = None
    if request.method == 'POST':

        place = request.form.get('dado_place')
        localresultado = main.getLatLon(place)
        lat = check_dados(localresultado, 0, "lat")
        lon = check_dados(localresultado, 0, "lon")
        climaresultado = main.getWeather(lat, lon)

        # Conversão de Data

        hora = check_dados(climaresultado, "current", "dt")
        offset = check_dados(climaresultado, "timezone_offset")
        if hora is not None and offset is not None:
            fuso_horario = timezone(timedelta(seconds=offset))
            hora_data = datetime.fromtimestamp(hora, tz=fuso_horario)
            hora_formatada = hora_data.strftime("%H:%M")
            hora_fuso_formatada = hora_data.strftime("%Z")

            if time(6,0) <= hora_data.time() <= time(18,0):
                periodo = "dia"
                condicao = {
                "Thunderstorm": "⛈️",
                "Drizzle": "🌧️",
                "Rain": "🌧️",
                "Snow": "🌨️",
                "Mist": "🌫️",
                "Smoke": "🌫️",
                "Haze": "🌫️",
                "Fog": "🌫️",
                "Sand": "🌫️",
                "Dust": "🌫️",
                "Ash": "🌫️",
                "Squall": "💨",
                "Tornado": "🌪️",
                "Clear": "☀️",
                "Clouds": "☁️",
            }
            else:
                periodo = "noite"
                condicao = {
                "Thunderstorm": "⛈️",
                "Drizzle": "🌧️",
                "Rain": "🌧️",
                "Snow": "🌨️",
                "Mist": "🌫️",
                "Smoke": "🌫️",
                "Haze": "🌫️",
                "Fog": "🌫️",
                "Sand": "🌫️",
                "Dust": "🌫️",
                "Ash": "🌫️",
                "Squall": "💨",
                "Tornado": "🌪️",
                "Clear": "🌑",
                "Clouds": "☁️",
            }


        else:
            hora_formatada = ""
            hora_fuso_formatada = ""

        # Dicionários separados para cada função

        clima_atual = {
            "condicao": check_dados(climaresultado, "current", "weather", 0, "main"),
            "descricao": check_dados(climaresultado, "current", "weather", 0, "description"),
            "temp_atual": check_dados(climaresultado, "current", "temp"),
            "temp_min": check_dados(climaresultado, "daily", 0, "temp", "min"),
            "temp_max": check_dados(climaresultado, "daily", 0, "temp", "max"),
        }

        tempo = {
            "time": hora_formatada,
            "timezone": hora_fuso_formatada,
        }

        local = {
            "country": check_dados(localresultado, 0,"country"),
            "state": check_dados(localresultado,0, "state"),
        }

    return render_template("index.html", clima=clima_atual, localizacao=local, timedate=tempo, periodo=periodo, condicao=condicao)

if __name__ == '__main__':
    app.run(debug=True)
