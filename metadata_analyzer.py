import sys

# APPEND ALL ATTRIBUTE TYPES FROM A TABLE IN A LIST AND RETURN IT
def _get_attributes(table: dict)-> list:

    attributes = []

    for attr in table['attributes']:
        # CHECK IF ATTRIBUTE TYPE IS CHAR OR VARCHAR AND IF SO THEN SAVE SIZE TOO
        if attr['attribute_type'] == 'CHAR' or attr['attribute_type'] == 'VARCHAR' or attr['attribute_type'] == 'CHARACTER' or attr['attribute_type'] == 'NCHAR' or attr['attribute_type'] == 'CHARACTER VARYING' or attr['attribute_type'] == 'NVARCHAR' or attr['attribute_type'] == 'TEXT':
            attributes.append((attr['attribute_name'], attr['attribute_type'], attr['size']))
        else:
            attributes.append((attr['attribute_name'], attr['attribute_type']))

    return attributes

# GET EVERY TABLE FROM THE DB SCHEMA AND ANALYZA THE ATTRIBUTE TYPES IN ORDER TO GENERATE RANDOM ROWS
def analyze(schema: dict)-> list:

    tables = schema['schema']['schema_tables']
    print(f'{len(tables)} TABLE SCHEMAS FOUND!\n')

    table_attributes_list = []

    print('GATHERING ATTRIBUTE TYPES FROM EACH TABLE...')
    # GET ATTRIBUTES IN attributes LIST FOR EACH TABLE IN THE SCHEMA
    for index, table in enumerate(tables, 1):
        attributes = _get_attributes(table)
        table_attributes_list.append(attributes)
        print(f'TABLE {index} DONE!')

    return table_attributes_list
    