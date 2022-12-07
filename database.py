import sqlite3

conn = sqlite3.connect('BotDataBase.db')
cursor = conn.cursor()
def table_create_projects(id: int, project_name: str):
    try:
        cursor.execute("INSERT INTO Projects(id, project_name) VALUES (?,?)", (id, project_name))
        conn.commit()
    except sqlite3.Error as Er:
        print("Ошибка1")
        return 'error'

def table_create_staff(id: int, name: str):
    try:
        cursor.execute("INSERT INTO staff(id, name) VALUES (?,?)", (id, name))
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
    article = cursor.fetchone()
    out = []
    while article is not None:
        out.append("%s" % article)
        article = cursor.fetchone()
    return ' '.join(out)
