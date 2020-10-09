import json
import random
import string
import datetime

# SIZE FOR RANDOMLY GENERATED STRINGS
size = 5

# READ THE JSON FILE TO GATHER USER PREFERENCES
json_file = open('config.json')



try:
    schema = json.load(json_file)
except Exception as err:
    print('FAILED LOADING JSON FILE!')

user_preferences = schema['user_preferences']


def group_id()-> int:
    return random.choice(user_preferences['group_id_list'])

def category()-> str:
    return random.choice(user_preferences['category_list'])

def sub_category(categoryy: str)-> str:
    rand_string = ''.join(random.choices(string.ascii_lowercase, k=size))
    return categoryy + '_' + rand_string

def file_name_mask(sub_category: str)-> str:

    # RANDOMIZE IF THE MASK WILL LOOK LIKE {to_dt}_from_{from_dt}_to_{to_dt} or {to_dt} only
    rand_numb = random.choice([0, 1])

    form = '_{to_dt}_from_{from_dt}_to_{to_dt}' if rand_numb == 1 else '_{to_dt}'
    return sub_category + form + '.dat.gz'

def last_arrived_file(file_name_mask: str)-> str:

    # START AND END DATE BETWEEN THE NEW DATE NEEDS TO BE RANDOMLY GENERATED
    start_date = datetime.date(2018, 1, 1)
    end_date = datetime.date(2020, 12, 1)

    # CALCULATING THE DIFFERENCE BETWEEN START AND END DATE IN DAYS SO WE 
    # CAN RANDOMLY GENERATE A NUMBER OF DAYS WITH AN UPPER LIMIT
    time_between_dates = end_date - start_date
    days_between_dates = time_between_dates.days
    random_number_of_days = random.randrange(days_between_dates)

    lwm = (start_date + datetime.timedelta(days=random_number_of_days))
    hwm = (lwm + datetime.timedelta(days=1)).strftime("%Y%m%d")
    lwm = lwm.strftime("%Y%m%d")
    return file_name_mask.replace('{to_dt}', hwm).replace('{from_dt}', lwm)

def last_arrived_file_timestamp(last_arrived_file: str)-> datetime:
    return datetime.datetime.strptime(last_arrived_file[-15:-7], '%Y%m%d')
    

def lwm(last_arrived_file: str)-> datetime:
    return datetime.datetime.strptime(last_arrived_file[-15:-7], '%Y%m%d') - datetime.timedelta(days=1)

def hwm(last_arrived_file: str)-> datetime:
    return datetime.datetime.strptime(last_arrived_file[-15:-7], '%Y%m%d')

def sla()-> str:
    return '00 17   *'

def file_name(sub_category: str)-> str:

    # START AND END DATE BETWEEN THE NEW DATE NEEDS TO BE RANDOMLY GENERATED
    start_date = datetime.date(2020, 1, 1)
    end_date = datetime.date(2020, 12, 1)

    # CALCULATING THE DIFFERENCE BETWEEN START AND END DATE IN DAYS SO WE 
    # CAN RANDOMLY GENERATE A NUMBER OF DAYS WITH AN UPPER LIMIT
    time_between_dates = end_date - start_date
    days_between_dates = time_between_dates.days
    random_number_of_days = random.randrange(days_between_dates)

    lwm = (start_date + datetime.timedelta(days=random_number_of_days))
    hwm = (lwm + datetime.timedelta(days=1)).strftime("%Y%m%d")
    lwm = lwm.strftime("%Y%m%d")
    return

def file_arrival_date(file_name: str)-> datetime:
    return

def available_per_sla()-> bool:
    return bool(random.getrandbits(1))
