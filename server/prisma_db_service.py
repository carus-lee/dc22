from prisma_db import add_data, get_data, update_data, get_list, delete_all, add_data_loop
import requests


def json_get(url):
    header = {'Content-Type' : 'application/json', 'Host': '192.168.100.59'}
    res=requests.get(url, headers=header)
    return res.json()

collection_name = 'service'


def get_list_service():
    return get_list(collection_name)


def add_data_service(s_data):
    return add_data_loop(collection_name, s_data)


def fetch_service_all(base_url):
    url = f'{base_url}/api/services/streamConditionings'
    res = json_get(url)
    sres = f'{res}'
    print(f'service/id ----> {res}')
    idx = 0
    ids = {}

    cur_del = delete_all(collection_name)
    print(f'del all for fetch data, {cur_del.deleted_count} docs deleted. ')

    add_data_service(res)

    # for id in res:
    #     sid = id['id']
    #     print(f'{idx}, {sid}')
    #     ids[sid] = id
    #     idx += 1
    # # print(f'ids={ids.items()}')
    # sorted_ids = sorted(ids.items(), key=lambda item: item[0])
    # # print(f'sorted_ids={sorted_ids}')
    # sorted_res = []
    # for id0 in sorted_ids:
    #     log_print(id0[0])
    #     sorted_res.append(id0[1])


def update_service_http():
    return None
#
# for item in get_list_service():
#     print(item)


# fetch_service_all('http://192.168.21.101:8080')
# print('-------')
# data = get_list_service()
# print(f'-------{data} ----')
# print(f'-------{len(data)} ----')
