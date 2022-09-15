from prisma_db import add_data, get_data, update_data, get_list, delete_data_id, update_dict_id
from prisma_db_service import get_list_service


name_collection = 'schedule'

def get_list_schedule(div):
    return get_list(name_collection)[0][div]


def get_list_schedule_all():
    return get_list(name_collection)


def get_list_schedule_config():
    return get_list_schedule('config')


def get_list_schedule_session():
    return get_list_schedule('session')


def del_schedule_id(gid):
    return delete_data_id(name_collection, gid)


def add_group_list(upload_data, div):
    add_data(name_collection, upload_data)


def update_group_list(upload_data):
    update_dict_id(name_collection, upload_data['id'], upload_data)



def import_group_ch_list():
    service_list = get_list_service()
    n_service = len(service_list)
    n_group = 7
    list_group_dict = get_list_group()

    cnt_sz_cat = n_service / n_group

    idx = 0
    idx_group_last = 0
    for service_item in service_list:
        idx_group = int(idx / cnt_sz_cat)
        # print(service_item['id'], '-----', idx, '====', idx_group)
        # list_group_dict[idx_group]['chs'] = []

        if idx_group > idx_group_last:
            idx_group_last = idx_group

        dict_id = {'id': service_item['id'], 'connection': service_item['connection']}
        list_group_dict[idx_group]['chs'].append(dict_id)
        list_group_dict[idx_group]['count'] = len(list_group_dict[idx_group]['chs'])

        s_ch_names=''
        for ch_item in list_group_dict[idx_group]['chs']:
            s_ch_names += ch_item['id']+', '
        list_group_dict[idx_group]['ch_names'] = s_ch_names

        s_id = list_group_dict[idx_group]['id']
        print(f'id : {s_id}')

        update_data('group', list_group_dict[idx_group]['id'], 'chs', list_group_dict[idx_group]['chs'])
        update_data('group', list_group_dict[idx_group]['id'], 'ch_name', s_ch_names)
        update_data('group', list_group_dict[idx_group]['id'], 'count',  len(list_group_dict[idx_group]['chs']))

        idx += 1

    # print(list_grou_dict)

#
# import_group_ch_list()

# sdata =get_list_schedule_config()
# print(sdata)
# print('---')
# sdata =get_list_schedule_session()
# print(sdata)
# print('---')
