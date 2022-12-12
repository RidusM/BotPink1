import sqlite3

conn = sqlite3.connect('BotDataBase.db')
cursor = conn.cursor()


def insert_projects(id: int, project_name: str):
    try:
        cursor.execute("INSERT INTO Projects(id, project_name, cost) VALUES (?,?, 1)", (id, project_name))
        conn.commit()
    except sqlite3.Error:
        print("Нет возможности внесения информации в таблицу проектов")
        return 'error'


def insert_staff(id: int, name: str):
    try:
        cursor.execute("INSERT INTO staff(id, name, hour_cost) VALUES (?,?, 1)", (id, name))
        conn.commit()
    except sqlite3.Error:
        print("Нет возможности внесения информации в таблицу сотрудников")
        return 'error'


def update_staff_cost(id: str, hour_cost: int):
    try:
        cursor.execute("UPDATE staff SET hour_cost = ? where id = ?", (id, hour_cost))
        conn.commit()
    except sqlite3.Error:
        print("Нет возможности обновления базы данных по сотрудникам")
        return 'error'


def update_projects_cost(id: int, cost: int):
    try:
        cursor.execute("UPDATE Projects SET cost =? where id =?", (id, cost))
        conn.commit()
    except sqlite3.Error:
        print("Нет возможности обновления базы данных по проектам")
        return 'error'


def select_projects_id():
    cursor.execute("SELECT id FROM Projects")
    selected_data_list = [*cursor.fetchall()]
    return selected_data_list


def select_project_name_byid(id: int):
    cursor.execute("SELECT project_name FROM Projects WHERE id =?", (id,))
    select_data = cursor.fetchone()
    selected_data_list = [select_data[0] for _ in select_data]
    return str(selected_data_list).replace("['", '').replace("']", '')


def select_project_cost_byid(id: int):
    cursor.execute("SELECT cost FROM Projects WHERE id =?", (id,))
    select_data = cursor.fetchone()
    selected_data_list = [select_data[0] for _ in select_data]
    return str(selected_data_list).replace('[', '').replace(']', '')


def select_name_staff_byid(id: int):
    cursor.execute("SELECT name FROM staff where id = ?", (id,))
    select_data = cursor.fetchone()
    selected_data_list = [select_data[0] for _ in select_data]
    return str(selected_data_list).replace("['", '').replace("']", '')


def select_id_staff():
    cursor.execute("SELECT id FROM staff")
    selected_data_list = [*cursor.fetchall()]
    return selected_data_list


def select_staff_cost_byid(id: int):
    cursor.execute("SELECT hour_cost FROM staff where id = ?", (id,))
    select_data = cursor.fetchone()
    selected_data_list = [select_data[0] for _ in select_data]
    selected_data_list = list(map(int, selected_data_list))
    return str(selected_data_list).replace('[', '').replace(']', '')
