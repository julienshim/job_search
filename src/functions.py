from requests import request
from json import loads, dumps
from time import sleep
from random import randint

def fetch_jobs(url, company_id):
    payload = ""
    headers = {}
    response = request("GET", url, headers=headers, data=payload)
    response_json = loads(response.text)

    with open(f'./json/{company_id}.json', 'w') as outfile:
        outfile.write(dumps(response_json, indent=4))

    sleep(randint(3,7))
