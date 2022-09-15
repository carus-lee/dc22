from pymongo import MongoClient
from pymongo.cursor import CursorType


def insert_item_one(mongo, data, db_name=None, collection_name=None):
    result = mongo[db_name][collection_name].insert_one(data).inserted_id
    return result

def insert_item_many(mongo, datas, db_name=None, collection_name=None):
    result = mongo[db_name][collection_name].insert_many(datas).inserted_ids
    return result
    
def find_item_one(mongo, condition=None, db_name=None, collection_name=None):
    result = mongo[db_name][collection_name].find_one(condition, {"_id": False})
    return result

def find_item(mongo, condition=None, db_name=None, collection_name=None):
    result = mongo[db_name][collection_name].find(condition, {"_id": False}, no_cursor_timeout=True, cursor_type=CursorType.EXHAUST)
    return result



host = "localhost"
port = "3001"

mongo = MongoClient(host, int(port))

test=MongoClient(host=host, port=int(port), username='root', password="admin"),

print(mongo.list_database_names())

db = mongo.test_db


data ={'animation':
            [
                {'id':0, 'name':'crawler', 'duration':100, 'mid':'hello.swf', 'layer':1, 
                    'options':
                        {
                        'SWF_TEXT_01':'자막송출 TEST 입니다. 1234567890 ABCDEFGHIJKLNMopqrstuvwxyz',
                        'SWF_SPEED' : 5,
                        'SWF_Y_POSITION':850,
                        'SWF_FONT_SIZE':100,
                        'SWF_COLOR':'ffffff',
                        'SWF_COLOR_BACK':'888888',
                        'SWF_FONT_NAME':'궁서'         
                        }
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

# 초기 설정
# insert_item_one(mongo, data, 'prisma', 'preset')

#result = db.things.insert_one(data)
#print(result.inserted_id)
list =mongo['pri']['test'].find(None, {'_id':False})
list = find_item(mongo, None, 'prisma', 'preset')
for item in list:
    print(item['slate'])

 


