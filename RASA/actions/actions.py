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
from deep_translator import GoogleTranslator

def translate (sentence):
    
    to_translate = sentence
    translated = GoogleTranslator(source='auto', target='en').translate(to_translate)
    return translated
# outpout -> Ich möchte diesen Text übersetzen

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
        
         translated = translate (text)
        
         emotion = NRCLex (translated)
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
        print(tracker.slots)
        if "student_number" in tracker.slots:

        ## Seleciona um número aletorio para ser o aluno.
            print(str(tracker.slots['student_number']))
            responses = requests.get("http://localhost:3000/students/" + str(tracker.slots['student_number'])).json()
            print(responses)

            ## Avaliar situação de risco: Nota de portugues e matematica distam 2 ou mais valores 
            #(Por exemplo: mat: 5 e port: 3)
            print(abs(responses['5_ANO_3_PERIODO_PT'] - responses['5_ANO_3_PERIODO_MAT']))
            if abs(responses['5_ANO_3_PERIODO_PT'] - responses['5_ANO_3_PERIODO_MAT']) >= 2:
                dispatcher.utter_message(text="Situação de risco detetada!! As tua notas de português e matemática estão separada de pelo menos 2 valores. Atenção ao estudo! Se precisares eu posso pedir ao professor que te contacte.")
            else:
                 dispatcher.utter_message(text="As tuas notas mantém-se congruentes. Não se nota nenhuma discrepância relevante.")

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