import json
import datetime
import time
from datetime import datetime as dattime

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
    entries = []
    for page in range(1,20):
        response = requests.get(f'https://byuropink.aspro.cloud/api/v1/module/task/tasks/list?api_key=WkN0a1hhQWc5NG5JNks3elFjZ1FYZlZpc2lLMHIyRVhfODgwOTY&page={page}')
        data = response.json()
        entries += data['response']['items']
    return entries

def tasks_reader2():
    entries = tasks_reader()
    curid = db.select_id_from_projects()
    nameproj = []
    for resp in curid:
        project_sum_time = 0
        project_sum_task = 0
        for item in entries:
            if item['plan_start_date'] == '0000-00-00 00:00:00' or item['plan_start_date'] == None:
                item['plan_start_date'] = None
            else:
                pn_st_dt = item['plan_start_date']
                pn_st_dt = dattime.strptime(pn_st_dt, '%Y-%m-%d %H:%M:%S')
                pn_st_dt = pn_st_dt.isocalendar()[1]
                this_dat = datetime.datetime.now()
                this_week = this_dat.isocalendar()[1]
                if item['model_id'] == resp[0] and pn_st_dt == this_week:
                    project_sum_task += 1
                    if item['time_estimate'] > 0:
                        project_sum_time += item['time_estimate']
        nameproj=db.select_proj_name_from_projects_byid(resp[0])
        print(resp[0])
        print(nameproj)
        print(f'sum task: {project_sum_task}')
        project_sum_time = (project_sum_time % (168 * 3600)) / 3600
        print(f'sum time: {project_sum_time}')
def task_reader3():
    entries = tasks_reader()
    curid = db.select_id_from_projects()
    idstaff = db.select_id_from_staff()
    namestaff = []
    nameproj = []
    for resp in curid:
        for resp2 in idstaff:
            project_sum_time = 0
            project_sum_task = 0
            for item in entries:
                if item['plan_start_date'] == '0000-00-00 00:00:00' or item['plan_start_date'] == None:
                    item['plan_start_date'] = None
                else:
                    pn_st_dt = item['plan_start_date']
                    pn_st_dt = dattime.strptime(pn_st_dt, '%Y-%m-%d %H:%M:%S')
                    pn_st_dt = pn_st_dt.isocalendar()[1]
                    this_dat = datetime.datetime.now()
                    this_week = this_dat.isocalendar()[1]
                    if item['responsible_id'] == resp2[0] and pn_st_dt == this_week and item['model_id'] == resp[0]:
                        project_sum_task += 1
                        nameproj = db.select_proj_name_from_projects_byid(item['model_id'])
                        namestaff = db.select_name_from_staff_byid(item['responsible_id'])
                        if item['time_estimate'] > 0 and item:
                            project_sum_time += item['time_estimate']
            if project_sum_task != 0:
                print(nameproj)
                print(namestaff)
                print(f'sum task: {project_sum_task}')
                project_sum_time = (project_sum_time % (168 * 3600)) / 3600
                print(f'sum time: {project_sum_time}')
