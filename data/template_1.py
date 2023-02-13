from requests import request
from bs4 import BeautifulSoup
from time import sleep
from random import randint
from csv import writer, reader
from datetime import datetime
from os import path


def get_soup(page_number):
    url = ''

    payload={}
    headers = {}

    response = request('GET', url, headers=headers, data=payload)
    soup = BeautifulSoup(response.text, 'html.parser')
    return soup

def parse_inline_text(inline_text):
    return inline_text.string

def parse_job_item(job_item):
    job_title = job_item.find('h3', class_='job-item-title').string
    job_link = ''
    job_reference = job_item.find('input', class_='jetboost-list-item')['value']
    inline_text = list(map(parse_inline_text, job_item.find_all('div', class_='inline-text')))
    [city, seperator, state] = inline_text[0:3]
    remote_possible = job_item.find('div', class_='remote-slug w-condition-invisible') is None
    employment_type = inline_text[-1]

    job_item_dict = {
        'job_title': job_title.strip(),
        'job_link': job_link.strip(),
        'job_reference_no': job_reference.strip(),
        'city': city.strip(),
        'state': state.strip(),
        'remote_possible': remote_possible,
        'employment_type': employment_type.strip()
    }
    
    return job_item_dict


def fetch_all_jobs():
    running = True
    current_page_number = 1
    tmp = []

    while running:
        soup = get_soup(current_page_number)
        job_items = soup.find_all('div', class_='job-item')
        job_items_parsed = list(map(parse_job_item, job_items))
        job_items_parsed_len = len(job_items_parsed)

        if job_items_parsed_len == 0:
            running = False
        else:
            print(f'Fetching Page {current_page_number} jobs... {job_items_parsed_len} job(s) found')
            tmp += job_items_parsed
            current_page_number += 1
            rand_int = randint(3, 7)
            sleep(rand_int)

    return tmp

def get_job_ref_date(row):
    [import_date, job_reference_no, job_title, city, state, remote_possible, employment_type, job_posting_url, status, notes] = row
    tmp = {
        'import_date': import_date,
        'job_reference_no': job_reference_no,
        'job_title': job_title,
        'city': city,
        'state': state,
        'remote_possible': remote_possible,
        'employment_type': employment_type,
        'job_positing_url': job_posting_url,
        'status': status,
        'notes': notes,
    }
    return tmp

def load_previously_imported_jobs():
    with open('') as ref:
        data = [row for row in reader(ref)][1:]
        data = list(map(get_job_ref_date, data))
        return data


all_job_items_fetched = fetch_all_jobs()
previously_imported_jobs_path = ''
previously_imported_jobs_path_exists = path.exists(previously_imported_jobs_path)
previously_imported_jobs = load_previously_imported_jobs() if previously_imported_jobs_path_exists else []
previously_imported_jobs_len = len(previously_imported_jobs)
csv_write_mode = 'w'

def job_is_previously_imported(job_reference_no):
    if previously_imported_jobs_len > 0:
        for job_item in previously_imported_jobs:
            if job_item['job_reference_no'] == job_reference_no:
                return job_item
    tmp = {'job_reference_no': '', 'import_date': ''}
    return tmp

def status_check(row):
    seen = False
    for job_item in all_job_items_fetched:
        if row['job_reference_no'] == job_item['job_reference_no']:
            seen = True
    if not seen:
        row['status'] = 'DELISTED'
    return row