import collections
import functools
import operator
from datetime import datetime as dt

import requests
import database as db


def get_projects():
    response = requests.get(f"https://byuropink.aspro.cloud/api/v1/module/st/projects/"
                            f"list?api_key=WkN0a1hhQWc5NG5JNks3elFjZ1FYZlZpc2lLMHIyRVhfODgwOTY")
    data = response.json()
    entries_data = data['response']['items']
    for item in entries_data:
        db.insert_projects(id=item['id'], project_name=item['name'])


def get_staff():
    response = requests.get(f"https://byuropink.aspro.cloud/api/v1/module/core/user/"
                            f"list?api_key=WkN0a1hhQWc5NG5JNks3elFjZ1FYZlZpc2lLMHIyRVhfODgwOTY")
    data = response.json()
    entries_data = data['response']['items']
    for item in entries_data:
        db.insert_staff(id=item['id'], name=item['name'])


def get_task():
    entries_data = []
    for page in range(1, 30):
        response = requests.get(f'https://byuropink.aspro.cloud/api/v1/module/task/tasks/'
                                f'list?api_key=WkN0a1hhQWc5NG5JNks3elFjZ1FYZlZpc2lLMHIyRVhfODgwOTY&page={page}')
        data = response.json()
        entries_data += data['response']['items']
    return entries_data


def html_get_staff(need_week: int):
    entries_data = get_task()
    selected_projects_id = db.select_projects_id()
    selected_staff_id = db.select_id_staff()
    project_time_dict = {}
    project_time_list_of_dict = []
    name_staff = []
    staff = []
    staff_procent = []
    enum_staff = 0
    count_certain_project_task = 0
    sum_id_for_divide = 0
    plan_cost_staff = 0
    for staff_id in selected_staff_id:
        project_time = 0
        certain_project_time = 0
        project_tasks = 0
        for projects_id in selected_projects_id:
            for item in entries_data:
                if item['plan_start_date'] == '0000-00-00 00:00:00' or item['plan_start_date'] is None:
                    item['plan_start_date'] = None
                else:
                    plan_start_date = item['plan_start_date']
                    plan_start_date = dt.strptime(plan_start_date, '%Y-%m-%d %H:%M:%S')
                    plan_start_date = plan_start_date.isocalendar()[1]
                    if item['responsible_id'] == staff_id[0] and plan_start_date == need_week \
                            and item['model_id'] == projects_id[0]:
                        sum_id_for_divide += projects_id[0]
                        project_tasks += 1
                        cost_staff = db.select_staff_cost_byid(item['responsible_id'])
                        plan_cost_staff = int(cost_staff) * 40
                        fact_cost_staff = int(cost_staff)
                        name_staff = db.select_name_staff_byid(item['responsible_id'])
                        if item['time_estimate'] > 0:
                            project_time += item['time_estimate']
                            certain_project_time += item['time_estimate']
                if item['plan_start_date'] == '0000-00-00 00:00:00' or item['plan_start_date'] is None:
                    item['plan_start_date'] = None
                else:
                    plan_start_date = item['plan_start_date']
                    plan_start_date = dt.strptime(plan_start_date, '%Y-%m-%d %H:%M:%S')
                    plan_start_date = plan_start_date.isocalendar()[1]
                    if project_tasks >= 1 and item['responsible_id'] == staff_id[0] \
                            and plan_start_date == need_week and item['model_id'] == projects_id[0]:
                        certain_project_id = projects_id[0]
                        count_certain_project_task += round(sum_id_for_divide / certain_project_id)
                        sum_id_for_divide = 0
                        project_time_dict[certain_project_id] = 0
                        if item['time_estimate'] > 0:
                            project_time_dict[certain_project_id] += round(((certain_project_time % (168 * 3600))
                                                                            / 3600) * fact_cost_staff)
            count_certain_project_task = 0
            certain_project_time = 0
        if project_tasks != 0:
            project_time_list_of_dict.append(project_time_dict.copy())
            project_time = (project_time % (168 * 3600)) / 3600
            workload_staff = round(((fact_cost_staff * (round(project_time))) / plan_cost_staff) * 100)
            staff_procent.append(workload_staff)
            enum_staff += 1
            if (enum_staff % 2) == 0:
                color = '#2f3232'
            elif (enum_staff % 2) == 1:
                color = '#232525'
            staff.append(
                f"""
                <tr bgcolor = "{color}">
                <td>{name_staff}</td>
                <td>{round(project_time)}</td>
                <td>{fact_cost_staff * (round(project_time))}</td>
                <td>{workload_staff}%</td>
                </tr>""")
        project_time_dict.clear()
    project_time_dict = project_time_list_of_dict
    project_time_dict = functools.reduce(operator.add, map(collections.Counter, project_time_dict))
    zip_staff_sorted = zip(staff_procent, staff)
    dict_staff_sorted = dict(zip_staff_sorted)
    dict_staff_sorted = {k: v for k, v in sorted(dict_staff_sorted.items(), reverse=True, key=lambda x: x[0])}
    staff = dict_staff_sorted.values()
    return ''.join(staff), project_time_dict


def html_get_projects(need_week: int):
    entries_data = get_task()
    selected_projects_id = db.select_projects_id()
    projects = []
    staff = []
    project_load_procent = []
    enumproject = 0
    html_projects, html_project_cost = html_get_staff(need_week)
    for projects_id in selected_projects_id:
        project_time = 0
        project_tasks = 0
        for item in entries_data:
            if item['plan_start_date'] == '0000-00-00 00:00:00' or item['plan_start_date'] is None:
                item['plan_start_date'] = None
            else:
                plan_start_date = item['plan_start_date']
                plan_start_date = dt.strptime(plan_start_date, '%Y-%m-%d %H:%M:%S')
                plan_start_date = plan_start_date.isocalendar()[1]
                if item['model_id'] == projects_id[0] and plan_start_date == need_week:
                    project_tasks += 1
                    if item['time_estimate'] > 0:
                        project_time += item['time_estimate']
        fact_cost = html_project_cost[projects_id[0]]
        project_name = db.select_project_name_byid(projects_id[0])
        plan_cost = db.select_project_cost_byid(projects_id[0])
        project_time = (project_time % (168 * 3600)) / 3600
        work_load = round((fact_cost / int(plan_cost)) * 100)
        if project_time != 0:
            enumproject += 1
            project_load_procent.append(work_load)
            if (enumproject % 2) == 0:
                color = '#2f3232'
            elif (enumproject % 2) == 1:
                color = '#232525'
            projects.append(
                f"""
                <tr bgcolor="{color}">
                <td>{project_name}</td>
                <td>{round(project_time)}</td>
                <td>{fact_cost}</td>
                <td>{work_load}%</td>
                </tr>""")
    staff.append(html_projects)
    zip_project_sorted = zip(project_load_procent, projects)
    dict_project_sorted = dict(zip_project_sorted)
    dict_project_sorted = {k: v for k, v in sorted(dict_project_sorted.items(), reverse=True, key=lambda x: x[0])}
    projects = dict_project_sorted.values()
    return ''.join(projects), ''.join(staff)
