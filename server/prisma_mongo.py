from pymongo import MongoClient
from pymongo.cursor import CursorType
import json

host = "localhost"
# port = "3001"
port = "27017"
username = 'root'
password = '1234'
#init_json_file='D:/2022/prisma/prisma/python/init.json'
init_json_file='./init.json'


def insert_item_one(mongo, data, db_name=None, collection_name=None):
    result = mongo[db_name][collection_name].insert_one(data).inserted_id
    return result


def insert_item_many(mongo, datas, db_name=None, collection_name=None):
    result = mongo[db_name][collection_name].insert_many(datas).inserted_ids
    return result


def find_item_one(mongo, condition=None, db_name=None, collection_name=None):
    result = mongo[db_name][collection_name].find_one(condition, {"_id": False})
    return result


def find_item_id(mongo, svc_id, db_name=None, collection_name=None):
    result = mongo[db_name][collection_name].find({"_id": svc_id}, {})
    print(f'result1_{result}')


    return result


def find_item(mongo, condition=None, db_name=None, collection_name=None):
    result = mongo[db_name][collection_name].find(condition, {"_id": False}, no_cursor_timeout=True, cursor_type=CursorType.EXHAUST)
    return result


def update_item_one(mongo, condition=None, update_value=None, db_name=None, collection_name=None):
    result = mongo[db_name][collection_name].update_one(filter=condition, update=update_value)
    return result


def update_item_many(mongo, condition=None, update_value=None, db_name=None, collection_name=None):
    result = mongo[db_name][collection_name].update_many(filter=condition, update=update_value)
    return result


def get_mongodb():
    # mongo_cli = MongoClient(f'mongodb://{username}:{password}@{host}:{port}')
    # print(mongo_cli)
    # return mongo_cli
    return MongoClient(host, int(port))


def log_print(msg, logger=None):
    if logger is None:
        print(msg)
    else:
        logger.log(msg)


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

    mongo = MongoClient(host, int(port))
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



 


