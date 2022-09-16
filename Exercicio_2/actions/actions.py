from typing import Text, List, Any, Dict

from rasa_sdk import Tracker, FormValidationAction
from rasa_sdk.executor import CollectingDispatcher
from rasa_sdk.types import DomainDict


def verify_email(email):
    f = True
    if len(email)<4:
        f = False
    return f

class ValidateNameForm(FormValidationAction):
    def name(self) -> Text:
        return "validate_data_form"

    def validate_prof_name(
        self,
        slot_value: Any,
        dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain: DomainDict,
    ) -> Dict[Text, Any]:
        """Validate `prof_name` value."""

        # If the name is super short, it might be wrong.
        prof_name = slot_value

        if len(prof_name) == 0:
            dispatcher.utter_message(text="Nome do professor é inválido")
            return {"prof_name": None}
      
        return {"prof_name": prof_name}


    
    def validate_email(
        self,
        slot_value: Any,
        dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain: DomainDict,
    ) -> Dict[Text, Any]:
        """Validate `email` value."""

        # If the name is super short, it might be wrong.
        email = verify_email(slot_value)
        if email == False:
            dispatcher.utter_message(text="O e-mail é invalido.")
            return {"email": None}
        return {"email": slot_value}

