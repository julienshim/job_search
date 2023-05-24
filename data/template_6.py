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