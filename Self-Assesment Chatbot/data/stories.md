## begin conversation
* greet
  - utter_greet
  <!-- - utter_menu -->

<!-- ## combined begin with url
* greet
    - utter_greet
    - utter_menu
* begin_lead
    - utter_lead_q1
    - lead_form_p1
    - form{"name": "lead_form_p1"}
    - form{"name": null}
* accept
    - lead_form_p2
    - form{"name": "lead_form_p2"}
    - form{"name": null}
    - lead_form_p3
    - form{"name": "lead_form_p3"}
    - form{"name": null}
    - utter_lead_q3
    - utter_lead_q4
    - utter_lead_q5

## combined begin without url
* greet
    - utter_greet
    - utter_menu
* begin_lead
    - utter_lead_q1
    - lead_form_p1
    - form{"name": "lead_form_p1"}
    - form{"name": null}
* reject
    - lead_form_p3
    - form{"name": "lead_form_p3"}
    - form{"name": null}
    - utter_lead_q3
    - utter_lead_q4
    - utter_lead_q5 -->

## covid-19 stories happy path
* begin_assessment
    - assessment_form
    - form{"name":"assessment_form"}
    - form{"name":null}
    - utter_bye
    - action_reset_all_slots

## covid-19 stories unhappy path
* reject
    - utter_otherTime
    - utter_bye
    - action_reset_all_slots
* corona_state
 - action_corona_tracker

## start assessment stories
* start_assessment
    - utter_start_conv
* accept
    - assessment_form
    - form{"name":"assessment_form"}
    - form{"name":null}
    - utter_bye
    - action_reset_all_slots
* corona_state
 - action_corona_tracker

## start assessment unhappy
* start_assessment
    - utter_start_conv
* reject
    - utter_otherTime
    - utter_bye
    - action_reset_all_slots
## corona tracker path
* corona_state
 - action_corona_tracker