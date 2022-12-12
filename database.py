import sqlite3

conn = sqlite3.connect('BotDataBase.db')
cursor = conn.cursor()


def table_create_projects(id: int, project_name: str):
    try:
        cursor.execute("INSERT INTO Projects(id, project_name, cost) VALUES (?,?, 1)", (id, project_name))
        conn.commit()
    except sqlite3.Error as Er:
        print("Нет возможности внесения информации в таблицу проектов")
        return 'error'


def table_create_staff(id: int, name: str):
    try:
        cursor.execute("INSERT INTO staff(id, name, hour_cost) VALUES (?,?, 1)", (id, name))
        conn.commit()
    except sqlite3.Error as Er:
        print("Нет возможности внесения информации в таблицу сотрудников")
        return 'error'


def table_update_staff_cost(id: str, hour_cost: int):
    try:
        cursor.execute("UPDATE staff SET hour_cost = ? where id = ?", (id, hour_cost))
        conn.commit()
    except sqlite3.Error as Er:
        print("Нет возможности обновления базы данных по сотрудникам")
        return 'error'


def table_update_projects_cost(id: int, cost: int):
    try:
        cursor.execute("UPDATE Projects SET cost =? where id =?", (id, cost))
        conn.commit()
    except sqlite3.Error as Er:
        print("Нет возможности обновления базы данных по проектам")
        return 'error'


def select_id_from_projects():
    cursor.execute("SELECT id FROM Projects")
    selected_data = [*cursor.fetchall()]
    return selected_data


def select_proj_name_from_projects_byid(id: int):
    cursor.execute("SELECT project_name FROM Projects WHERE id =?", (id,))
    selected_data_step_1 = cursor.fetchone()
    selected_data_step_2 = [selected_data_step_1[0] for item in selected_data_step_1]
    return str(selected_data_step_2).replace("['", '').replace("']", '')


def select_proj_cost_from_projects_byid(id: int):
    cursor.execute("SELECT cost FROM Projects WHERE id =?", (id,))
    selected_data_step_1 = cursor.fetchone()
    selected_data_step_2 = [selected_data_step_1[0] for item in selected_data_step_1]
    return str(selected_data_step_2).replace('[','').replace(']','')


def select_name_from_staff_byid(id: int):
    cursor.execute("SELECT name FROM staff where id = ?", (id,))
    selected_data_step_1 = cursor.fetchone()
    selected_data_step_2 = [selected_data_step_1[0] for item in selected_data_step_1]
    return str(selected_data_step_2).replace("['", '').replace("']", '')


def select_id_from_staff():
    cursor.execute("SELECT id FROM staff")
    selected_data = [*cursor.fetchall()]
    return selected_data


def select_cost_from_staff_byid(id: int):
    cursor.execute("SELECT hour_cost FROM staff where id = ?", (id,))
    selected_data_step_1 = cursor.fetchone()
    selected_data_step_2 = [selected_data_step_1[0] for item in selected_data_step_1]
    selected_data_step_2 = list(map(int, selected_data_step_2))
    return str(selected_data_step_2).replace('[', '').replace(']', '')

