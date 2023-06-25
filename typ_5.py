from datetime import datetime, timedelta
from requests import request
from json import loads, dumps
from random import randint
from time import sleep
from csv import reader

def get_date_n_weeks_ago():
    today = datetime.now()
    delta = timedelta(weeks=1)
    n_weeks_ago = today - delta
    return n_weeks_ago

def fetch_jobs(url, company_id):
    print(company_id)
    payload = ""
    headers = {}
    response = request("GET", url, headers=headers, data=payload)
    response_json = loads(response.text)

    with open(f'./json/unamed/{company_id}.json', 'w') as outfile:
        outfile.write(dumps(response_json, indent=4))

    sleep(randint(3,7))

def fetch_seed_body():
    with open('./csv/seed.csv') as csv_input:
        data = [row for row in reader(csv_input)]
        data_header = data[0]
        data_body = data[1:]
        return data_body