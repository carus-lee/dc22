import json
from pymongo import MongoClient


def setup_mongo_init():

    # import
    mongodb_host = 'localhost'
    mongodb_port = 27017
    db = None

    with open('setup.json', 'r') as file:
        dict_setup = json.load(file)

        for collection_temp in dict_setup:
            col_name = collection_temp['col_name']
            if col_name == 'config':
                value_data = collection_temp['value']
                mongodb_host = value_data['mongodb_host']
                mongodb_port = value_data['mongodb_port']
                mongo = MongoClient(mongodb_host, int(mongodb_port))
                db = mongo['prisma']

    with open('setup.json', 'r', encoding='UTF-8') as file:
        dict_setup = json.load(file)
        # 인덱싱
        # result = db.profiles.create_index([('user_id', pymongo.ASCENDING)], unique=True)
        # ['_id_', 'user_id_1']

        for collection_temp in dict_setup:
            col_name = collection_temp['col_name']
            value_data = collection_temp['value']

            s_value = f'{value_data}'
            print(f'col_name({col_name}): {len(value_data)}, {len(s_value)}')

            is_exist = db[col_name].find_one(None, {"_id": False})
            if is_exist is None:
                if col_name in ['config', 'schedule', 'DSLS']:
                    is_exist = db[col_name].find_one(None, {"_id": False})
                    if is_exist is None:
                        ses_id = db[col_name].insert_one(value_data).inserted_id
                elif col_name in ['preset', 'group', 'service']:
                    for preset_item in value_data:
                        ses_id = db[col_name].insert_one(preset_item).inserted_id
            else:
                # ses_id = db[col_name].insert_one(value_data).inserted_id
                print(f'{col_name} duplicate data!!!, ignore')
                ses_id = None

            print(f'ses_id : {ses_id}')


setup_mongo_init()
