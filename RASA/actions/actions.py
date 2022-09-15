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
#
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
         emotions = []
         for (emo,val) in emotion.top_emotions:
             emotions.append(emo)


         dispatcher.utter_message(text="It looks like you're feeling: {}".format(emotions))
         
         return []

class ActionStudentInfo(Action):

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
