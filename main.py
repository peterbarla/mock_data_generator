import json
from metadata_analyzer import analyze
from mock_data_generator import generate_mock_data
from db_commands import *
import sys
import random

# CHECK IF ARGUMENT WAS GIVEN
if len(sys.argv) != 2:
    print('ARGUMENT MISSING, UTILITY: python3 main.py number_of_rows_to_be_generated')
    exit(1)

# GET ARGUMENT
try:
    number_of_rows_to_be_generated = int(sys.argv[1])
except ValueError:
    print('ARGUMENT MUST BE AN INTEGER!')
    exit(1)

def run(number_of_rows_to_be_generated)->None:

    # READ THE JSON FILE WHICH CONTAINS THE DB SCHEMA METADATA
    json_file = open('config.json')

    print('LOADING JSON FILE...')
    try:
        schema = json.load(json_file)
    except Exception:
        print('FAILED LOADING JSON FILE!')
    print('JSON FILE SUCCESFULLY LOADED!\n')

    print('ANALYZING DB SCHEMA...')
    # GET ATTRIBUTE TYPES FOR EACH TABLE IN THE SCHEMA
    table_attribute_list = analyze(schema)
    print('\nDB SCHEMA INFORMATION GATHERING DONE!')

    print(f'GENERATING {number_of_rows_to_be_generated} ROWS OF MOCK DATA FOR EACH TABLE...\n')

    all_data_generated = []

    # PASS EACH ATTRIBUTE LIST TO A MOCK DATA GENERATOR WHICH GENERATES A SPECIFIED NUMBER OF RECORDS FOR EACH TABLE
    for index, attribute_list in enumerate(table_attribute_list, 1):
        # FILL HISTORY TABLE WITH GENERATED DATA
        if index == 2:
            history = []
            for row in all_data_generated[0]:
                history_row = {}
                for attr in attribute_list:
                    attr_name = attr[0]
                    if attr_name == 'file_name':
                        history_row[attr_name] = row['last_arrived_file']
                    elif attr_name == 'file_arrival_date':
                        history_row[attr_name] = row['hwm']
                    elif attr_name == 'available_per_sla':
                        history_row[attr_name] = bool(random.getrandbits(1))
                    else: history_row[attr_name] = row[attr_name]

                history.append(history_row)

            all_data_generated.append(history)
        else:
            mock_data_records = generate_mock_data(attribute_list, number_of_rows_to_be_generated)
            all_data_generated.append(mock_data_records)

    print('DONE GENERATING DATA!\n')

    # SEPARATE 2 SPECIFIC TABLES FOR EDC_META SCHEMA
    # EDC_META.ETL_FILES TABLE
    etl_files_table_data = all_data_generated[0]

    # EDC_META.ETL_FILES_HISTORY TABLE
    etl_files_history_table_data = all_data_generated[1]

    # CREATING CONNECTION WITH THE DB SPECIFIED IN THE config.json FILE
    print('CREATING DB CONNECTION...')
    try:
        conn = connect()
    except Exception:
        print('CONNECTION CREATION FAILED!')
        exit(1)
    print('SUCCESSFULLY CONNECTED TO DB!\n')

    # INFINITE LOOP IN CASE SOMETHING GOES WRONG IT RETRIES
    ok = False
    while not ok:
        print('FILLING TABLE etl_files WITH DATA GENERATED...')
        try:
            fill_etl_files(conn, etl_files_table_data)
        except Exception:
            print('FAILED FILLING TABLE etl_files!')
            exit(1)
        print(f'TABLE etl_files SUCCESSFULLY FILLED WITH {number_of_rows_to_be_generated} ROWS!\n')

        print('FILLING TABLE etl_files_history WITH DATA GENERATED...')
        try:
            fill_etl_files_history(conn, etl_files_history_table_data)
        except Exception:
            print('FAILED FILLING TABLE etl_files_history!')
            exit(1)
        print(f'TABLE etl_files_history SUCCESSFULLY FILELD WITH {number_of_rows_to_be_generated} ROWS!\n')

        print('EXECUTING SUMMARY PROCEDURE IN ORDER TO FILL TABLE etl_files_summary...')
        try:
            execute_summary_procedure(conn)
        except Exception:
            print('FAILED TO EXECUTE PROCEDURE!\n')
            print('TRUNCATING TABLES...')
            truncate_all(conn)
            print('TRUNCATED!\n')
            continue
        print('PROCEDURE FIRED SUCCESFULLY!\n')
        print("etl_files_summary TABLE FILLED SUCCESFULLY!\n")
        ok = True




run(number_of_rows_to_be_generated)
