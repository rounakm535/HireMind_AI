import sqlite3

conn = sqlite3.connect(r"D:\Python\HireMind_AI\backend\hiremind_db.sqlite")
cursor = conn.cursor()

cursor.execute("DELETE FROM users")
conn.commit()

print("Deleted", cursor.rowcount)

conn.close()