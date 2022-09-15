import random
import uuid
import json
import requests, datetime

from prisma_init import config_base_url, config_img_dir, config_dir_assets, is_debug
from prisma_img import send_img_file
from flask import Flask, request, make_response, jsonify, send_file
from flask_cors import CORS
# from prisma_mongo_preset import find_preset, edit_preset, add_preset, del_preset
# from prisma_mongo_group import add_group

from prisma_font import get_duration_text2font

from prisma_db_group import get_list_group, del_group_id, update_group_list, add_group_list
from prisma_db_schedule import get_list_schedule_config, get_list_schedule_session, del_schedule_id
from prisma_db_preset import get_list_preset_all, get_list_preset_method
from os import listdir, stat
from prisma_file import get_file_list, get_file_list_ssh, get_list_service_file, test_group_ch_list

import logging

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)
logFormatter = logging.Formatter('%(asctime)s %(name)s %(message)s')

streamhandler = logging.StreamHandler()
streamhandler.setFormatter(logFormatter)
logger.addHandler(streamhandler)

filehandler = None
try:
    filehandler = logging.FileHandler('/root/prisma/logs/server_{:%Y%m%d}.log'.format(datetime.datetime.now()),
                                      encoding='utf-8')
except FileNotFoundError as e:
    filehandler = logging.FileHandler('server_{:%Y%m%d}.log'.format(datetime.datetime.now()), encoding='utf-8')

filehandler.setFormatter(logFormatter)
logger.addHandler(filehandler)

logging.basicConfig(filename="prisma.log", level=logging.DEBUG)

base_url = config_base_url()

app = Flask(__name__)
app.config['JSON_AS_ASCII'] = False
CORS(app)


def log_print(msg):
    logger.info(msg)


def json_get(url):
    header = {'Content-Type': 'application/json', 'Host': '192.168.100.59'}
    res = requests.get(url, headers=header)
    return res.json()


def json_delete(url):
    header = {'Content-Type': 'application/json', 'Host': '192.168.100.59'}
    res = requests.delete(url, headers=header)
    log_print(f'delete Response : {res}')
    return res


def get_List_Detail(serviceid, endpointid, opcode='events'):
    # url=f'http://192.168.100.59:8080/api/services/streamConditionings/{serviceid}/endPoints/{endpointid}/{opcode}'
    url = f'{base_url}/api/services/streamConditionings/{serviceid}/endPoints/{endpointid}/{opcode}'
    header = {'Content-Type': 'application/json', 'Host': '192.168.100.59'}

    res = requests.get(url, headers=header)

    r_json = res.json()
    log_print(res, res.reason)
    log_print(res.request.headers)
    log_print(res.content)
    # print(res.request.data)

    return r_json


def get_List_Service(url, data_attr='ALL'):
    """전체 채널 목록을 가져오는 function

    Args:
        data_attr : ALL, OP, EVT

    Retruns:
        json 데이터
    """
    retDic = {'request': {'mode': 'all', 'base_url': base_url, 'data_attr': data_attr}, 'response': []}
    retRes = retDic['response']
    r_json = json_get(url)
    for x_s in r_json:
        sid = x_s['id']
        retResSid = {'sid': sid, 'endpoints': []}
        retResSid = {'sid': sid, 'endpoints': []}

        ep_ids = x_s['connection']['endPoints']

        for x_ep in ep_ids:
            epid = x_ep['id']

            j_operation = get_List_Detail(sid, epid, opcode='operations')
            j_events = get_List_Detail(sid, epid, opcode='events')

            if data_attr == 'ALL':
                retResEpid = {'epid': epid, 'operations': j_operation, 'events': j_events}
            elif data_attr == 'OP':
                retResEpid = {'epid': epid, 'operations': j_operation}
            elif data_attr == 'EVT':
                retResEpid = {'epid': epid, 'events': j_events}
            log_print(f'-=-=-= {retResEpid} -=-=-')
            retResSid['endpoints'].append(retResEpid)
            # x_ep['operations']=j_operation
            # x_ep['events']=j_events

        retRes.append(retResSid)
    return retDic


