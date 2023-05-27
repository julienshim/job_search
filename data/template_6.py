from csv import reader, writer
from re import sub
from requests import request
from json import loads
from time import sleep
from random import randint
from datetime import datetime
from os import path

def fetch_jobs(url):
    payload = ""
    headers = {}
    response = request("GET", url, headers=headers, data=payload)
    response_json = loads(response.text)

    if '' in response_json:
        jobs_found = response_json['']
        return jobs_found
    return []

def fetch_seed_body():
    with open('') as csv_input:
        data = [row for row in reader(csv_input)]
        data_header = data[0]
        data_body = data[1:]
        return data_body
    
def fetch_all_jobs():
    reference = {
        '': {
            '',
            ''
        },
        '': {
            '',
            ''
        }
    }

    seed_body = fetch_seed_body()
    tmp = {}
    for row in seed_body:
        [company_id, url, company_name, careers_page, api] = list(map(lambda x: x.strip(), row))
        if company_id in ['']:
            api_url = ''
            if company_id in ['']:
                api_url = careers_page
            elif api in ['']:
                board_token = careers_page.replace(reference[api])
                api_url = reference[api]
            response_jobs = fetch_jobs(api_url)
            response_jobs_len = len(response_jobs)

            if response_jobs_len > 0:
                print(f'')
                if company_name in tmp:
                    tmp[company_name] += response_jobs
                else:
                    tmp[company_name] = response_jobs
            random_int = randint(3,7)
            sleep(random_int)
    return tmp

def get_target_keys(all_job_items_fetched):
    tmp = []
    for company in all_job_items_fetched:
        for job_item in all_job_items_fetched[company]:
            keys = job_item.keys()
            for key in keys:
                if key not in tmp:
                    tmp.append(key)
    return tmp

def get_job_ref_data(row):
    [import_date, company_name, absolute_url, education, internal_job_id, location, id, updated_at, title, content, departments, offices, status, notes] = row
    tmp = {
        '': id,
        '': company_name,
        '': import_date
    }
    return tmp