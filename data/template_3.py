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