1. make a folder in which you unzip the .zip file

2. run setup.sh(give execute right to the file if needed, chmod u+x <filename>)

3. go to config.json file and at database_connection section enter your db information to connect to -> save

4.run python3 main.py <number_of_rows_to_be_generated>

HINT: etl_files, etl_files_history and etl_files_summary tables must be created before running script!!!