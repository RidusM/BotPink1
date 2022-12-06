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
        db.table_create_projects_cost(id=item['id'], project_name=item['name'])

def tasks_reader():
    response = requests.get(f"https://byuropink.aspro.cloud/api/v1/module/task/tasks/list?api_key=WkN0a1hhQWc5NG5JNks3elFjZ1FYZlZpc2lLMHIyRVhfODgwOTY")
    data = response.json()
    entries = data['response']['items']
    for item in entries:
        print(item['model_id'], item['id'], item['name'], item['responsible_id'], item['plan_start_date'],  item['time_estimate'])