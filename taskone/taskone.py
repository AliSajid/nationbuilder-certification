"""
This file contains the code required to apply for certification as a Nationbuilder Developer.

I am required to do two tasks.
For Task One I've chosen the People section. I will be attempting all three tasks in it:

1. Create a Person
2. Update a Person
3. Delete the Person
"""
import json
import os
from functools import partial

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

person_example = json.loads("""{
  "person": {
    "email": "bob@example.com",
    "last_name": "Smith",
    "first_name": "Bob",
    "sex": "M",
    "signup_type": 0,
    "employer": "Dexter Labs",
    "party": "P",
    "registered_address": {
      "state": "TX",
      "country_code": "US"
    }
  }
}""")

person_update = json.loads("""{
  "person": {
    "first_name": "Joe",
    "email": "johndoe@gmail.com",
    "phone": "303-555-0841"
  }
}
""")

baseurl = "https://aliimami.nationbuilder.com/api/v1"
people_url = baseurl + "/people"

# Create a person
newperson = nb_post(people_url, json=person_example)

if newperson.status_code == 201:
    newperson_id = newperson.json()['person']["id"]

# Update a person
updatedperson = nb_put(people_url + "/{}".format(newperson_id), json=person_update)

# Delete a person
deleted_person = nb_delete(people_url + "/{}".format(newperson_id))
