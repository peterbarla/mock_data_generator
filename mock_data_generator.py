from attribute_gen_wrapper import *

# BIND REDSHIFT DATA TYPES TO THE CORRESPONDING PYTHON DATA GENERATOR FUNCTION()
attribute_callables = {'group_id': group_id, 'category': category, 'sub_category': sub_category,
                             'file_name_mask': file_name_mask, 'last_arrived_file': last_arrived_file, 
                             'last_arrived_file_timestamp': last_arrived_file_timestamp, 'lwm': lwm, 'hwm': hwm, 'sla': sla,
                             'file_name': file_name, 'file_arrival_date': file_arrival_date, 'available_per_sla': available_per_sla}

# GENERATE MOCK DATA FOR EACH ATTRIBUTE TYPE IN THE ATTRIBUTE LIST ROWCOUNT TIMES
def generate_mock_data(attributes: list, rowcount: int)-> list:

    # STORES ROWCOUNT NUMBER OF RANDOMLY GENERATED RECORDS
    rows = []

    for i in range(rowcount):

        mock_data_record = {}

        # INVOKE BINDED FUNCTION FOR EACH ATTRIBUTE TYPE
        for attr in attributes:
            if attr[0] == 'sub_category':
                mock_data_record[attr[0]] = attribute_callables[attr[0]](mock_data_record['category'])
            elif attr[0] == 'file_name_mask':
                mock_data_record[attr[0]] = attribute_callables[attr[0]](mock_data_record['sub_category'])
            elif attr[0] == 'last_arrived_file':
                mock_data_record[attr[0]] = attribute_callables[attr[0]](mock_data_record['file_name_mask'])
            elif attr[0] == 'last_arrived_file_timestamp':
                mock_data_record[attr[0]] = attribute_callables[attr[0]](mock_data_record['last_arrived_file'])
            elif attr[0] == 'lwm':
                mock_data_record[attr[0]] =  attribute_callables[attr[0]](mock_data_record['last_arrived_file'])
            elif attr[0] == 'hwm':
                mock_data_record[attr[0]] =  attribute_callables[attr[0]](mock_data_record['last_arrived_file'])
            else: mock_data_record[attr[0]] = attribute_callables[attr[0]]()


        rows.append(mock_data_record)

    return rows
