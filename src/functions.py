from requests import request
from json import loads, dumps
from csv import reader
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

def fetch_seed_body(filter_value):
    with open('./csv/seed.csv') as csv_input:
        data = [row for row in reader(csv_input)]
        data_body = data[1:]
        data_body = list(filter(lambda x: filter_value in x[4].lower(), data_body))
        return data_body