import collections
import functools
import operator
from datetime import datetime as dt

import requests
import database as db


def get_list_project():
    response = requests.get(f"https://byuropink.aspro.cloud/api/v1/module/st/projects/"
                            f"list?api_key=WkN0a1hhQWc5NG5JNks3elFjZ1FYZlZpc2lLMHIyRVhfODgwOTY")
    data = response.json()
    entries_data = data['response']['items']
    for item in entries_data:
        db.table_create_projects(id=item['id'], project_name=item['name'])


def get_list_staff():
    response = requests.get(f"https://byuropink.aspro.cloud/api/v1/module/core/user/"
                            f"list?api_key=WkN0a1hhQWc5NG5JNks3elFjZ1FYZlZpc2lLMHIyRVhfODgwOTY")
    data = response.json()
    entries_data = data['response']['items']
    for item in entries_data:
        db.table_create_staff(id=item['id'], name=item['name'])


def get_task_list():
    entries_data = []
    for page in range(1, 20):
        response = requests.get(f'https://byuropink.aspro.cloud/api/v1/module/task/tasks/'
                                f'list?api_key=WkN0a1hhQWc5NG5JNks3elFjZ1FYZlZpc2lLMHIyRVhfODgwOTY&page={page}')
        data = response.json()
        entries_data += data['response']['items']
    return entries_data


def html_create_table_step_1(need_week: int):
    entries_data = get_task_list()
    selected_id_of_projects = db.select_id_from_projects()
    selected_id_of_staff = db.select_id_from_staff()
    project_summary_time_dict = {}
    project_summary_time_list_of_dict = []
    table_staff_list = []
    name_staff_list = []
    id_project_step_2 = 0
    id_staff_step_2 = 0
    plan_cost_staff = 0
    number_in_table = 0
    project_sum_proj = 0
    for id_of_staff in selected_id_of_staff:
        project_sum_time = 0
        cur_proj_sum_time = 0
        project_sum_task = 0
        for id_of_projects in selected_id_of_projects:
            for item in entries_data:
                if item['plan_start_date'] == '0000-00-00 00:00:00' or item['plan_start_date'] is None:
                    item['plan_start_date'] = None
                else:
                    plan_start_date = item['plan_start_date']
                    plan_start_date = dt.strptime(plan_start_date, '%Y-%m-%d %H:%M:%S')
                    plan_start_date = plan_start_date.isocalendar()[1]
                    if item['responsible_id'] == id_of_staff[0] and plan_start_date == need_week\
                            and item['model_id'] == id_of_projects[0]:
                        what = (id_of_projects[0])
                        id_staff_step_2 += what
                        project_sum_task += 1
                        cost_staff = db.select_cost_from_staff_byid(item['responsible_id'])
                        plan_cost_staff = int(cost_staff) * 40
                        fact_cost_staff = int(cost_staff)
                        name_staff_list = db.select_name_from_staff_byid(item['responsible_id'])
                        if item['time_estimate'] > 0:
                            project_sum_time += item['time_estimate']
                            cur_proj_sum_time += item['time_estimate']
                if item['plan_start_date'] == '0000-00-00 00:00:00' or item['plan_start_date'] is None:
                    item['plan_start_date'] = None
                else:
                    plan_start_date = item['plan_start_date']
                    plan_start_date = dt.strptime(plan_start_date, '%Y-%m-%d %H:%M:%S')
                    plan_start_date = plan_start_date.isocalendar()[1]
                    if project_sum_task >= 1 and item['responsible_id'] == id_of_staff[0]\
                            and plan_start_date == need_week and item['model_id'] == id_of_projects[0]:
                        id_staff_step_1 = id_of_projects[0]
                        id_project_step_2 += round(id_staff_step_2/id_staff_step_1)
                        id_staff_step_2 = 0
                        project_summary_time_dict[id_staff_step_1] = 0
                        if item['time_estimate'] > 0:
                            project_summary_time_dict[id_staff_step_1] += round(((cur_proj_sum_time % (168 * 3600))
                                                                                 / 3600)*fact_cost_staff)
            if id_project_step_2 == 1:
                project_sum_proj += 1
            if id_project_step_2 > 1:
                project_sum_proj += 1
            id_project_step_2 = 0
            cur_proj_sum_time = 0
        if project_sum_task != 0:
            project_summary_time_list_of_dict.append(project_summary_time_dict.copy())
            project_sum_time = (project_sum_time % (168 * 3600)) / 3600
            number_in_table += 1
            table_staff_list.append(
                f"""
                <tr>
                <td>{number_in_table}</td>
                <td>{name_staff_list}</td>
                <td>{project_sum_proj}</td>
                <td>{project_sum_task}</td>
                <td>{round(project_sum_time)}</td>
                <td>{fact_cost_staff*(round(project_sum_time))}</td>
                <td>{plan_cost_staff}</td>
                <td>{round(((fact_cost_staff*(round(project_sum_time)))/plan_cost_staff)*100)}%</td>
                </tr>""")
        project_sum_proj = 0
        project_summary_time_dict.clear()
    project_summary_time_dict = project_summary_time_list_of_dict
    project_summary_time_dict = functools.reduce(operator.add, map(collections.Counter, project_summary_time_dict))
    return ''.join(table_staff_list), project_summary_time_dict


def html_create_table_finall(need_week: int):
    entries_data = get_task_list()
    selected_id_of_projects = db.select_id_from_projects()
    table_projects = []
    table_staff = []
    number_in_table = 0
    html_projects, html_cost_proj = html_create_table_step_1(need_week)
    for resp in selected_id_of_projects:
        project_sum_time = 0
        project_sum_task = 0
        for item in entries_data:
            if item['plan_start_date'] == '0000-00-00 00:00:00' or item['plan_start_date'] is None:
                item['plan_start_date'] = None
            else:
                pn_st_dt = item['plan_start_date']
                pn_st_dt = dt.strptime(pn_st_dt, '%Y-%m-%d %H:%M:%S')
                pn_st_dt = pn_st_dt.isocalendar()[1]
                if item['model_id'] == resp[0] and pn_st_dt == need_week:
                    project_sum_task += 1
                    if item['time_estimate'] > 0:
                        project_sum_time += item['time_estimate']
        plan_cost = html_cost_proj[resp[0]]
        name_of_project = db.select_proj_name_from_projects_byid(resp[0])
        cost_of_project = db.select_proj_cost_from_projects_byid(resp[0])
        project_sum_time = (project_sum_time % (168 * 3600)) / 3600
        number_in_table += 1
        work_load = plan_cost/int(cost_of_project)
        table_projects.append(f"""<tr>
        <td>{number_in_table}</td>
        <td>{name_of_project}</td>
        <td>{project_sum_task}</td>
        <td>{round(project_sum_time)}</td>
        <td>{cost_of_project}</td>
        <td>{plan_cost}</td>
        <td>{round(work_load*100)}%</td>
        </tr>""")
    table_staff.append(html_projects)
    return ''.join(table_projects), ''.join(table_staff)
