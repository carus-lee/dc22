from pymongo import MongoClient
from pymongo.cursor import CursorType
import json
from prisma_init import config_img_dir
from prisma_mongo import insert_item_one, insert_item_many, find_item_id, find_item, log_print, get_mongodb, update_item_one
import gridfs, datetime, requests, time
from flask import send_file
from PIL import Image
from io import BytesIO
from bs4 import BeautifulSoup


init_json_file = './init.json'


def reset_img(mongo, data, db_name=None, collection_name=None):
    result = mongo[db_name][collection_name].delete_many({})
    print(f'delete many -- {result}')
    result = mongo[db_name][collection_name].insert_one(data).inserted_id
    return result


def get_img(name_type):

    mongo = get_mongodb()
    list_img = find_item(mongo, None, 'prisma', 'img')
    data = None
    for item in list_img:
        data = item[name_type]

    return data


def update_item_one(mongo, condition=None, update_value=None, db_name=None, collection_name=None):
    result = mongo[db_name][collection_name].update_one(filter=condition, update=update_value)
    return result


def push_img(svc_id, img):
    mongo = get_mongodb()

    cond = {'_id': svc_id}
    items = mongo['prisma']['img'].find_one(cond)
    # items = find_item_id(mongo, svc_id, 'prisma', 'img')



    print(items)

    if items is None:
        print(f'svc_id({svc_id}) is None')
        fs = gridfs.GridFs(mongo['prisma'])
        fs.put(img, filename=svc_id)

        data = mongo.grid_file.files.find_one({'filename': svc_id})


        dnow = datetime.datetime.now()
        s_now = dnow.strftime("%y/%m/%d %H:%M:%S")

        # def insert_item_one(mongo, data, db_name=None, collection_name=None):
        item = insert_item_one(mongo, {'_id': svc_id, 'date': s_now}, 'prisma', 'img')
        print(f'-----{item}')
    else:
        print(f'svc_id({svc_id}) is {items}')

    # for
    #
    # print(item)
    #
    # item = find_item_id(mongo, svc_id, 'prisma', 'img')

    # print(item)
    # list_img = find_item(mongo, None, 'prisma', 'img')
    #
    # sCond = f''
    # update_item_one(mongo, sCond, sUpdate, )


def con_img(svc_id):
    file_image_dir = config_img_dir()
    url = 'http://localhost:18080/ui/connectors/envivio.unified.liveencoder/2.67.1/ajax/thumbnails/f2a741ede9ee4cc3a0f1fc07c28c20bf/standalone/?time=1661839749831'
    header = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.97 Safari/537.36'}
    cookie = {'sessionid': 'm3t95av946li19yy972nz5cjmkhym7mz', 'csrftoken': 'x3JXSdEasjoetozz5z4MxpGFZpbcPWHNB9ZQ01Yc6D7YbIqFXwMMaNTVURBdogHd'}

    res = requests.get(url=url, headers=header, cookies=cookie)
    bytes_img = Image.open(BytesIO(res.content))

    file_name_img = file_image_dir + '/' + svc_id + '.jpg'
    bytes_img.save(file_name_img)

    d_now = datetime.datetime.now()
    s_now = d_now.strftime("%y/%m/%d %H:%M:%S")

    print(f'{s_now} Loading image ---{bytes_img.size}')


def get_img(ip):
    url=f'http://localhost:18080/ui/connectors/envivio.unified.liveencoder/2.67.1/ajax/thumbnails/f2a741ede9ee4cc3a0f1fc07c28c20bf/standalone/?time=1661839749831'


def send_img_file(svc_id):
    file_image_dir = config_img_dir()
    file_name_img = file_image_dir + '/' + svc_id + '.jpg'
    send_file(file_name_img, mimetype='image/jpeg')


