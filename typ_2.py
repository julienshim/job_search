from datetime import datetime, timedelta
from requests import request
from bs4 import BeautifulSoup

def get_date_n_weeks_ago():
    today = datetime.now()
    delta = timedelta(weeks=1)
    n_weeks_ago = today - delta
    return n_weeks_ago

def get_soup(page_number):
    print(f'Fetching Page {page_number} jobs...')
    url = f'https://unamed.com/page/{page_number}'

    payload={}
    headers={}

    response = request('GET', url, headers=headers, data=payload)
    soup = BeautifulSoup(response.text, 'html.parser')
    return soup

def get_seconds(job_link):
    
    payload={}
    headers={}

    response = request('GET', job_link, headers=headers, data=payload)
    response_txt = response.text
    job_id = job_link.split('/')[-1]
    with open(f'./html/unamed/{job_id}.html', 'w') as output_file:
        output_file.write(response_txt)