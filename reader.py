import json
from datetime import datetime

import requests
import database as db

def project_reader():
    response = requests.get(f"https://byuropink.aspro.cloud/api/v1/module/st/projects/list?api_key=WkN0a1hhQWc5NG5JNks3elFjZ1FYZlZpc2lLMHIyRVhfODgwOTY")
    data = response.json()
    entries = data['response']['items']
    for item in entries:
        db.table_create_projects(id=item['id'], project_name=item['name'])

def staff_reader():
    response = requests.get(f"https://byuropink.aspro.cloud/api/v1/module/core/user/list?api_key=WkN0a1hhQWc5NG5JNks3elFjZ1FYZlZpc2lLMHIyRVhfODgwOTY")
    data = response.json()
    entries = data['response']['items']
    for item in entries:
        db.table_create_staff(id=item['id'], name=item['name'])

def project_costs_reader():
    response = requests.get(f"https://byuropink.aspro.cloud/api/v1/module/st/projects/list?api_key=WkN0a1hhQWc5NG5JNks3elFjZ1FYZlZpc2lLMHIyRVhfODgwOTY")
    data = response.json()
    entries = data['response']['items']
    for item in entries:
        db.table_create_projects(id=item['id'], project_name=item['name'])

def tasks_reader():
    project_sum_task = 0;
    project_sum_time = 0;
    for page in range(1,20):
        print(page)
        response = requests.get(f'https://byuropink.aspro.cloud/api/v1/module/task/tasks/list?api_key=WkN0a1hhQWc5NG5JNks3elFjZ1FYZlZpc2lLMHIyRVhfODgwOTY&page={page}')
        data = response.json()
        entries = data['response']['items']
        for item in entries:
            if item['plan_start_date'] == '0000-00-00 00:00:00':
                item['plan_start_date'] = None
            pn_st_dt = item['plan_start_date']
            pn_st_dt = datetime.strptime(pn_st_dt, '%Y-%m-%d %H:%M:%S')
            print(datetime.now().isocalendar()[1])
            print(pn_st_dt)
            if item['model_id'] == 8 &  pn_st_dt.isocalendar()[1] == f'{datetime.now().isocalendar()[1]}':
                print('yes model')
                project_sum_task += 1
                if item['time_estimate'] > 0:
                    project_sum_time += item['time_estimate']
                    print('yes_time')
            emae = item['model_id'], item['id'], item['name'], item['responsible_id'], item['plan_start_date'],  item['time_estimate']
    print(project_sum_task)
    print(project_sum_time)