def sort_list_service(data_in, sort_method=None):
    sres = f'{data_in}'
    # log_print(f'service/id ----> {data_in}')
    sorted_res = []
    idx = 0
    ids = {}

    if sort_method is None:
        sorted_res = data_in
    else:
        for id_item in data_in:
            sid = id_item['id']
            # print(f'{idx}, {sid}')
            ids[sid] = id_item
            idx += 1
        # print(f'ids={ids.items()}')
        if sort_method == 'ASC':
            sorted_ids = sorted(ids.items(), key=lambda item: item[0])
        else:  # DESC 처리
            sorted_ids = sorted(ids.items(), key=lambda item: item[0], reverse=True)
        # print(f'sorted_ids={sorted_ids}')

        for id_item in sorted_ids:
            # log_print(id_item[0])
            sorted_res.append(id_item[1])

    return sorted_res


@app.route("/get_list_service/id", methods=['GET'])
def get_list_service_id():
    if request.method == 'GET':
        if is_debug():
            service_list = get_list_service_file()
            # s_lst = f'{service_list}'
            # log_print(f'enter debug mode.......service/id ----> {service_list}')
            return make_response(jsonify(service_list), 200)
        else:
            url = f'{base_url}/api/services/streamConditionings'
            res = json_get(url)
            # sres=f'{res}'
            # log_print(f'service/id ----> {res}')
            # idx=0
            # ids={}
            # for id in res:
            #     sid=id['id']
            #     print(f'{idx}, {sid}')
            #     ids[sid]=id
            #     idx+=1
            # # print(f'ids={ids.items()}')
            # sorted_ids=sorted(ids.items(), key= lambda item: item[0])
            # # print(f'sorted_ids={sorted_ids}')
            # sorted_res=[]
            # for id0 in sorted_ids:
            #     log_print(id0[0])
            #     sorted_res.append(id0[1])
            sorted_res = sort_list_service(res, sort_method='ASC')
            return make_response(jsonify(sorted_res), 200)
    return get_List()


@app.route("/get_list_schedule", methods=['GET'])
def get_list_schedule_get():
    if request.method == 'GET':
        # log_print(f'get_list_schedule_get.schedule_list: enter')
        schedule_list = get_list_schedule_config()
        # log_print(f'get_list_schedule_get.schedule_list: {schedule_list}')
        return make_response(jsonify(schedule_list), 200)
    return get_List()


@app.route("/get_list_group/id", methods=['GET'])
def get_list_group_id():
    if request.method == 'GET':
        if is_debug():
            # FILE의 테스트 데이터 가져오기
            log_print(f'group list (debug) ----')
            group_list = get_list_group()
            # log_print(f'enter debug mode.......group/id ----> {group_list} ')
            return make_response(jsonify(group_list), 200)
        else:
            # 몽고 DB에서 가져오기

            url = f'{base_url}/api/services/streamConditionings'
            res = json_get(url)
            sres = f'{res}'
            log_print(f'service/id ----> {res}')
            idx = 0
            ids = {}
            for id in res:
                sid = id['id']
                print(f'{idx}, {sid}')
                ids[sid] = id
                idx += 1
            # print(f'ids={ids.items()}')
            sorted_ids = sorted(ids.items(), key=lambda item: item[0])
            # print(f'sorted_ids={sorted_ids}')
            sorted_res = []
            for id0 in sorted_ids:
                log_print(id0[0])
                sorted_res.append(id0[1])
            return make_response(jsonify(sorted_res), 200)
    return get_List()


@app.route("/add_group_list", methods=['POST'])
def add_group_list_post():
    if request.method == 'POST':
        # log_print('POST')
        data = request.get_json()
        log_print(f'\n\r ----del_group_list data----{data},,,')
        rtn = add_group_list(data)
        log_print(f'\n\r ----del_group_list data----{data},,,{rtn}')

    return make_response(jsonify({'status': True}), 200)


@app.route("/edit_group_list", methods=['POST'])
def edit_group_list_post():
    if request.method == 'POST':
        # log_print('POST')
        data = request.get_json()
        log_print(f'\n\r ----update_group_list data----{data},,')
        rtn = update_group_list(data)
        log_print(f'\n\r ----update_group_list data----{data},,,{rtn}')

    return make_response(jsonify({'status': True}), 200)


@app.route("/del_group", methods=['POST'])
def delGroup():
    if request.method == 'POST':
        log_print('POST')
        data = request.get_json()
        log_print(f'\n\r ----del_preset data----{data}')
        rtn = del_group_id(data['id'])
        log_print(f'\n\r ----del_preset data----{data},,,{rtn}')

    return make_response(jsonify({'status': True}), 200)


