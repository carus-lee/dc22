from pymongo import MongoClient
from pymongo.cursor import CursorType
import json
from prisma_mongo import insert_item_one, insert_item_many, find_item_one, find_item, log_print, get_mongodb


init_json_file='D:/2022/prisma/prisma/python/init.json'

def reset_preset(mongo, data, db_name=None, collection_name=None):
    result = mongo[db_name][collection_name].delete_many({})
    print(f'delete many -- {result}')
    result = mongo[db_name][collection_name].insert_one(data).inserted_id
    return result

def find_preset(name_type):

    mongo =  get_mongodb()
    list = find_item(mongo, None, 'prisma', 'preset')
    data=None
    for item in list:
        data=item[name_type]

    return data


def add_preset(name_type, data):
    mongo = get_mongodb()
    list = find_item(mongo, None, 'prisma', 'preset')

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







    # idx=0
    # #index 구하기
    # preset_data=find_preset(name_type)
    # if preset_data is not None:
    #     for item in preset_data:
    #         idx_temp = item['id']
    #         if idx_temp > idx:
    #             idx= idx_temp
    #     preset_data.append(data)

    #     #맥스값의 1 추가
    #     idx+=1

    # data={ 'animation': data}

    # # mongo = MongoClient(host, int(port))
    # # ret=insert_item_one(mongo, data, 'prisma', 'preset')

    # # return ret



def init_preset(logger=None):
    rtn=[]
    data ={'animation':
            [
                {'id':0, 'name':'crawler', 'duration':100, 'mid':'hello.swf', 'layer':1,
                    'options':
                        [
                        {'name':'SWF_TEXT_01', 'value':'자막송출 TEST 입니다. 1234567890 ABCDEFGHIJKLNMopqrstuvwxyz'},
                        {'name':'SWF_SPEED' , 'value': '5'},
                        {'name':'SWF_Y_POSITION', 'value':'850'},
                        {'name':'SWF_FONT_SIZE', 'value':'100'},
                        {'name':'SWF_COLOR', 'value':'ffffff'},
                        {'name':'SWF_COLOR_BACK', 'value':'888888'},
                        {'name':'SWF_FONT_NAME', 'value':'궁서'}
                        ]
                },

            ],
            'slate': [
                {'id':0, 'name':'sun_err.jpg', 'duration':30, 'mid':'sun_err.jpg'},
                {'id':1, 'name':'system_err', 'duration':15, 'mid':'system_err.jpg'},
            ],
            'video clip': [
                {'id':0, 'name':'emergency', 'clips':
                    [
                        {'mid':'clip_emergency.ts', 'duration':30, 'start offset':0}
                    ]
                },
                {'id':1, 'name':'TEST_500', 'clips':
                    [
                        {'mid':'clip_emergency.ts', 'duration':500, 'start offset':0}
                    ]
                },

            ],
            'alternate content': [
                {'id':0, 'name':'SWF Adv.', 'mid':'hellow.swf'},
                {'id':1, 'name':'re', 'mid':'re'},
            ],
        }

    mongo =  get_mongodb()
    isExist=find_item_one(mongo, None, 'prisma', 'preset')


    if isExist is not None:
        len_data=len(isExist)
        log_print(f'데이터가 이미 존재합니다!!!! ({len_data})', logger)
    else:
        log_print(f'초기 데이터를 설정합니다...')
        # 초기설정 파일 읽기
        json_data=None
        with open(init_json_file, 'r', encoding='UTF-8') as f:
            json_data=json.load(f)

        if json_data is None:
            log_print(f'초기 설정파일(init.json)이 존재 하지 않습니다.', logger)
            result = insert_item_one(mongo, data, 'prisma', 'preset', logger)
            log_print(f'디폴트 데이터로 설정 완료! ({result})', logger)
        else:
            log_print(f"초기 설정파일(init.json) 로드 중...", logger)
            result = insert_item_one(mongo, json_data, 'prisma', 'preset')
            log_print(f'초기 설정 파일 설정 완료! ({result})', logger)



# 초기 설정
init_preset()


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






