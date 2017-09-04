"""
This file contains the code required to apply for certification as a Nationbuilder Developer.

I am required to do two tasks.
For Task Two I've chosen the Surveys + Contact section. I will be attempting all three tasks in it:

1. Create a Survey
2. Log a contact when someone answers a survey question.
"""

import json
import os
import random
from functools import partial
import time
import requests

nb_get = partial(requests.get,
                 params={'access_token': os.getenv("NB_TOKEN")},
                 headers={'content-type': 'application/json'})
nb_get.__doc__ = "requests.get function with the access token inside it and the headers variable set."

nb_post = partial(requests.post,
                  params={'access_token': os.getenv("NB_TOKEN")},
                  headers={'content-type': 'application/json'})
nb_post.__doc__ = "requests.get function with the access token inside it and the headers variable set."

nb_delete = partial(requests.delete,
                    params={'access_token': os.getenv("NB_TOKEN")},
                    headers={'content-type': 'application/json'})
nb_delete.__doc__ = "requests.get function with the access token inside it and the headers variable set."

nb_put = partial(requests.put,
                 params={'access_token': os.getenv("NB_TOKEN")},
                 headers={'content-type': 'application/json'})
nb_put.__doc__ = "requests.get function with the access token inside it and the headers variable set."


def generate_example_survey():
    example_survey = json.loads('''{
      "survey": {
        "slug": "survey",
        "name": "Survey",
        "tags": ["funny"],
        "status":"published",
        "questions": [{
          "prompt": "What issue is more important to you?",
          "external_id": null,
          "slug": "important_issue",
          "type": "multiple",
          "status": "published",
          "choices": [{
            "name": "Daily mail service to all homes. Yeah right....",
            "feedback": "really now...?"
          }, {
            "name": "Opposition to any change in our naturalization laws",
            "feedback": null
          }, {
            "name": "foobar",
            "feedback": "foobar"
          }, {
            "name": "Kansas should be admitted as a state",
            "feedback": null
          }]
        }]
      }
    }''')
    example_survey['survey']['slug'] = str(round(time.time(),1)) + "survey"
    example_survey['survey']['name'] = str(round(time.time(),1)) + "Survey"
    return example_survey

def generate_example_response(survey_id, person_id, question_id, response_ids):
    example_response = json.loads("""{
      "survey_response": {
        "survey_id": 0,
        "person_id": 0,
        "question_responses": [{
          "question_id": 1,
          "response": 3
        }]
      }
    }""")
    example_response['survey_response']['survey_id'] = survey_id
    example_response['survey_response']['person_id'] = person_id
    example_response['survey_response']["question_responses"][0]["response"] = random.choice(response_ids)
    example_response['survey_response']["question_responses"][0]["question_id"] = question_id
    return example_response

baseurl = "https://aliimami.nationbuilder.com/api/v1"
survey_url = baseurl + "/sites/aliimami/pages/surveys"
contact_url = baseurl + "/people/{}/contacts"
response_url = baseurl + "/survey_responses"

# Create a survey
newsurvey = nb_post(survey_url, json=generate_example_survey())

if newsurvey.status_code == 200:
    newsurvey_id = newsurvey.json()['survey']['id']
    newsurvey_question_id = newsurvey.json()['survey']['questions'][0]['id']
    newsurvey_option_ids = [item['id'] for item in newsurvey.json()['survey']['questions'][0]['choices']]

# Create a response to test against
newresponse = nb_post(response_url,
                      json=generate_example_response(newsurvey_id, random.choice([4, 5]),
                                                     newsurvey_question_id, newsurvey_option_ids))

# Grab the response person_id and log a contact
responses = nb_get(response_url)
responses = [res for res in responses.json()['results'] if res['survey_id'] == newsurvey_id]

example_contact = json.loads("""
{
    "contact": {
        "sender_id": 4,
        "author_id": 4,
        "method": "other",
        "type_id": 7,
        "status": "meaningful_interaction"
    }
}""")

contacts = []
for res in responses:
    contacts += nb_post(contact_url.format(res['person_id']), json=example_contact)
