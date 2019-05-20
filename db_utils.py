import sqlite3

def get_db_conn(sqlite_file='arxoid_db.sqlite'):
    return sqlite3.connect(sqlite_file)

def get_conn_cursor(conn):
    return conn.cursor()


table_name1 = 'my_table_1'  # name of the table to be created
table_name2 = 'my_table_2'  # name of the table to be created
new_field = 'my_1st_column' # name of the column
field_type = 'INTEGER'  # column data type

def create_table(query):
    conn = get_db_conn()
    cur = get_conn_cursor(conn)
    cur.execute('CREATE TABLE {}'.format(query))
    conn.commit()
    conn.close()
    return True

def insert_into_table(table_name, values):
    conn = get_db_conn()
    cur = get_conn_cursor(conn)
    cur.execute('INSERT INTO {} (id, filtered_question, filtered_answer) VALUES(null, ?, ?);'.format(table_name), values)
    conn.commit()
    conn.close()
    return True