@app.route("/del_schedule_get/<sid>", methods=['GET'])
def del_schedule_get(sid):
    if request.method == 'GET':
        rtn = del_schedule_id(sid)
        log_print(f'\n\r ----del_schedule_get data----{sid},,,{rtn}')

    return make_response(jsonify({'status': True}), 200)


@app.route("/get_list_service/post", methods=['POST'])
def get_list_service_post():
    if request.method == 'POST':
        log_print(f'get_list_service_post.enter debug mode.......service/post 000000000 ----> {request.method}')
        data = request.get_json()
        # log_print(f'get_list_service_post.enter debug mode.......service/post ----> {data}')
        if is_debug():

            service_list_temp = get_list_service_file()
            group_list_temp = test_group_ch_list()
            service_list = []

            req_sort = data['sort_val']
            req_group = data['select_group']
            req_service = data['select_service']
            # 선택된 서비스 유지

            if len(req_group) == 0:  # 그룹 미 선택시
                service_list = get_list_service_file()
            else:
                for group_item in group_list_temp:
                    id_temp = group_item['id']
                    for req_group_item in req_group:
                        if id_temp == req_group_item:
                            service_list_temp = group_item['chs']
                            # log_print(f'match group item ----- {service_list_temp} ')
                            for service_item in service_list_temp:
                                service_list.append(service_item)
            log_print(f'return group({req_group}, {req_sort}) item\'s count----- {len(service_list)} ')

            # 소팅
            sorted_service_list = sort_list_service(service_list, req_sort)

            return make_response(jsonify(sorted_service_list), 200)
        else:
            url = f'{base_url}/api/services/streamConditionings'
            res = json_get(url)
            sres = f'{res}'
            log_print(f'service/id ----> {res}')
            idx = 0
            ids = {}
            for id in res:
                sid = id['id']
                print(f'{idx}, {sid}')
                ids[sid] = id
                idx += 1
            # print(f'ids={ids.items()}')
            sorted_ids = sorted(ids.items(), key=lambda item: item[0])
            # print(f'sorted_ids={sorted_ids}')
            sorted_res = []
            for id0 in sorted_ids:
                log_print(id0[0])
                sorted_res.append(id0[1])
            return make_response(jsonify(sorted_res), 200)
    return get_List()


@app.route("/pcms/push", methods=['POST'])
def pcms_push():
    data = request.get_json()

    id_pcms = data['SubIdenti']
    num_retry = data['SubRepeti']
    mesg = data['SubText']

    log_print(f'pcms_push - id:{id_pcms}, retry:{num_retry}, mesg:{mesg} ')

    dict_return = {
        'ResultCode': '0000',
        'reason': '성공'
    }

    dict_return_fail = {
        'ResultCode': 'FFFF',
        'reason': '키없음!!!'
    }

    if id_pcms == '':
        return make_response(jsonify(dict_return_fail), 200)

    return make_response(jsonify(dict_return), 200)


@app.route("/pcms/status/<id_pcms>", methods=['GET'])
def pcms_status(id_pcms):
    log_print(f'pcms_status - id:{id_pcms}')

    rand_int = random.randrange(1, 10)

    dict_return_ok = {
        'identifier': id_pcms,
        'broadcastDT': '20220905163620',
        'broadcastEt': '20220905164120',
        'ResultCode': '0000',
        'ErrorMsg': ''

    }

    dict_return_2001 = {
        'identifier': id_pcms,
        'ResultCode': '2001',
        'ErrorMsg': ''

    }
    if rand_int > 5:
        return make_response(jsonify(dict_return_ok), 200)
    else:
        return make_response(jsonify(dict_return_2001), 200)


@app.route("/get_list_preset/<id_type>", methods=['GET'])
def get_list_preset_id(id_type):
    if request.method == 'GET':
        data_preset = get_list_preset_method(id_type)
        log_print(data_preset)

        return make_response(jsonify(data_preset), 200)
    return get_List()


@app.route("/get_list_preset_all", methods=['GET'])
def get_list_preset_all_get():
    if request.method == 'GET':
        data_preset = get_list_preset_all()
        log_print(data_preset)

        return make_response(jsonify(data_preset), 200)
    return get_List()


