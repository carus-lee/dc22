# import paramiko
from scp import SCPClient, SCPException
from os import listdir, stat
from prisma_init import config_dir_assets, config_dir_service_list
import json


def get_file_list_ssh(hostname, port=22, directory='/mfvpel/assets', passwd='3nvivo_!', ext='*'):
    sftp_hostname = hostname
    sftp_port = port
    sftp_user = 'root'
    sftp_passwd = passwd
    sftp_directory = directory

    ssh = paramiko.SSHClient()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())

    ssh.connect(sftp_hostname, port=sftp_port, username=sftp_user, password=sftp_passwd)

    sftp = ssh.open_sftp()
    sftp.chdir(sftp_directory)
    files = sftp.listdir()

    for file in files:
        print(file)

    # print(files)


def get_file_list(dir_name):
    file_list = listdir(dir_name)
    files_ls = []

    for file_itm in file_list:
        file_name = dir_name + '/' + file_itm
        stat_info = stat(file_name)
        files_ls.append({'filename': file_itm, 'size': stat_info.st_size, 'date': stat_info.st_atime})

    return files_ls


def get_list_service_file():
    base_dir = config_dir_service_list()
    file_list = listdir(base_dir)
    files_ls = []

    for file_item in file_list:
        # print(file_item)
        file_full_path = base_dir + '/' + file_item
        with open(file_full_path, 'r') as fp:
            json_data = json.load(fp)
            json_config = json_data['config']
            # print(json_config)
            files_ls.append(json_config)

    # print(len(files_ls))

    return files_ls


def test_group_ch_list():
    service_list = get_list_service_file()
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





def get_file_list_assets():
    print(';;;')
    return get_file_list(config_dir_assets())

#getFileList('onyun.club', port=18981)
# get_file_list_ssh('10.1.216.10', passwd='MediaKind')

# get_list_service_file()


# test_group_ch_list()