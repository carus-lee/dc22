import os
import json



config_data= {
    'test': {
        'url_base': 'http://10.1.216.11:8080',
        'dir_img': 'e:/projects/2022/prisma/pycharm/server/image_svc/',
        'dir_assets': '/root/dc22/server/assets/',
        'service_list': '/root/dc22/server/debug/service_list'
    },
    'commercial': {
        'url_base': 'http://10.1.216.11:8080',
        'dir_img': 'e:/projects/2022/prisma/pycharm/server/image_svc/',
        'dir_assets': '/root/zw22/assets',
        'service_list': '/root/dc22/server/debug/service_list'
    }

}

config_mode = 'test'


def is_debug():
    if config_mode == 'test' :
        return True
    return False


def config_img_dir():
    # return "e:/projects/2022/prisma/pycharm/server/image_svc/"
    return config_data[config_mode]['dir_img']


def config_base_url():
    # return 'http://10.1.216.11:8080'
    return config_data[config_mode]['url_base']


def config_dir_assets():
    # return '/root/zw22/assets'
    return config_data[config_mode]['dir_assets']


def config_dir_service_list():
    return config_data[config_mode]['service_list']
#
# pwd= 'E:/projects/2022/prisma/json'
# os.chdir(pwd)
# ls = os.listdir()
#
# datas=[]
#
# for dir in ls:
#     print(dir)
#     file_temp=pwd +'/'+ dir
#     with open(file_temp, 'r') as file:
#         data = json.load(file)
#         data_dumps=json.dumps(data)
#
#         datas.append(data['config'])
#
#         # print('---->'+data_dumps)
#
#
# print(json.dumps(datas))
#
# file_temp2 = pwd +'/../jsonfile_111.json'
#
# with open(file_temp2, 'w') as json_file:
#     json.dump(datas, json_file)
# # print(os.listdir())