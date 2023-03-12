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

    if 'result' in response_json:
        jobs_found = response_json['result']
        return jobs_found
    return []

def fsb():
    with open('') as csv_input:
        data = [row for row in reader(csv_input)]
        data_header = data[0]
        data_body = data[1:]
        return data_body

def fetch_items():
    sb = fsb()
    tmp = {}

    for row in sb:
        [company_id, url, company_name, careers_page, api] = list(map(lambda x: x.strip(), row))
        if api in ['']:
            api_url = careers_page
            response_jobs = fetch_jobs(api_url)
            response_jobs_len = len(response_jobs)

            if response_jobs_len > 0:
                print(f'Fetching {company_name} jobs... {response_jobs_len} jobs found')
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
