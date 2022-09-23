from rasa_sdk import Action, Tracker


from api.turismo import TurismoAPI

import requests

api = TurismoAPI()

url = "https://api.peru.travel/api/contenido"
headers = {
    'Accept': '*/*',
    'Accept-Language': 'es-419,es;q=0.6',
    'Cache-Control': 'no-cache',
    'Connection': 'keep-alive',
    'Origin': 'https://www.peru.travel',
    'Pragma': 'no-cache',
    'Referer': 'https://www.peru.travel/',
    'Sec-Fetch-Dest': 'empty',
    'Sec-Fetch-Mode': 'cors',
    'Sec-Fetch-Site': 'same-site',
    'Sec-GPC': '1',
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/105.0.0.0 Safari/537.36',
    'authorization': 'Basic cGVydXRyYXZlbC51c2VyOlBAc3NkMDByZF8yMDIw',
    'content-type': 'application/json',
}

labels = {
    'histórico': 'historico-cultural',
    'cultural': 'historico-cultural',
    'gastronomía': 'gastronomia',
    'comida': 'gastronomia',
    'exclusivo': 'exclusivo',
    'entretenimiento': 'entretenimiento',
    'naturaleza': 'naturaleza',
    'aventura': 'aventura',
    'vivencial': 'vivencial'
}

experiencias = api.get_experiencias('naturaleza')['Experiencias']

text = 'Resultados\n'

for experiencia in experiencias:

    titulo = experiencia['Titulo']
    subtitulo = experiencia['SubTitulo']
    url = 'https://www.peru.travel'+experiencia['LinkPaginaRelativo']
    text += f'- {titulo}: {subtitulo} ({url})'
    text += '\n'

print(text)
