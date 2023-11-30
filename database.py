import psycopg2

conn_params = {
    'dbname': 'Flask',
    'user': 'kingsleyatuba',
    'password': '',
    'host': 'localhost'
}

def get_db_connection():
    return psycopg2.connect(**conn_params)
