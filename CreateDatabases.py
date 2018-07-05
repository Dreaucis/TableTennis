import sqlite3

db = sqlite3.connect('table_tennis.db')

cursor = db.cursor()

# Creating players table
cursor.execute("""
CREATE TABLE IF NOT EXISTS players(
id INTEGER,
name STRING,
password STRING
)
""")

# Creating game history table
cursor.execute("""
CREATE TABLE IF NOT EXISTS games(
id INTEGER,
id_player_1 INTEGER,
id_player_2 INTEGER,
score_player_1 INTEGER,
score_player_2 INTEGER
)
""")

# Creating ladder table
cursor.execute("""
CREATE TABLE IF NOT EXISTS ladder(
player_id INTEGER,
rank INTEGER
""")

