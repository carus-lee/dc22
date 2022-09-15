from prisma_db import add_data, get_data, update_data, get_list, delete_data_id, update_dict_id
from prisma_db_service import get_list_service


def get_list_group():
    return get_list('group')


def del_group_id(gid):
    return delete_data_id('group', gid)


def add_group_list(upload_data):
    add_data('group', upload_data)


def update_group_list(upload_data):
    update_dict_id('group', upload_data['id'], upload_data)


def test_group_ch_list():
    service_list = get_list_service()
    n_service = len(service_list)
    n_group = 7
    list_group_dict = [
        {'id': 'G000', 'name': '지상파/종편', 'tips': '지상파 방송사 및 종합편성 방송사업자', 'count': 0, 'ch_names': '', 'chs': []},
        {'id': 'G001', 'name': '드라마', 'tips': '드라마채널', 'count': 0, 'ch_names': '', 'chs': []},
        {'id': 'G002', 'name': '연예/오락', 'tips': '연예오락 채널', 'count': 0, 'ch_names': '', 'chs': []},
        {'id': 'G003', 'name': '시사교양', 'tips': '뉴스채널', 'count': 0, 'ch_names': '', 'chs': []},
        {'id': 'G004', 'name': '스포츠', 'tips': '스포츠채널', 'count': 0, 'ch_names': '', 'chs': []},
        {'id': 'G005', 'name': '영화', 'tips': '영화채널', 'count': 0, 'ch_names': '', 'chs': []},
        {'id': 'G006', 'name': '어린이', 'tips': '유아/어린이 채널', 'count': 0, 'ch_names': '', 'chs': []},
    ]

    list_group_dict = get_list_group()

    cnt_sz_cat = n_service / n_group

    idx = 0
    idx_group_last = 0
    for service_item in service_list:
        idx_group = int(idx / cnt_sz_cat)
        # print(service_item['id'], '-----', idx, '====', idx_group)

        if idx_group > idx_group_last:
            idx_group_last = idx_group

        dict_id = {'id': service_item['id'], 'connection': service_item['connection']}
        list_group_dict[idx_group]['chs'].append(dict_id)
        list_group_dict[idx_group]['count'] = len(list_group_dict[idx_group]['chs'])

        s_ch_names=''
        for ch_item in list_group_dict[idx_group]['chs']:
            s_ch_names += ch_item['id']+', '
        list_group_dict[idx_group]['ch_names'] = s_ch_names

        idx += 1

    # print(list_grou_dict)

    return list_group_dict


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
