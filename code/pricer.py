import http.client,json,time,pymysql,logging,threading

def downloadResource(host,resource):
    data = None
    headers = {'User-Agent': 'Mozilla/5.0'}
    conn = http.client.HTTPSConnection(host)
    conn.request('GET',resource,'',headers)
    response = conn.getresponse()
    data = response.read()
    return data

def bitsoPriceExtractor(data):
    price = None
    data = data.decode('utf-8')
    jsonObj = json.loads(data)
    price = jsonObj['payload']['last']
    return price

def bitfinexPriceExtractor(data):
    price = None
    data = data.decode('utf-8')
    jsonString = json.loads(data)
    price = jsonString['last_price']
    return price

def binancePriceExtractor(data):
    price = None
    data = data.decode('utf-8')
    jsonObj = json.loads(data)
    price = jsonObj['lastPrice']
    return price


def createDBConnection(host,user, password, db_name):
    db = pymysql.connect(host,user,password,db_name)
    return db

def savePriceBD(exchange, cur_pair, price, db):
    cursor = db.cursor()
    sql = 'select id from currency_pair where name = \"' + cur_pair + '\"'
    cursor.execute(sql)
    data = cursor.fetchone()[0]
    cursor.close()
    cur_pair_id = data
    cursor = db.cursor()
    sql = 'select id from exchange where name = \"' + exchange + '\"'
    cursor.execute(sql)
    data = cursor.fetchone()[0]
    exchange_id = data
    cursor.close()
    cursor = db.cursor()
    sql = 'select id from price_type where name = \"last\"'
    cursor.execute(sql)
    data = cursor.fetchone()[0]
    price_type = data
    cursor.close()

    sql = 'insert into coin_price(date_time_sec, exchange_id, currency_pair_id, price, date_time, price_type_id) '
    sql = sql + 'values('
    sql = sql + str( time.time() )+ ', '
    sql = sql + str( exchange_id ) + ', '
    sql = sql + str( cur_pair_id ) + ', '
    sql = sql + str( price ) + ', '
    sql = sql + 'NOW(), '
    sql = sql + str( price_type) + ')'

    cursor = db.cursor()
    cursor.execute(sql)
    db.commit()

def startDownload(host,resource,exchange,cur_pair,pause,db,extractor):
    number = 1
    while True:
        try:
            data = downloadResource(host,resource)
            price = extractor(data)
            savePriceBD(exchange, cur_pair, price, db);
            print('Download successfull ' + str(number) + ': ' ,host+resource)
            number += 1
        except Exception as err:
            print(threading.current_thread().name, 'Error', host+resource )
            logging.exception(err)
        time.sleep(pause)

def startMultiDownload():
    print('Type next Mysql params -  host user password dbName: ')
    db_params = input().split()
    print('Type amount of resources: ')
    nums_requests = int(input())
    ths = []
    for i in range(nums_requests):
        db = createDBConnection(*db_params)
        print('Type params for resource number ' + str(i+1) + ' : host resource exchange currencyPair pause: ')
        req = input().split()
        req[4] = int(req[4])
        args = ( *req, db, exts[req[2]] )
        th = threading.Thread(target=startDownload, args=args )
        th.start()
        ths.append(th)
    for th in ths:
        th.join()


exts = {}
exts['bitso'] = bitsoPriceExtractor
exts['bitfinex'] = bitfinexPriceExtractor
exts['binance'] = binancePriceExtractor

startMultiDownload()


