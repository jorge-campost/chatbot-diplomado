import requests


class TurismoAPI:
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

    def get_destinos(self, paisaje):
        payload_tmpl = "{\"Version\": \"pe\",\"Modulo\": \"destinos\",\"Titulo\": \"%s\",\"Pagina\": 1,\"ListaParams\": {\"Buscador\": null,\"TipoFiltro\": 1,\"CadFiltroId\": null,\"NroPagina\": 1,\"NroRegistros\": 100},\"FlagInicial\": false,\"flagBusqueda\": false\n}"
        response = requests.request(
            "POST", self.url, headers=self.headers, data=payload_tmpl % paisaje)
        dests = response.json()

        destinos = dests['Destinos']

        # Se valida que los destinos sea una lista
        if not isinstance(destinos, list):
            return None

        # Creamos una cadena que contenta los nombres de cada destino
        text = ''
        for i, destino in enumerate(destinos):
            text += '- ' + destino['Titulo']
            if i != len(destinos)-1:
                text += '\n'

        return text

    def get_first_destination(self, dest):
        payload_tmpl = "{\"Version\": \"pe\",\"Modulo\": \"destinos\",\"Titulo\": \"%s\",\"Pagina\": 1,\"ListaParams\": {\"Buscador\": null,\"TipoFiltro\": 1,\"CadFiltroId\": null,\"NroPagina\": 1,\"NroRegistros\": 100},\"FlagInicial\": false,\"flagBusqueda\": false\n}"
        response = requests.request(
            "POST", self.url, headers=self.headers, data=payload_tmpl % dest)
        dests = response.json()
        return dests['Destinos'][0]

    def get_first_experience(self, exp):
        payload_tmpl = "{\"Version\":\"pe\",\"Modulo\":\"experiencias\",\"Titulo\":\"%s\",\"Pagina\":1,\"ListaParams\":{\"Buscador\":null,\"TipoFiltro\":4,\"CadFiltroId\":null,\"NroPagina\":1,\"FieldNameOrderBy\":\"ExperienciaTitulo asc\",\"NroRegistros\":6},\"FlagInicial\":false,\"flagBusqueda\":false}"
        response = requests.request(
            "POST", self.url, headers=self.headers, data=payload_tmpl % exp)
        exps = response.json()
        return exps['Experiencias'][0]

    def get_experiencias(self, exp):
        payload_tmpl = "{\"Version\":\"pe\",\"Modulo\":\"experiencias\",\"Titulo\":\"%s\",\"Pagina\":1,\"ListaParams\":{\"Buscador\":null,\"TipoFiltro\":4,\"CadFiltroId\":null,\"NroPagina\":1,\"FieldNameOrderBy\":\"ExperienciaTitulo asc\",\"NroRegistros\":6},\"FlagInicial\":false,\"flagBusqueda\":false}"
        response = requests.request(
            "POST", self.url, headers=self.headers, data=payload_tmpl % exp)
        exps = response.json()
        return exps

    def how_to_get_to_city(self, city):
        payload_tmpl = '{"Version":"es","Modulo":"destinos","Titulo":"%s","FlagInicial":true}'
        response = requests.request(
            "POST", self.url, headers=self.headers, data=payload_tmpl % city.lower())
        resp = response.json()
        rutas = resp['ComoLlegar']['Rutas'] or []
        result = []
        if rutas:
            rutas_length = len(rutas)
            if rutas_length > 1:
                result.append("Se ha encontrado %d rutas para llegar a %s:" % (
                    rutas_length, city))
            else:
                result.append(
                    "Se ha encontrado una ruta para llegar a %s:" % city)
            for ruta in rutas:
                for recorrido in ruta['Recorrido']:
                    result.append("%s %s %s" % (
                        recorrido['Titulo'], recorrido['Icono']['Titulo'], recorrido['Descripcion']))
        return "\n".join(result)
