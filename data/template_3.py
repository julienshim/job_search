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

all_job_items_fetched = fetch_all_jobs()
previously_imported_jobs_path = ''
previously_imported_jobs_path_exists = path.exists(previously_imported_jobs_path)
previously_imported_jobs = load_previously_imported_jobs() if previously_imported_jobs_path_exists else []
previously_imported_jobs_len = len(previously_imported_jobs)
csv_write_mode = 'a' if previously_imported_jobs_path_exists else 'w'


def job_is_previously_imported(job_reference_no):
    if previously_imported_jobs_len > 0:
        for job_item in previously_imported_jobs:
            if job_item['job_reference_no'] == job_reference_no:
                return job_item
    tmp = {'job_reference_no': '', 'import_date': ''}
    return tmp

with open(previously_imported_jobs_path, csv_write_mode, encoding='utf-8') as f:
    csv_writer = writer(f)
    if csv_write_mode == 'w':
        csv_writer.writerow(['import_date', 'job_reference_no', 'job_title', 'location', 'remote_possible', 'job_posting_url', 'is_tagged_new', 'status', 'notes'])

    jobs_written_count = 0
    jobs_skipped_count = 0

    for job_item in all_job_items_fetched:
        job_title = job_item['job_title']
        job_posting_url = job_item['job_link']
        job_reference_no = job_item['job_reference']
        location = job_item['location']
        remote_possible = job_item['remote_possible']
        is_tagged_new = job_item['is_tagged_new']
        import_date = datetime.today().strftime('%Y-%m-%d')

        import_status = job_is_previously_imported(job_reference_no)
        import_job_reference_no = import_status["job_reference_no"]
        import_import_date = import_status["import_date"]

        if import_job_reference_no and import_import_date:
            jobs_skipped_count += 1
        else:
            job_item_row = [import_date, job_reference_no, job_title, location, remote_possible, job_posting_url, is_tagged_new, '', '']
            csv_writer.writerow(job_item_row)
            jobs_written_count += 1

    print(f'Done! {jobs_written_count} new jobs added.')
