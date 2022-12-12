import sqlite3

conn = sqlite3.connect('BotDataBase.db')
cursor = conn.cursor()
def table_create_projects(id: int, project_name: str):
    try:
        cursor.execute("INSERT INTO Projects(id, project_name, cost) VALUES (?,?, 1)", (id, project_name))
        conn.commit()
    except sqlite3.Error as Er:
        print("Ошибка1")
        return 'error'

def table_create_staff(id: int, name: str):
    try:
        cursor.execute("INSERT INTO staff(id, name, hour_cost) VALUES (?,?, 1)", (id, name))
        conn.commit()
    except sqlite3.Error as Er:
        print("Ошибка2")
        return 'error'

def table_update_staff_cost(id: str, hour_cost: int):
    try:
        cursor.execute("UPDATE staff SET hour_cost = ? where id = ?", (id, hour_cost))
        conn.commit()
    except sqlite3.Error as Er:
        print("Ошибка4")
        return 'error'

def table_update_projects_cost(id: int, cost: int):
    try:
        cursor.execute("UPDATE Projects SET cost =? where id =?", (id, cost))
        conn.commit()
    except sqlite3.Error as Er:
        print("Ошибка5")
        return 'error'

def db_table_selectAll():
    cursor.execute("SELECT * FROM Projects")
    row = cursor.fetchone()
    out = []
    while row is not None:
        i=1
        out.append(f"""\n        <tr><td>{i}</td> \n<td align="center">%s</td>""" % row[1])
        out.append("""\n        <td><228></td><td><228></td><td align="center">%s</td>\n<td><228></td>\n<td><228></td></tr>""" % row[2])
        row = cursor.fetchone()
    return ''.join(out)

def select_id_from_projects():
    cursor.execute("SELECT id FROM Projects")
    backkk = [*cursor.fetchall()]
    return backkk

def select_proj_name_from_projects_byid(id: int):
    cursor.execute("SELECT project_name FROM Projects WHERE id =?", (id,))
    backkk = cursor.fetchone()
    back2 = [backkk[0] for item in backkk]
    return str(back2).replace("['",'').replace("']",'')

def select_proj_cost_from_projects_byid(id: int):
    cursor.execute("SELECT cost FROM Projects WHERE id =?", (id,))
    backkk = cursor.fetchone()
    back2 = [backkk[0] for item in backkk]
    return str(back2).replace('[','').replace(']','')

def select_name_from_staff_byid(id: int):
    cursor.execute("SELECT name FROM staff where id = ?", (id,))
    backkk = cursor.fetchone()
    back2 = [backkk[0] for item in backkk]
    return str(back2).replace("['",'').replace("']",'')

def select_id_from_staff():
    cursor.execute("SELECT id FROM staff")
    backkk = [*cursor.fetchall()]
    return backkk

def select_cost_from_staff_byid(id: int):
    cursor.execute("SELECT hour_cost FROM staff where id = ?", (id,))
    backkk = cursor.fetchone()
    back2 = [backkk[0] for item in backkk]
    back2 = list(map(int, back2))
    return str(back2).replace('[','').replace(']','')

