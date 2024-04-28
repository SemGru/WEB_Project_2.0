import sqlite3

DB = sqlite3.connect('DB/test_web.db')
# таблица Task
# number
#
SQL = DB.cursor()

a = 1
b = '/static/img/1267.gif'
# SQL.execute("""DELETE from task where number = 4""")
print(SQL.execute(f"SELECT * FROM Task").fetchall())
# SQL.execute(f"INSERT INTO Task Values (?, ?)", (a, b))
DB.commit()
