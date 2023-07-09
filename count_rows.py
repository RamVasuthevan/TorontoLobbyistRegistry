import sqlite3

def print_row_counts(db_path):
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    # Get list of all tables
    cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
    tables = cursor.fetchall()

    for table in tables:
        table_name = table[0]
        cursor.execute(f"SELECT COUNT(*) FROM {table_name};")
        count = cursor.fetchone()[0]
        print(f"Table: {table_name}, Rows: {count}")

    conn.close()

print_row_counts("app.sqlite")
