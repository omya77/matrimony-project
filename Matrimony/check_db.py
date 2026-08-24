import sqlite3

conn = sqlite3.connect('db.sqlite3')
cursor = conn.cursor()

print("Tables and Rows:")
cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
tables = cursor.fetchall()
for t in tables:
    if not t[0].startswith('django_') and not t[0].startswith('auth_permission'):
        try:
            cursor.execute(f"SELECT COUNT(*) FROM {t[0]}")
            count = cursor.fetchone()[0]
            print(f"- {t[0]}: {count} rows")
        except:
            pass
conn.close()
