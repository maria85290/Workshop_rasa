# This files contains your custom actions which can be used to run
# custom Python code.
#
# See this guide on how to implement these action:
# https://rasa.com/docs/rasa/custom-actions


# This is a simple example for a custom action which utters "Hello World!"

from typing import Any, Text, Dict, List

from rasa_sdk import Action, Tracker
from rasa_sdk.executor import CollectingDispatcher
import requests
from nrclex import NRCLex
#
from rasa_sdk import Tracker, FormValidationAction
from rasa_sdk.types import DomainDict
#
class ActionEmotion(Action):
#
    def name(self) -> Text:
         return "action_emotion"

    def run(self, dispatcher: CollectingDispatcher,
             tracker: Tracker,
             domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
         
         ## Vai buscar a ultima mensagem do utilizador;
         text = str (tracker.latest_message["text"])

         emotion = NRCLex (text)
         print(emotion.affect_frequencies)
         pos  = emotion.affect_frequencies['positive']
         neg = emotion.affect_frequencies['negative']
        
         if pos>=neg:
            dispatcher.utter_message(text="Fico feliz por estares a sentir-te bem!! Pareces muito positivo!!")
         else:
            dispatcher.utter_message(text="Parece-me que hoje estas bastante negativo! Acredita, o dia ainda vai melhorar!!")
         
         return []

class ActionStudentInfo(Action):

    '''
    Esta ação na resposta deve confirma a recepção dos número de aluno. 
    Tipo: "Recebido. Parece-me que este periodo as tuas notas estão bastantes melhores. Estas de parabéns!!"
    '''

    def name(self) -> Text:
        return "action_student_info"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        ## Seleciona um número aletorio para ser o aluno.

        responses = requests.get("http://localhost:3000/students/1").json()
        print(responses)
        dispatcher.utter_message(text="Response {}".format(responses))
        

        return []


def verify_number(number):
    f = False
    if int(number) > 0 and int(number) < 200:
        f = True
    return f


class ValidateIdentificationForm(FormValidationAction):
    def name(self) -> Text:
        return "validate_identification_form"

    def validate_student_number(
        self,
        slot_value: Any,
        dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain: DomainDict,
    ) -> Dict[Text, Any]:
        print(slot_value)
        # If the name is super short, it might be wrong.
        f = verify_number(slot_value)
        
        if f == False:
            dispatcher.utter_message(text="Indique um número de aluno válido. No intervalo: [0,199].")
            return {"student_number": None}
        return {"student_number": slot_value}