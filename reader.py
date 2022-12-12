import collections
import functools
import json
import datetime
import operator
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

def tasks_reader2(need_week: int):
    entries = tasks_reader()
    curid = db.select_id_from_projects()
    nameproj = []
    costproj = []
    modeif = []
    numberinmass = 0
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
                if item['model_id'] == resp[0] and pn_st_dt == need_week:
                    project_sum_task += 1
                    if item['time_estimate'] > 0:
                        project_sum_time += item['time_estimate']
        nameproj=db.select_proj_name_from_projects_byid(resp[0])
        costproj=db.select_proj_cost_from_projects_byid(resp[0])
        project_sum_time = (project_sum_time % (168 * 3600)) / 3600
        numberinmass += 1
        modeif.append(f"""<tr><td>{numberinmass}</td><td>{nameproj}</td><td>{project_sum_task}</td><td>{round(project_sum_time)}</td><td>{costproj}</td><td>{22}</td><td>{costproj}</td></tr>""")
    return ''.join(modeif)

def task_reader3(need_week: int):
    entries = tasks_reader()
    curid = db.select_id_from_projects()
    idstaff = db.select_id_from_staff()
    namestaff = []
    projsumtime = {}
    projsumtime2 = []
    who2 = 0
    what2 = 0
    plan_coststaff = 0
    modeif = []
    numberinmass = 0
    project_sum_proj = 0
    for resp2 in idstaff:
        project_sum_time = 0
        cur_proj_sum_time = 0
        project_sum_task = 0
        for resp in curid:
            for item in entries:
                if item['plan_start_date'] == '0000-00-00 00:00:00' or item['plan_start_date'] == None:
                    item['plan_start_date'] = None
                else:
                    pn_st_dt = item['plan_start_date']
                    pn_st_dt = dattime.strptime(pn_st_dt, '%Y-%m-%d %H:%M:%S')
                    pn_st_dt = pn_st_dt.isocalendar()[1]
                    if item['responsible_id'] == resp2[0] and pn_st_dt == need_week and item['model_id'] == resp[0]:
                        what = (resp[0])
                        what2 += what
                        project_sum_task += 1
                        coststaff = db.select_cost_from_staff_byid(item['responsible_id'])
                        plan_coststaff = int(coststaff) * 40
                        fact_coststaff = int(coststaff)
                        namestaff = db.select_name_from_staff_byid(item['responsible_id'])
                        if item['time_estimate'] > 0:
                            project_sum_time += item['time_estimate']
                            cur_proj_sum_time += item['time_estimate']
                if item['plan_start_date'] == '0000-00-00 00:00:00' or item['plan_start_date'] == None:
                    item['plan_start_date'] = None
                else:
                    pn_st_dt = item['plan_start_date']
                    pn_st_dt = dattime.strptime(pn_st_dt, '%Y-%m-%d %H:%M:%S')
                    pn_st_dt = pn_st_dt.isocalendar()[1]
                    if project_sum_task >= 1 and item['responsible_id'] == resp2[0] and pn_st_dt == need_week and item['model_id'] == resp[0]:
                        who = resp[0]
                        who2 += round(what2/who)
                        what2=0
                        projsumtime[who] = 0
                        if item['time_estimate'] > 0:
                            projsumtime[who]+=round(((cur_proj_sum_time % (168 * 3600)) / 3600)*fact_coststaff)
            if who2 == 1:
                project_sum_proj += 1
            if who2 > 1:
                project_sum_proj += 1
            who2=0
            cur_proj_sum_time = 0
        if project_sum_task != 0:
            projsumtime2.append(projsumtime.copy())
            print(projsumtime)
            project_sum_time = (project_sum_time % (168 * 3600)) / 3600
            numberinmass += 1
            modeif.append(
                f"""<tr><td>{numberinmass}</td><td>{namestaff}</td><td>{project_sum_proj}</td><td>{project_sum_task}</td><td>{round(project_sum_time)}</td><td>{fact_coststaff*(round(project_sum_time))}</td><td>{plan_coststaff}</td><td>{round(((fact_coststaff*(round(project_sum_time)))/plan_coststaff)*100)}%</td></tr>""")
        project_sum_proj = 0
        projsumtime.clear()
    projsumtime = projsumtime2
    projsumtime = functools.reduce(operator.add, map(collections.Counter, projsumtime))
    print(projsumtime)
    return ''.join(modeif)