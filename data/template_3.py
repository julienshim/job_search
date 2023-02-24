from requests import request
from bs4 import BeautifulSoup
from time import sleep
from random import randint
from csv import writer, reader
from datetime import datetime
from os import path


def get_soup(page_number):
    url = f""

    payload={}
    headers = {}

    response = request('GET', url, headers=headers, data=payload)
    soup = BeautifulSoup(response.text, 'html.parser')
    return soup

def parse_inline_text(inline_text):
    return inline_text.string

def parse_job_item(job_item):
    job_link = f""
    job_reference = job_item['href'].split('/')[2]
    job_title = job_item.find('h2', class_='h6').string
    location = job_item.find('span', class_='location').string
    remote_possible = job_item.find('span', class_='remote') is not None
    is_tagged_new = job_item.find('span', id=f'new-label-{job_reference}') is not None
    job_item_dict = {
        'job_title': job_title.strip(),
        'job_link': job_link.strip(),
        'job_reference': job_reference.strip(),
        'location': location.strip(),
        'remote_possible': remote_possible,
        'is_tagged_new': is_tagged_new
    }
    return job_item_dict

def fetch_all_jobs():
    running = True
    current_page_number = 1
    tmp = []

    while running:
        soup = get_soup(current_page_number)
        job_items = soup.find_all('a', class_='job-item')
        job_items_parsed = list(map(parse_job_item, job_items))
        job_items_parsed_len = len(job_items_parsed)

        if job_items_parsed_len == 0:
            running = False
        else:
            print(f'Fetching Page {current_page_number} jobs... {job_items_parsed_len} jobs found')
            tmp += job_items_parsed
            current_page_number += 1
            rand_num = randint(3, 7)
            sleep(rand_num)

    return tmp

def get_job_ref_date(row):
    [import_date, job_reference_no, job_title, location, remote_possible, job_posting_url, is_tagged_new, status, notes] = row
    tmp = {
        'job_reference_no': job_reference_no,
        'import_date': import_date
    }
    return tmp


def load_previously_imported_jobs():
    with open('') as ref:
        data = [row for row in reader(ref)][1:]
        data = list(map(get_job_ref_date, data))
        return data