import psycopg2
import json
import string
import datetime

def connect():

    # READ DATABASE CONNECTION INFORMATION FROM config.json
    json_file = open('config.json')
    schema = json.load(json_file)
    database_connection = schema['database_connection']


    # CREATE CONNECTION WITH POSTGRESQL SERVER DB
    conn = psycopg2.connect(
        host=database_connection['host'],
        database=database_connection['database'],
        user=database_connection['user'],
        password=database_connection['password'])

    return conn

# FUNCTION TO FILL etl_files TABLE
def fill_etl_files(conn, etl_files_table_data: list)-> None:

    cur = conn.cursor()
    # INSERTING DATA IN ETL_FILES TABLE
    # FOR EACH ROW IN TABLE RECORDS
    for row in etl_files_table_data:
        values = []
        # GATHER ROW VALUES
        for _, val in row.items():
            values.append('\'' + str(val) + '\'')

    # INSERT ROW VALUES
        cur.execute(
    f'''

    INSERT INTO edc_meta.etl_files(group_id, category, sub_category, file_name_mask, last_arrived_file, last_arrived_file_timestamp, 
    lwm, hwm, sla)
    VALUES
        ({
            ','.join(values)
        });

    ''' )

    cur.close()
    conn.commit()

# FUNCTION TO FILL etl_files_history TABLE
def fill_etl_files_history(conn, etl_files_history_table_data: list)-> None:

    cur = conn.cursor()

    # INSERTING DATA IN ETL_FILES_HISTORY TABLE TOO
    for row in etl_files_history_table_data:
        values = []

        for _, val in row.items():
            values.append('\'' + str(val) + '\'')
        cur.execute(
    f'''

    INSERT INTO edc_meta.etl_files_history(group_id, category, sub_category, file_name, file_arrival_date, available_per_sla)
    VALUES
        ({
            ','.join(values)
        });

    ''' )

    cur.close()
    conn.commit()

# EXECUTE PROCEDURE TO FILL etl_files_sumamry TABLE 
def execute_summary_procedure(conn)-> None:

    cur = conn.cursor()

    # READ PROCEDURE FROM sumamry_procedure.txt

    procedure_file = open('summary_procedure.txt', 'r')

    procedure = procedure_file.read()

    # EXECUTE SUMMARY PROCEDURE FROM summary_procedure.txt
    cur.execute(procedure)
    cur.execute('CALL sp_etl_files_summary()')

    cur.close()
    conn.commit()


# TRUNCATES ALL TABLES
def truncate_all(conn)-> None:

    cur = conn.cursor()
    cur.execute('truncate table edc_meta.etl_files')
    cur.execute('truncate table edc_meta.etl_files_history')
    cur.execute('truncate table edc_meta.etl_files_summary')
    cur.execute('drop table if exists stg_etl_files_summary')

    cur.close()
    conn.commit()

    conn.close()
    