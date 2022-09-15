
from prisma import prisma_Create
from prisma_mongo import get_mongodb

import pymongo

def get_list_group():
    groups = [
        {'id': '0001', 'name':'지상파/종편', 'chs':[
            {'id': ''},
            {'id': ''},
            {'id': ''},
            {'id': ''},
        ]}
    ]


def create_group_mesg(gid, op_data, mesg):
    return 0
    # def prisma_Create(serviceid, endpointid, jdata, opcode='events', idx=0, mid_src=''):


def get_col():
    mongodb = get_mongodb()
    return mongodb['prisma']['group']


def next_id():
    last_id = -1
    rec_last = get_col().find_one(None, sort=[('_id', pymongo.DESCENDING)])
    if rec_last is not None:
        last_id = int(rec_last['id'][1:])
    last_id += 1
    gid = f'G{last_id:03}'

    return gid


# Create
def add_group(gdata):
    gid = next_id()

    print(gid)


# Read
def get_group_gid(gid):
    return get_col().find_one({'id': gid}, {"_id": False})


# Update
# Delete

print(get_group_gid('G005'))