def is_file(dirname, filename):
    list_file = listdir(dirname)

    b_return = False

    for item_file in list_file:
        if item_file == filename:
            b_return = True
            return True

    return b_return


@app.route("/get_svc_img/<svc_id>", methods=['GET'])
def get_svc_img(svc_id):
    # log_print(f'get_svc_img.req ----> {request}')
    if request.method == 'GET':
        file_image_dir = config_img_dir()
        file_name_img = file_image_dir + svc_id + '.jpg'
        file_img_default = file_image_dir + 'default.jpg'

        file_stat = is_file(file_image_dir, svc_id + '.jpg')
        # print(f'file_name_img {file_name_img} ......{file_stat}')

        if file_stat:
            return send_file(file_name_img, mimetype='image/jpeg')
        else:
            return send_file(file_img_default, mimetype='image/jpeg')

    print(f'test {svc_id}')
    return svc_id


def get_List(id_svc=None, id_endp=None, id_op=None, id_evt=None, data_attr='ALL'):
    url = f'{base_url}/api/services/streamConditionings/'
    retDic = {}
    if request.method == 'GET':
        log_print('GET')

        if id_svc == None and id_endp == None and id_op == None and id_evt == None:
            url = f'{base_url}/api/services/streamConditionings/'
            retDic = get_List_Service(url, data_attr)
        elif id_svc != None and id_endp != None:

            retDic = {'request': {'mode': 'ids', 'base_url': base_url, 'id_svc': id_svc, 'id_endp': id_endp,
                                  'data_attr': data_attr}, 'response': {}}
            if data_attr == 'ALL':
                j_operation = get_List_Detail(id_svc, id_endp, opcode='operations')
                j_event = get_List_Detail(id_svc, id_endp, opcode='events')
                retDic['response'] = {'events': j_event, 'operations': j_operation}
            elif data_attr == 'EVT':
                # j_event=json_get(url_evt)
                j_event = get_List_Detail(id_svc, id_endp, opcode='events')
                retDic['response'] = {'events': j_event}
            elif data_attr == 'OP':
                # j_operation=json_get(url_op)
                j_operation = get_List_Detail(id_svc, id_endp, opcode='operations')
                retDic['response'] = {'operations': j_operation}

    # log_print(f'---retRes: {retDic}')
    return make_response(jsonify(retDic), 200)


def prisma_Create(serviceid, endpointid, jdata, opcode='events', idx=0, mid_src=''):
    a = uuid.uuid1()
    temp_jdata = jdata

    # url=f'http://192.168.100.59:8080/api/services/streamConditionings/{serviceid}/endPoints/{endpointid}/{opcode}'
    url = f'{base_url}/api/services/streamConditionings/{serviceid}/endPoints/{endpointid}/{opcode}'
    header = {'Content-Type': 'application/json', 'Host': '192.168.100.59'}

    if opcode == 'events' and idx > 0:
        # mid=temp_jdata['operation']['materialId']
        mid = mid_src
        mid_temp = mid.split('.')
        log_print(f'prisma_create.event-------->{mid_temp}')
        sidx = str(idx)
        sz_idx = sidx.zfill(3)

        mid_target = f'{mid_temp[0]}_{sz_idx}.{mid_temp[1]}'
        # mid_target = f'006_2_36_{sz_idx}.swf'
        temp_jdata['operation']['materialId'] = mid_target

        log_print(f'prisma_create.event-------->{mid} ---- {mid_target} ______ {idx}')

    res = requests.post(url, data=json.dumps(jdata), headers=header)

    log_print(f'prisma_create.res({opcode}:{url}) : {res} --> {type(jdata)},,,,, {jdata}')
    log_print(f'prisma_create.head -->{res.request.headers}')
    log_print(f'prisma_create.content ->{res.content}')
    log_print(f'prisma_create.body ->{res.request.body}')


@app.route("/get_list_service/", methods=['GET'])
def get_list_service():
    return get_List()


@app.route("/get_list_file/<op_code>", methods=['GET'])
def get_list_file(op_code):
    dir_assets = '/root/dc22/server/assets'

    if request.method == 'GET':
        log_print('get get_list_file')
        files_ls = get_file_list(dir_assets)
        retDic = {'request': {}, 'response': files_ls}

    # log_print(f'---retRes: {retDic}')
    return make_response(jsonify(files_ls), 200)


