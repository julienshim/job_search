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
    
def fetch_all_jobs():
    reference = {
        'unamed': {
            'api': 'https://api.unamed.com/job-board/$$BT$$',
            'root_url': 'https://app.unamed.com/job-board/'
        }
    }

    seed_body = fetch_seed_body()
    tmp = {}

    for row in seed_body:
        [company_id, url, company_name, careers_page, api] = list(map(lambda x: x.strip(), row))
        if api in ['unamed']:
            board_token = careers_page.replace(reference[api]['root_url'], '')
            api_url = reference[api]['api'].replace('$$BT$$', board_token)
            response_jobs = fetch_jobs(api_url, company_id)

fetch_all_jobs()