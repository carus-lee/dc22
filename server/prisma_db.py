import pymongo

host = "localhost"
port = "27017"


def get_mongodb():
    # mongo_cli = MongoClient(f'mongodb://{username}:{password}@{host}:{port}')
    # print(mongo_cli)
    # return mongo_cli
    return pymongo.MongoClient(host, int(port))


def get_col(col_name):
    mongodb = get_mongodb()
    return mongodb['prisma'][col_name]


def next_id(col_name):
    last_id = -1
    rec_last = get_col(col_name).find_one(None, sort=[('_id', pymongo.DESCENDING)])
    if rec_last is not None:
        last_id = int(rec_last['id'][1:])
    last_id += 1
    gid = f'G{last_id:03}'

    return gid


# Create
def add_data(col_name, d_data):
    d_id = next_id(col_name)
    d_data['id'] = d_id
    return get_col(col_name).insert_one(d_data).inserted_id


def add_data_loop(col_name, d_data):
    idx = 0
    for item_data in d_data:
        get_col(col_name).insert_one(item_data)
        idx += 1

    print(f'insert rows : {idx}')




# Read
def get_data(col_name, d_id):
    return get_col(col_name).find_one({'id': d_id}, {"_id": False})


def get_list(col_name):
    return list(get_col(col_name).find(None, {"_id": False}))


# Update
def update_data(col_name, d_id, d_key, d_data):
    get_col(col_name).update_one({'id': d_id}, {'$set': {d_key: d_data}})


def update_dict_id(col_name, d_id, d_data):
    rtn = get_col(col_name).update_one({'id': d_id}, {'$set': d_data})
    print(f'update_dict_id.rtn: {rtn}')



def delete_data_id(col_name, value):
    return get_col(col_name).delete_one({'id': value})

# Delete
def delete_all(col_name):
    return get_col(col_name).delete_many({})

# print(get_data('group', 'G005'))