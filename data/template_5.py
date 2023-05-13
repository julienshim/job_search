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

    if 'jobs' in response_json:
        jobs_found = response_json['jobs']
        return jobs_found
    return []

def fetch_seed_body():
    with open('../csv/seed.csv') as csv_input:
        data = [row for row in reader(csv_input)]
        data_header = data[0]
        data_body = data[1:]
        return data_body
    
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
    [import_date, company_name, permalink, status, formType, atsSourcePlatform, atsSourceId, title, content, location, office, team, department, offices, departments, workType, publicUrl, postedAt, jobBoard, shareTemplates, publicUnfurlImageUrl, publicShareableUrl, status, notes] = row
    tmp = {
        'job_reference_no': atsSourceId,
        'job_company_name': company_name,
        'import_date': import_date
    }
    return tmp

def load_previously_imported_jobs():
    with open('./results/template5.csv') as ref:
        data = [row for row in reader(ref)][1:]
        data = list(map(get_job_ref_data, data))
        return data

previously_imported_jobs_path = './results/template5.csv'
previously_imported_jobs_path_exists = path.exists(previously_imported_jobs_path)
previously_imported_jobs = load_previously_imported_jobs() if previously_imported_jobs_path_exists else []
previously_imported_jobs_len = len(previously_imported_jobs)
all_target_keys = get_target_keys(all_job_items_fetched)
csv_write_mode = 'a' if previously_imported_jobs_path_exists else 'w'

def job_is_previously_imported(job_reference_no, job_company_name):
    if previously_imported_jobs_len > 0:
        for job_item in previously_imported_jobs:
            if job_item['job_reference_no'] == job_reference_no and job_item['job_company_name'] == job_company_name:
                return job_item
    tmp = {'job_reference_no': '', 'import_date': ''}
    return tmp

def sanitize_content(output_value):
    for item in [
        ('&lt;', '<'),
        ('&gt;', '>'),
        ('(<([^>]+)>)', '\n'),
        ('&NewLine;', '\n'),
        ('\n{1,}', '\n'),
        ('&comma;', ','),
        ('&CloseCurlyQuote;', '’')
        # ('&amp;', '&')
    ]:
        output_value = sub(item[0], item[1], output_value)
    return output_value

with open(previously_imported_jobs_path, csv_write_mode, encoding='utf-8') as tempalte5_csv:
    csv_writer = writer(tempalte5_csv)

    if csv_write_mode == 'w':
        csv_writer.writerow(['import_date', 'company_name'] + all_target_keys + ['status', 'notes'])

    jobs_written_count = 0
    jobs_skipped_count = 0

    for company_name in all_job_items_fetched:
        for job in all_job_items_fetched[company_name]:
            job_reference_no = job['atsSourceId']
            job_company_name = company_name
            import_date = datetime.today().strftime('%Y-%m-%d')
            job_item_row = [import_date, company_name]

            for target_key in all_target_keys:
                output_value = ''
                if target_key in job:
                    key_value = job[target_key]
                    if target_key in ['content']:
                        key_value = sanitize_content(key_value)
                    output_value = key_value
                job_item_row.append(str(output_value))
            
            job_item_row += ['', '']

            import_status = job_is_previously_imported(job_reference_no, job_company_name)
            import_job_reference_no = import_status["job_reference_no"]
            import_import_date = import_status["import_date"]

            if import_job_reference_no and import_import_date:
                jobs_skipped_count += 1
            else: 
                csv_writer.writerow(job_item_row)
                jobs_written_count += 1
        
        print(f'{jobs_written_count} new {job_company_name} jobs added.')

print('Done!')
