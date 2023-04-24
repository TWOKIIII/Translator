import sqlite3
con = sqlite3.connect('TranslatorBase.db')
cur = con.cursor()
cur.execute('''CREATE TABLE users (id VARCHAR(255), lang VARCHAR(255))''')
