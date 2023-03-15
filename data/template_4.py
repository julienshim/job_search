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


def get_job_ref_data(row):
    [import_date, company_name, id, jobOpeningName, departmentId, departmentLabel, employmentStatusLabel, location, isRemote, status, notes] = row
    tmp = {
        'job_reference_no': id,
        'job_company_name': company_name,
        'import_date': import_date
    }
    return tmp


def load_previously_imported_jobs():
    with open('') as ref:
        data = [row for row in reader(ref)][1:]
        data = list(map(get_job_ref_data, data))
        return data

all_job_items_fetched = fetch_items()
previously_imported_jobs_path = ''
previously_imported_jobs_path_exists = path.exists(previously_imported_jobs_path)
previously_imported_jobs = load_previously_imported_jobs() if previously_imported_jobs_path_exists else []
previously_imported_jobs_len = len(previously_imported_jobs)
all_target_keys = get_target_keys(all_job_items_fetched)
all_target_keys = ['id', 'jobOpeningName', 'employmentStatusLabel', 'location', 'isRemote']
csv_write_mode = 'a' if previously_imported_jobs_path_exists else 'w'


def job_is_previously_imported(job_reference_no, job_company_name):
    if previously_imported_jobs_len > 0:
        for job_item in previously_imported_jobs:
            if job_item['job_reference_no'] == job_reference_no and job_item['job_company_name'] == job_company_name:
                return job_item
    tmp = {'job_reference_no': '', 'import_date': ''}
    return tmp