def create_img(svc_id):
    session = requests.Session()

    header = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.97 Safari/537.36'}
    url = 'http://localhost:18080/ui/connectors/envivio.unified.liveencoder/2.67.1/ajax/thumbnails/f2a741ede9ee4cc3a0f1fc07c28c20bf/standalone/?time=1661839749831'
    req_0=requests.get('http://localhost:18080')
    req_cookie=req_0.cookies.get_dict()
    print('cookies...', req_cookie)
    soup = BeautifulSoup(req_0.text, features='html.parser')
    token_csr = soup.find('input', attrs={'name': 'csrfmiddlewaretoken'})
    token_val = token_csr.attrs['value']
    data = {'username': 'admin', 'password': 'admin', 'csrfmiddlewaretoken': token_val}
    url = 'http://localhost:18080/ui/home'

    response = session.post(url, headers=header, data=data, cookies=req_cookie)

    req_cookie = req_0.cookies.get_dict()

    url = 'http://localhost:18080/ui/connectors/envivio.unified.liveencoder/2.67.1/ajax/thumbnails/f2a741ede9ee4cc3a0f1fc07c28c20bf/standalone/?time=1661839749831'
    header = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.97 Safari/537.36'}
    cookie = {'sessionid': 'm3t95av946li19yy972nz5cjmkhym7mz',
              'csrftoken': 'x3JXSdEasjoetozz5z4MxpGFZpbcPWHNB9ZQ01Yc6D7YbIqFXwMMaNTVURBdogHd'}

    res = session.get(url=url, headers=header, cookies=cookie)
    bytes_img = Image.open(BytesIO(res.content))

    file_image_dir = config_img_dir()
    file_name_img = file_image_dir + '/' + svc_id + '.jpg'
    bytes_img.save(file_name_img)

    print('session.cookie ', req_cookie, bytes_img.size)



    # file_image_dir = config_img_dir()
    # url = 'http://localhost:18080/ui/connectors/envivio.unified.liveencoder/2.67.1/ajax/thumbnails/f2a741ede9ee4cc3a0f1fc07c28c20bf/standalone/?time=1661839749831'
    # header = {
    #     'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.97 Safari/537.36'}
    # cookie = {'sessionid': 'm3t95av946li19yy972nz5cjmkhym7mz',
    #           'csrftoken': 'x3JXSdEasjoetozz5z4MxpGFZpbcPWHNB9ZQ01Yc6D7YbIqFXwMMaNTVURBdogHd'}
    #
    # res = requests.get(url=url, headers=header, cookies=cookie)
    # bytes_img = Image.open(BytesIO(res.content))
    #
    # file_name_img = file_image_dir + '/' + svc_id + '.jpg'
    # bytes_img.save(file_name_img)

    d_now = datetime.datetime.now()
    s_now = d_now.strftime("%y/%m/%d %H:%M:%S")

    print(f'{s_now} Loading image ---{token_val}')



def get_ch_info(ip_encoder='localhost', port=8080):
    session = requests.Session()
    url_base = f'http://{ip_encoder}:{port}'

    header = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.97 Safari/537.36'}
    url = f'{url_base}/ui/connectors/envivio.unified.liveencoder/2.67.1/ajax/thumbnails/f2a741ede9ee4cc3a0f1fc07c28c20bf/standalone/?time=1661839749831'

    req_0 = requests.get(f'http://localhost:{port}')
    req_cookie = req_0.cookies.get_dict()
    print('cookies...', req_cookie)

    soup = BeautifulSoup(req_0.text, features='html.parser')
    token_csr = soup.find('input', attrs={'name': 'csrfmiddlewaretoken'})
    token_val = token_csr.attrs['value']

    data = {'username': 'admin', 'password': 'admin', 'csrfmiddlewaretoken': token_val}
    url = f'{url_base}/ui/services'

    response = session.post(url, headers=header, data=data, cookies=req_cookie)

    soup_ch = BeautifulSoup(response.text, features='html.parser')
    list_ch = soup_ch.find('tbody')
    print(response.text)


    # print(response.text)




    # print('session.cookie ', req_cookie, response.text )


def loop_write_img(i_sleep):
    while True:
        con_img('BS02_TS01_ChA')
        time.sleep(i_sleep)
# push_img('BS02_TS01_ChA', '')

# loop_write_img(1)
