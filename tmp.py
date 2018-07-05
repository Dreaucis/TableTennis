import sqlite3


db = sqlite3.connect('table_tennis.db')
cursor = db.cursor()

cursor.execute("""
CREATE TABLE IF NOT EXISTS users(
id INTEGER,
name STRING,
password STRING
)
""")

#cursor.execute("""INSERT INTO users(id,name,password) VALUES(2,'hst','ap')""")

ranks = cursor.execute(""" SELECT id FROM users WHERE name IN (?,?) """,('hst','hest')).fetchall()

print(ranks)