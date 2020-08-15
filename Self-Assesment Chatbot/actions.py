from typing import Dict, Text, Any, List, Union, Optional

from rasa_sdk import Tracker
from rasa_sdk import Action
from rasa_sdk.executor import CollectingDispatcher
from rasa_sdk.forms import FormAction
from rasa_sdk.events import SlotSet, EventType, Form, AllSlotsReset

from rasa_sdk import Action, Tracker
import requests


# class ActionStartInfo(Action):

#     def name(self) -> Text:
#         return "action_start_info"

#     def run(self, dispatcher: CollectingDispatcher,
#             tracker: Tracker,
#             domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

#         dispatcher.utter_message(text="Hello, there 👋 We understand times are tough and everyone is panicking.")
#         dispatcher.utter_message(text="But we're here to help ease it out for you!")
#         dispatcher.utter_message(text="Our coronavirus self-assessment scan has been developed on the basis of guidelines from the WHO. ")
#         dispatcher.utter_message(text="If you feel any of the symptoms please visit your nearest COVID-19 center and safeguard others around you 🙏")
#         dispatcher.utter_message(text="Can we proceed with your assessment now?")
#         return []

class ResetAllSlots(Action):

     def name(self) -> Text:
            return "action_reset_all_slots"

     def run(self, dispatcher: CollectingDispatcher,
             tracker: Tracker,
             domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        #  dispatcher.utter_message("Hello World!")

         return [AllSlotsReset()]

class AssessmentForm(FormAction):
    """Example of a custom form action"""

    def name(self) -> Text:
        """Unique identifier of the form"""

        return "assessment_form"

    @staticmethod
    def required_slots(tracker: Tracker) -> List[Text]:
        """A list of required slots that the form has to fill"""
        return ["age", "gender","bodyTemperature", "symptoms1","symptoms2","travelHistory","medicalHistory","symptomChanges"]

    def slot_mappings(self) -> Dict[Text, Union[Dict, List[Dict]]]:
        """A dictionary to map required slots to
            - an extracted entity
            - intent: value pairs
            - a whole message
            or a list of them, where a first match will be picked"""
        return {
            "age": [
                self.from_text(),
            ],
            "gender": [
                self.from_text(),
            ],
            "bodyTemperature": [
                self.from_text(),
            ],
            "symptoms1": [
                self.from_text(),
            ],
            "symptoms2": [
                self.from_text(),
            ],
            "travelHistory": [
                self.from_text(),
            ],
            "medicalHistory": [
                self.from_text(),
            ],
            "symptomChanges": [
                self.from_text(),
            ],
        }

    @staticmethod
    def is_int(string: Text) -> bool:
        """Check if a string is an integer"""
        try:
            int(string)
            return True
        except ValueError:
            return False

    def validate_age(
        self,
        value: Text,
        dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain: Dict[Text, Any],
    ) -> Dict[Text, Any]:
        """Validate age value."""

        if self.is_int(value) and int(value) <= 16:
            return {"age": "below16"}
        elif self.is_int(value) and int(value) >= 107:
            return {"age": "above107"}
        elif self.is_int(value):
            return {"age": value}
        else:
            dispatcher.utter_message(template="utter_wrong_age_format")
            return {"age": None}


    def request_next_slot(
        self,
        dispatcher: "CollectingDispatcher",
        tracker: "Tracker",
        domain: Dict[Text, Any],
    ) -> Optional[List[EventType]]:
        """Request the next slot and utter template if needed,
            else return None"""
        for slot in self.required_slots(tracker):
            if self._should_request_slot(tracker, slot):

                ## Condition of validated slot that triggers deactivation
                if slot == "gender" and tracker.get_slot("age") == "below16":
                    # dispatcher.utter_message(text="Sorry, I can't help you with that")
                    dispatcher.utter_message(template="utter_under_16")
                    return [self.deactivate(), AllSlotsReset()]
                elif slot == "gender" and tracker.get_slot("age") == "above107":
                    dispatcher.utter_message(template="utter_above_107")
                    return [self.deactivate(), AllSlotsReset()]

                ## For all other slots, continue as usual
                # logger.debug(f"Request next slot '{slot}'")
                dispatcher.utter_message(
                    template=f"utter_ask_{slot}", **tracker.slots
                )
                return [SlotSet("requested_slot", slot)]
        return None

    # def validate_age(
    #     self,
    #     value: Text,
    #     dispatcher: CollectingDispatcher,
    #     tracker: Tracker,
    #     domain: Dict[Text, Any],
    # ) -> Dict[Text, Any]:
    #     """Validate cuisine value."""

    #     print("coming in age validation method",value)
    #     return {"age": value}
    #     # if value.lower() in self.cuisine_db():
    #     #     # validation succeeded, set the value of the "cuisine" slot to value
    #     #     return {"cuisine": value}
    #     # else:
    #     #     dispatcher.utter_message(template="utter_wrong_cuisine")
    #     #     # validation failed, set this slot to None, meaning the
    #     #     # user will be asked for the slot again
    #     #     return {"cuisine": None}

    def submit(
        self,
        dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain: Dict[Text, Any],
    ) -> List[Dict]:
        """Define what the form has to do
            after all required slots are filled"""

        # utter submit template
        # dispatcher.utter_message("All slots are takens. Thanks")
        print(tracker.current_slot_values())
        all_slots = tracker.current_slot_values()
        
        bodyTemperature = all_slots['bodyTemperature']
        symptoms1 = all_slots['symptoms1'].split(",")
        symptoms2 = all_slots['symptoms2'].split(",")
        symptomChanges = all_slots['symptomChanges']
        medicalHistory = all_slots['medicalHistory']
        print(bodyTemperature, symptoms1, symptoms2, symptomChanges, medicalHistory)
        if bodyTemperature == "Normal (96°F-98.6°F or 35.5°C-37°C)":
            if ("None of these" in symptoms1) or ((len(symptoms1) == 1) and ("None of these" not in symptoms1) and ("All the above" not in symptoms1)):
                if ("None of these" in symptoms2) or ((len(symptoms2) == 1) and ("None of these" not in symptoms2) and ("All the above" not in symptoms2)):
                    if (symptomChanges == "Improved") or (symptomChanges == "Same, no change!"):
                        print("coming 175")
                        res = "utter_low"
                    else:
                        print("coming 178")
                        res = "utter_medium"
                else:
                    print("coming 181")
                    res = "utter_medium"
            else:
                res = "utter_medium"
        elif bodyTemperature == "Fever (98.7°F-102°F or 37°C-38.8°C)":
            if ((len(symptoms1) == 1) and ("None of these" not in symptoms1) and ("All the above" not in symptoms1)):
                if ((len(symptoms2) == 1) and ("None of these" not in symptoms2) and ("All the above" not in symptoms2)):
                    if medicalHistory != "None of these":
                        print("coming 189")
                        res = "utter_medium"
                    else:
                        print("coming 192")
                        res = "utter_medium"
                elif "None of these" in symptoms2:
                    print("coming 195")
                    res = "utter_low"
                elif "All the above" in symptoms2:
                    print("coming 198")
                    res = "utter_high"
                else:
                    print("coming 201")
                    res = "utter_high"
            elif "None of these" in symptoms1:
                print("coming 204")
                res = "utter_low"
            elif "All the above" in symptoms1:
                print("coming 207")
                res = "utter_high"
            else:
                print("coming in 210")
                res = "utter_high"
        elif bodyTemperature == "High Fever (>102°F or >38.8°C)":
            if ((len(symptoms1) == 2) or ("All the above" in symptoms1)):
                if ((len(symptoms2) == 2) or ("All the above" in symptoms2)):
                    if (symptomChanges == "Bad") or (symptomChanges == "Bad Considerably"):
                        print("coming 216")
                        res = "utter_high"
                    else:
                        print("coming 219")
                        res = "utter_high"
                else:
                    print("coming 222")
                    res = "utter_medium"
            else:
                print("coming 225")
                res = "utter_medium"
        print("based on conditions",res)
        dispatcher.utter_message(template=res)
        # dispatcher.utter_template("utter_showResult", tracker)
        return [AllSlotsReset()]


# class LeadFormFirstPart(FormAction):
#     """Example of a custom form action"""

#     def name(self) -> Text:
#         """Unique identifier of the form"""

#         return "lead_form_p1"

#     @staticmethod
#     def required_slots(tracker: Tracker) -> List[Text]:
#         """A list of required slots that the form has to fill"""
#         return ["requirement", "mockup"]

#     def slot_mappings(self) -> Dict[Text, Union[Dict, List[Dict]]]:
#         """A dictionary to map required slots to
#             - an extracted entity
#             - intent: value pairs
#             - a whole message
#             or a list of them, where a first match will be picked"""
#         return {
#             "requirement": [
#                 self.from_text(),
#             ],
#             "mockup": [
#                 self.from_text(),
#             ],
#         }

#     def submit(
#         self,
#         dispatcher: CollectingDispatcher,
#         tracker: Tracker,
#         domain: Dict[Text, Any],
#     ) -> List[Dict]:
#         """Define what the form has to do
#             after all required slots are filled"""

#         # utter submit template
#         dispatcher.utter_template("utter_urlAvailable", tracker)
#         return []


# class LeadFormSecondPart(FormAction):
#     """Example of a custom form action"""

#     def name(self) -> Text:
#         """Unique identifier of the form"""

#         return "lead_form_p2"

#     @staticmethod
#     def required_slots(tracker: Tracker) -> List[Text]:
#         """A list of required slots that the form has to fill"""
#         return ["url"]

#     def slot_mappings(self) -> Dict[Text, Union[Dict, List[Dict]]]:
#         """A dictionary to map required slots to
#             - an extracted entity
#             - intent: value pairs
#             - a whole message
#             or a list of them, where a first match will be picked"""
#         return {
#             "url": [
#                 self.from_text(),
#             ],
#         }

#     def submit(
#         self,
#         dispatcher: CollectingDispatcher,
#         tracker: Tracker,
#         domain: Dict[Text, Any],
#     ) -> List[Dict]:
#         """Define what the form has to do
#             after all required slots are filled"""
            
#         return []


# class LeadFormThirdPart(FormAction):
#     """Example of a custom form action"""

#     def name(self) -> Text:
#         """Unique identifier of the form"""

#         return "lead_form_p3"

#     @staticmethod
#     def required_slots(tracker: Tracker) -> List[Text]:
#         """A list of required slots that the form has to fill"""
#         return ["timeline", "budget", "name", "email", "phone"]

#     def slot_mappings(self) -> Dict[Text, Union[Dict, List[Dict]]]:
#         """A dictionary to map required slots to
#             - an extracted entity
#             - intent: value pairs
#             - a whole message
#             or a list of them, where a first match will be picked"""
#         return {
#             "timeline": [
#                 self.from_text(),
#             ],
#             "budget": [
#                 self.from_text(),
#             ],
#             "name": [
#                 self.from_text(),
#             ],
#             "email": [
#                 self.from_text(),
#             ],
#             "phone": [
#                 self.from_text(),
#             ],
#         }

#     def submit(
#         self,
#         dispatcher: CollectingDispatcher,
#         tracker: Tracker,
#         domain: Dict[Text, Any],
#     ) -> List[Dict]:
#         """Define what the form has to do
#             after all required slots are filled"""

#         # utter submit template
#         dispatcher.utter_template("utter_lead_q2", tracker)
#         return []

class ActionCoronaTracker(Action):

    def name(self) -> Text:
        return "action_corona_tracker"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        response = requests.get("https://api.covid19india.org/data.json").json()
        entities = tracker.latest_message['entities']
        print("Last Message Now",entities)
        state = None
        for e in entities:
            if e['entity'] == "state":
                state = e['value']
        message = "Please enter correct state name"

        if state == "india":
            state = "Total"
        for data in response["statewise"]:
            if data["state"] == state.title():
                print(data)
                message = "Active: "+data["active"] +" Confirmed: " + data["confirmed"] +" Recovered: "+data["recovered"]+" On "+data["lastupdatedtime"]
        dispatcher.utter_message(message)

        return []

