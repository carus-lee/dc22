from pymongo import MongoClient
from pymongo.cursor import CursorType
import json
from prisma_mongo import insert_item_one, insert_item_many, find_item_one, find_item, log_print, get_mongodb, update_item_one, update_item_many


init_json_file='D:/2022/prisma/prisma/python/init.json'

def reset_preset(mongo, data, db_name=None, collection_name=None):
    result = mongo[db_name][collection_name].delete_many({})
    print(f'delete many -- {result}')
    result = mongo[db_name][collection_name].insert_one(data).inserted_id
    return result

def find_preset(name_type):

    mongo = get_mongodb()
    list = find_item(mongo, None, 'prisma', 'preset')
    data=None
    for item in list:
        data=item[name_type]

    return data


def add_group(gid, gname):
    mongo = get_mongodb()
    list = find_item(mongo, None, 'prisma', 'group')

    item_data={}
    print(f'====== {list}')
    for doc in list:
        iLen=len(doc)
        for item in doc:
            if item !=name_type:
                item_data[item]=doc[item]
                print(f'def key {item} ={name_type} ---> {item_data}')
            else:
                print('same key')
                idx=-1
                list_data=doc[item]
                for idata in list_data:
                    idx_temp=int(idata['id'])
                    if idx<int(idx_temp):
                        idx=idx_temp
                        print(f'idx update ---{idx}')
                idx+=1
                data['id']=idx
                list_data.append(data)
                # print(f'append data : {data}')
                item_data[item]=list_data

            print(f'{item}-------{type(doc[item])}  --------{doc[item]}')
            # data=item[name_type]

    print(f'data ---- {item_data}')
    reset_preset(mongo, item_data, 'prisma', 'preset')

def del_preset(name_type, del_idx):
    mongo = get_mongodb()
    list = find_item(mongo, None, 'prisma', 'preset')

    item_data={}
    # print(f'====== {list}')
    for doc in list:
        iLen=len(doc)
        for item in doc:
            if item !=name_type:
                item_data[item]=doc[item]
                # print(f'def key {item} ={name_type} ---> {item_data}')
            else:
                print('same key')
                list_temp=[]
                list_data=doc[item]
                for idata in list_data:
                    idx_temp=idata['id']
                    if del_idx==idx_temp:
                        print(f'find idx ---{idx_temp}')
                    else:
                        list_temp.append(idata)

                item_data[item]=list_temp

            # print(f'{item}-------{type(doc[item])}  --------{doc[item]}')
            # data=item[name_type]

    # print(f'data ---- {item_data}')
    reset_preset(mongo, item_data, 'prisma', 'preset')


def edit_preset(name_type, edit_idx, data):
    mongo =  get_mongodb()
    list = find_item(mongo, None, 'prisma', 'preset')

    item_data={}
    # print(f'====== {list}')
    for doc in list:
        iLen=len(doc)
        for item in doc:
            if item !=name_type:
                item_data[item]=doc[item]
                # print(f'def key {item} ={name_type} ---> {item_data}')
            else:
                print('same key')
                list_temp=[]
                list_data=doc[item]
                for idata in list_data:
                    idx_temp=idata['id']
                    if edit_idx==idx_temp:
                        print(f'find idx ---{idx_temp}')
                        data['id']=idx_temp
                        list_temp.append(data)
                    else:
                        list_temp.append(idata)

                item_data[item]=list_temp

            # print(f'{item}-------{type(doc[item])}  --------{doc[item]}')
            # data=item[name_type]

    # print(f'data ---- {item_data}')
    reset_preset(mongo, item_data, 'prisma', 'preset')


def test_group(gid, gsort):
    mongo = get_mongodb()
    filter_val={'gid': gid}
    update_val={ "$set" : {'sort':gsort}}
    list = update_item_one(mongo, filter_val, update_val, 'prisma', 'group')

    print(f'{list}')



def init_group(logger=None):
    rtn=[]
    data =[
        {"gid":"a884ff5490da485e91eec221624e2376", "gname":"group name 1", "sort":"asc",
         "channels":[
             {"cid":"TC01_BS04_terrestrial", "cname":"TC01_BS04_terrestrial"},
             {"cid":"TC01_BS04_PP_GSshop", "cname":"TC01_BS04_PP_GSshop"},
             {"cid":"TC01_BS08_Relay", "cname":"TC01_BS08_Relay"},
             ]},
        {"gid":"4d227ca0e24e487fb7485824f9452ad3", "gname":"group name 2", "sort":"asc",
          "channels":[
             {"cid":"TC01_BS08_PPV", "cname":"TC01_BS08_PPV"},
             {"cid":"TC03_BS04_Relay", "cname":"TC03_BS04_Relay"},
             {"cid":"TC03_BS04_PPV", "cname":"TC03_BS04_PPV"},
             ]},
    ]

    mongo =  get_mongodb()
    isExist=find_item_one(mongo, None, 'prisma', 'group')


    if isExist is not None:
        len_data=len(isExist)
        log_print(f'데이터가 이미 존재합니다!!!! ({len_data})', logger)
    else:
        log_print(f'초기 데이터를 설정합니다...')
        # 초기설정 파일 읽기
        json_data=None
        # with open(init_json_file, 'r', encoding='UTF-8') as f:
        #     json_data=json.load(f)

        if json_data is None:
            log_print(f'초기 설정파일(init.json)이 존재 하지 않습니다.', logger)
            result = insert_item_many(mongo, data, 'prisma', 'group')
            log_print(f'디폴트 데이터로 설정 완료! ({result})', logger)
        else:
            log_print(f"초기 설정파일(init.json) 로드 중...", logger)
            result = insert_item_one(mongo, json_data, 'prisma', 'preset')
            log_print(f'초기 설정 파일 설정 완료! ({result})', logger)



# 초기 설정
init_group()
test_group('a884ff5490da485e91eec221624e2376', 'twinsjbu')


# data=find_preset('animation')
# print(data)

# data={'name':'crawler4', 'duration':100, 'mid':'hello.swf', 'layer':1,
#                     'options':
#                         {
#                         'SWF_TEXT_01':'자막송출 TEST 입니다. 1234567890 ABCDEFGHIJKLNMopqrstuvwxyz',
#                         'SWF_SPEED' : 5,
#                         'SWF_Y_POSITION':850,
#                         'SWF_FONT_SIZE':100,
#                         'SWF_COLOR':'ffffff',
#                         'SWF_COLOR_BACK':'888888',
#                         'SWF_FONT_NAME':'궁서'
#                         }
#                 }
# ret=add_preset('animation', data)


# del_preset('animation', 1)

# edit_preset('animation', 0, data)

# print(ret)