@app.route("/get_list_service/events", methods=['GET'])
def get_list_service_evt():
    return get_List(data_attr='EVT')


@app.route("/get_list_service/operations", methods=['GET'])
def get_list_service_op():
    return get_List(data_attr='OP')


@app.route("/get_list_service/<id_svc>/endPoints/<id_endp>", methods=['GET'])
def get_list_service_svc_endp(id_svc, id_endp):
    return get_List(id_svc=id_svc, id_endp=id_endp)


@app.route("/get_list_service/<id_svc>/endPoints/<id_endp>/events", methods=['GET'])
def get_list_service_svc_endp_evt(id_svc, id_endp):
    return get_List(id_svc=id_svc, id_endp=id_endp, data_attr='EVT')


@app.route("/get_list_service/<id_svc>/endPoints/<id_endp>/operations", methods=['GET'])
def get_list_service_svc_endp_op(id_svc, id_endp):
    return get_List(id_svc=id_svc, id_endp=id_endp, data_attr='OP')


@app.route("/cancel_event/<id_svc>/<id_endp>/<id_evt>", methods=['GET'])
def cancel_event_evt(id_svc, id_endp, id_evt):
    if request.method == 'GET':
        url = f'{base_url}/api/services/streamConditionings/{id_svc}/endPoints/{id_endp}/events/{id_evt}'
        res = json_delete(url)
        sres = f'{res}'
        print(f'cancel_event delete ----> {res}')
        return make_response(jsonify({'status': sres}), 200)


@app.route("/cancel_events", methods=['POST'])
def cancel_event_endp():
    if request.method == 'POST':
        data = request.get_json()
        ids = data["id"]
        print(f'data: {jsonify(ids)}')

        json_ret = {'request': ids, 'response': []}
        for id in ids:
            id_svc = id['sid']
            id_endp = id['epid']
            url = f'{base_url}/api/services/streamConditionings/{id_svc}/endPoints/{id_endp}/events'
            list_event = json_get(url)

            log_print(f'sid:{id_svc}, epid:{id_endp}, url: {url}')

            id_event_playing = ''
            name_event_playing = ''
            type_event_playing = ''
            for x in list_event:
                sId = x['id']
                sState = x['status']['state']
                sName = x['operation']['name']
                sType = x['operation']['type']
                log_print(f'id: {sId}, status:{sState}, type:{sType}')
                if sState == 'playing':
                    id_event_playing = sId
                    name_event_playing = sName
                    type_event_playing = sType

            if id_event_playing != '':
                url = f'{base_url}/api/services/streamConditionings/{id_svc}/endPoints/{id_endp}/events/{id_event_playing}'
                res = json_delete(url)
                sres = f'{res}'
                log_print(
                    f'cancel_events delete ----> {res} / {name_event_playing} / {id_event_playing} / {type_event_playing}')
                json_ret['response'].append(
                    {'mode': 'delete', 'status': 'success', 'name': name_event_playing, 'id': id_event_playing,
                     'sid': id_svc, 'epid': id_endp, 'type': type_event_playing})

            else:
                json_ret['response'].append({'mode': 'delete', 'status': 'event not found'})

        return make_response(jsonify(json_ret), 200)


