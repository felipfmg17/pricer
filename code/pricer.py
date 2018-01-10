import http.client,json,time,pymysql



def downloadResource(host,resource):
    data = None
    headers = {'User-Agent': 'Mozilla/5.0'}
    conn = http.client.HTTPSConnection(host)
    conn.request('GET',resource,'',headers)
    response = conn.getresponse()
    if response.status==200:
        data = response.read()
    return data

def extractBitsoPrice(data):
    price = None
    data = data.decode('utf-8')
    jsonObj = json.loads(data)
    price = jsonObj['payload']['last']
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

    print(sql)
    cursor = db.cursor()
    cursor.execute(sql)
    db.commit()






def test1():
    data = downloadResource('api.bitso.com','/v3/ticker/?book=xrp_mxn')
    price = extractBitsoPrice(data)
    print(price)

def test2():
    db = createDBConnection('localhost','root','root','crypto_prices')
    id = savePriceBD('bitso','xrp_mxn',1717,db)
    print(id)

test2()


