
from typing import Any, Text, Dict, List

from rasa_sdk import Action, Tracker
from rasa_sdk.executor import CollectingDispatcher

from api.turismo import TurismoAPI


ciudades = ["Amazonas", "Ancash", "Arequipa", "Cusco", "Ica", "La libertad", "Lambayeque",
            "Lima", "Loreto", "Madre de Dios", "Piura", "Puno", "San Martin", "Tumbes"]

api = TurismoAPI()


class ActionBuscarAtractivos(Action):
    def __init__(self) -> None:
        super().__init__()

    def name(self) -> Text:
        return 'action_buscar_atractivos'

    def run(self, dispatcher: CollectingDispatcher, tracker: Tracker, domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        dispatcher.utter_message(
            text="Lo siento no hemos encontrado nada atractivo")
        return []


class ActionBuscarDestino(Action):
    def __init__(self) -> None:
        super().__init__()

    def name(self) -> Text:
        return 'action_buscar_destino'

    def run(self, dispatcher: CollectingDispatcher, tracker: Tracker, domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        labels = {"desierto": "desierto", "montaña": "montana",
                  "playa": "playa", "mar": "playa", "selva": "selva", "valle": "valle"}

        # Obtener la entidad identificada
        current_entity = next(
            tracker.get_latest_entity_values("destino"), None)

        # Si el paisaje no se encuentra en la lista, omitir ya que la api fallaría
        if current_entity not in list(labels.keys()):
            current_entity = None
        else:
            current_entity = labels[current_entity]

        if current_entity:
            text = api.get_destinos(current_entity)

            if text is not None:
                text = 'Hemos encontrado un destino que te podría interesar:\n' + text
                dispatcher.utter_message(text=text)
                return []

        dispatcher.utter_message(
            text="Lo siento no hemos encontrado lo que estás buscando.")
        return []


class ActionSubmit(Action):
    def __init__(self) -> None:
        super().__init__()

    def name(self) -> Text:
        return 'action_submit'

    def run(self, dispatcher: CollectingDispatcher, tracker: Tracker, domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        dispatcher.utter_message(text="Formulario completado")
        return []


class ActionComoLlegar(Action):
    def __init__(self) -> None:
        super().__init__()

    def name(self) -> Text:
        return 'action_como_llegar'

    def run(self, dispatcher: CollectingDispatcher, tracker: Tracker, domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        entity_ciudad = next(
            tracker.get_latest_entity_values("departamento"), None)

        if entity_ciudad and entity_ciudad.lower() not in [x.lower() for x in ciudades]:
            entity_ciudad = None

        if entity_ciudad:
            result = api.how_to_get_to_city(entity_ciudad)
            if result:
                dispatcher.utter_message(text=result)
                return []

        dispatcher.utter_message(
            text="Lo siento no he encontrado una ruta para el lugar que estás buscando.")
        return []


class ActionMostrarExperiencias(Action):
    def __init__(self) -> None:
        super().__init__()

    def name(self) -> Text:
        return 'action_mostrar_experiencias'

    def run(self, dispatcher: CollectingDispatcher, tracker: Tracker, domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
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
        # Obtener la entidad identificada
        current_entity = next(
            tracker.get_latest_entity_values("experiencia"), None)

        # Si el paisaje no se encuentra en la lista, omitir ya que la api fallaría
        if current_entity not in list(labels.keys()):
            current_entity = None
        else:
            current_entity = labels[current_entity]

        if current_entity:
            res = api.get_experiencias(current_entity)
            if res:
                # Se le formato al response
                experiencias = res['Experiencias']

                text = 'Resultados\n'
                for experiencia in experiencias:
                    titulo = experiencia['Titulo']
                    subtitulo = experiencia['SubTitulo']
                    url = 'https://www.peru.travel' + \
                        experiencia['LinkPaginaRelativo']
                    text += f'- {titulo}: {subtitulo} ({url})'
                    text += '\n'
                dispatcher.utter_message(text=text)
                return []

        dispatcher.utter_message(
            text="Lo siento no hemos encontrado lo que estás buscando.")
        return []