# 모두 삭제 로직 추가 0125
@app.route("/cancel_events_all", methods=['POST'])
def cancel_event_endp_all():
    if request.method == 'POST':
        data = request.get_json()
        ids = data["id"]
        log_print(f'del0 --> data: {jsonify(ids)}')

        json_ret = {'request': ids, 'response': []}
        for id in ids:
            id_svc = id['sid']
            id_endp = id['epid']
            url = f'{base_url}/api/services/streamConditionings/{id_svc}/endPoints/{id_endp}/events'
            list_event = json_get(url)

            log_print(f'del1 --> sid:{id_svc}, epid:{id_endp}, url: {url}')

            id_event_playing = ''
            name_event_playing = ''
            type_event_playing = ''
            for x in list_event:
                sId = x['id']
                sState = x['status']['state']
                sName = x['operation']['name']
                sType = x['operation']['type']
                log_print(f'cancel_events_all --> id: {sId}, status:{sState}, type:{sType}')

                id_event_playing = sId
                name_event_playing = sName
                type_event_playing = sType

                url = f'{base_url}/api/services/streamConditionings/{id_svc}/endPoints/{id_endp}/events/{id_event_playing}'
                res = json_delete(url)
                sres = f'{res}'
                log_print(
                    f'cancel_events delete ---->{url} : {res} / {name_event_playing} / {id_event_playing} / {type_event_playing}')
                json_ret['response'].append(
                    {'mode': 'delete', 'status': 'success', 'name': name_event_playing, 'id': id_event_playing,
                     'sid': id_svc, 'epid': id_endp, 'type': type_event_playing})

            # if id_event_playing != '':
            #     url=f'{base_url}/api/services/streamConditionings/{id_svc}/endPoints/{id_endp}/events/{id_event_playing}'
            #     res=json_delete(url)
            #     sres=f'{res}'
            #     print(f'cancel_events delete ----> {res} / {name_event_playing} / {id_event_playing} / {type_event_playing}')
            #     json_ret['response'].append({'mode': 'delete', 'status': 'success', 'name': name_event_playing, 'id': id_event_playing, 'sid':id_svc, 'epid': id_endp, 'type': type_event_playing })

            # else:
            #    json_ret['response'].append({'mode': 'delete', 'status': 'event not found'})

        return make_response(jsonify(json_ret), 200)


# 추가  preset 저장
@app.route("/add_preset", methods=['POST'])
def addPreset():
    if request.method == 'POST':
        log_print('POST')
        data = request.get_json()
        log_print(f'\n\r ----add_preset data----{data}')
        add_preset(data['type'], data['data'])

    return make_response(jsonify({'status': True}), 200)


# 삭제  preset 저장
@app.route("/del_preset", methods=['POST'])
def delPreset():
    if request.method == 'POST':
        log_print('POST')
        data = request.get_json()
        log_print(f'\n\r ----del_preset data----{data}')
        del_preset(data['type'], data['id'])

    return make_response(jsonify({'status': True}), 200)


# 수정  preset 저장
@app.route("/edit_preset", methods=['POST'])
def editPreset():
    if request.method == 'POST':
        log_print('POST')
        data = request.get_json()
        log_print(f'\n\r ----edit_preset data----{data}')
        edit_preset(data['type'], data['id'], data['data'])

    return make_response(jsonify({'status': True}), 200)


@app.route("/create_prisma", methods=['POST'])
def create_prisma():
    if request.method == 'POST':
        log_print('POST')
        data = request.get_json()
        log_print(f'\n\r ----create_prisma ----{data}')

        id_event = uuid.uuid1()
        id_operation = uuid.uuid1()

        log_print(f'event_id: {id_event.hex}')
        log_print(f'oper_id: {id_operation.hex}')

        ids = data["id"]
        json_event = data["event"]
        json_event['id'] = id_event.hex
        mid_src = json_event['operation']['materialId']

        font_repeat = json_event['operation']['repeat']
        list_field = json_event['operation']['fields']
        font_text = ''
        font_name = ''
        font_speed = 0
        font_size = 0
        for item_field in list_field:
            if item_field['name'] == 'SWF_SPEED':
                font_speed = int(item_field['value'])
            if item_field['name'] == 'SWF_FONT_SIZE':
                font_size = int(item_field['value'])
            if item_field['name'] == 'SWF_TEXT_01':
                font_text = item_field['value']
            if item_field['name'] == 'SWF_FONT_NAME':
                font_name = item_field['value']

        font_duration = 10
        if len(font_text) > 0 and font_speed > 0 and font_size > 0:
            i_repeat = int(font_repeat)
            font_duration = i_repeat * get_duration_text2font(font_text, font_size, font_speed, font_name)
            json_event['operation']['duration'] = font_duration

        json_operation = data["operation"]
        json_operation['id'] = id_operation.hex

        idx = 1

        for x in ids:
            sid = x["sid"]
            epid = x["epid"]

            prisma_Create(sid, epid, json_operation, 'operations')
            prisma_Create(sid, epid, json_event, 'events', idx=idx, mid_src=mid_src)
            idx += 1

    return make_response(jsonify({'status': True}), 200)


if __name__ == '__main__':
    app.run(host="0.0.0.0", port="5000", debug=True)
