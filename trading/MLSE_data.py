import datetime as datetime
import logging
import time
import hashlib
import matplotlib.pyplot as plt
import requests
import json
import pytz
import numpy as np
import pandas as pd
from bs4 import BeautifulSoup
import sqlite3
from sqlite3 import Error
database = r"./db/quotes.db"

def fetch_MLSE_last_intraday_quotes(code: str) -> pd.DataFrame:
    url = "https://charts.borsaitaliana.it/charts/services/ChartWService.asmx/GetPricesWithVolume"
    stringaintraday = '{"request":{"SampleTime":"1mm","TimeFrame":"1d","RequestedDataSetType":"ohlc","ChartPriceType":"ohlc","Key":\
        "' + code + '","Keys":[],"OffSet":0,"FromDate":null,"ToDate":null,"UseDelay":false,"KeyType":"Topic",' \
                    '"KeyType2":"Topic","Language":"it-IT"}} '
    r = doPostUrl(url,json.loads(stringaintraday))# requests.post(url, json=json.loads(stringaintraday))
   # cnt = 0
   # while r.status_code != 200 and cnt < 30:
   #     r = requests.post(url, json=json.loads(stringaintraday))
   #     time.sleep(1)
   #     cnt = cnt + 1
   # if r.status_code != 200:
   #     raise RuntimeError("cannot fetch " + code)
    arr = np.array(r.json().get('d'))
    df = pd.DataFrame(arr[:, 2:], index=arr[:, 0], columns=['o', 'h', 'l', 'c', 'v'])
    # df.index=df.index.map(lambda x : datetime.datetime.fromtimestamp(x/1000,tz=pytz.timezone('Europe/Rome')))
    df.index = df.index.map(lambda x: datetime.datetime.fromtimestamp(x / 1000 - 3600, tz=pytz.timezone('Europe/Rome')))
    df['oi'] = 0
    return df

def doPostUrl(url: str, jsonpar : json, retries: int = 10) -> requests.models.Response:
    response = requests.post(url,json=jsonpar)
    cnt = 0
    while response.status_code == 429 and cnt < retries:
        secwait = int(response.headers["Retry-After"])
        if secwait > 0:
            time.sleep(int(response.headers["Retry-After"]))
        else:
            time.sleep(1)
        response = requests.post(url,json=jsonpar)
        cnt = cnt + 1
    cnt = 0
    while response.status_code != 200 and cnt < retries:
        response = requests.post(url, json=jsonpar)
        cnt = cnt + 1
    if response.status_code != 200:
        raise RuntimeError("error n. " + str(response.status_code) + " fetching " + url)
    return response


def fetch_MLSE_eod_quotes(code: str) -> pd.DataFrame:
    url = "https://charts.borsaitaliana.it/charts/services/ChartWService.asmx/GetPricesWithVolume"
    stringaeod = '{"request":{"SampleTime":"1d","TimeFrame":"10y","RequestedDataSetType":"ohlc","ChartPriceType":"price","Key":\
        "' + code + '","OffSet":0,"FromDate":null,"ToDate":null,"UseDelay":true,"KeyType":"Topic","KeyType2":"Topic","Language":"it-IT"}}'
    #r = requests.post(url, json=json.loads(stringaeod))
    #cnt = 0
    #while r.status_code != 200 and cnt < 30:
    #    r = requests.post(url, json=json.loads(stringaeod))
    #    time.sleep(1)
    #    cnt = cnt + 1
    #if r.status_code != 200:
    #    raise RuntimeError("cannot fetch " + code)
    r=doPostUrl(url,json.loads(stringaeod))
    arr = np.array(r.json().get('d'))
    df = pd.DataFrame(arr[:, 2:], index=arr[:, 0], columns=['o', 'h', 'l', 'c', 'v'])
    # df.index=df.index.map(lambda x : datetime.datetime.fromtimestamp(x/1000,tz=pytz.timezone('Europe/Rome')))
    df.index = df.index.map(lambda x: datetime.datetime.fromtimestamp(x / 1000 - 3600, tz=pytz.timezone('Europe/Rome')))
    df['oi'] = 0
    return df


def fetch_MLSE_list() -> list:
    # "https://www.borsaitaliana.it/borsa/azioni/global-equity-market/scheda/BE0974264930.html?lang=it"
    # urldet = "https://www.borsaitaliana.it/borsa/azioni/dati-completi.html?isin=IT0001233417&lang=en"
    # https://www.borsaitaliana.it/borsa/azioni/global-equity-market/dati-completi.html?isin=BE0974264930&lang=it
    stock_listurl = []
    ascii_uppercase = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'
    idxchar = 0
    idxpage = 1
    while (True):
        print(
            "ascii " + ascii_uppercase[idxchar] + " page " + str(idxpage) + "\tcurrent len " + str(len(stock_listurl)))
        urllist = "https://www.borsaitaliana.it/borsa/azioni/listino-a-z.html?initial=" + ascii_uppercase[
            idxchar] + "&page=" + str(idxpage) + "&lang=en"
        r = fetchUrl(urllist)
        # soup = BeautifulSoup(r.text, 'html.parser')
        soup = BeautifulSoup(r.text, features="lxml")
        if r.status_code != 200:
            print("warn: error no " + str(r.status_code) + " fetching " + urllist)
            time.sleep(1)
            continue
        # l = soup.find_all('a', class_="u-hidden -xs")
        for link in soup.find_all('a'):
            if str(link.get('href')).__contains__("scheda"):
                stock_listurl.append(link.get('href'))
        pr = soup.find('span', class_="m-icon -pagination-right")
        if pr is None and ascii_uppercase[idxchar] == 'Z':
            break
        if pr is not None:
            idxpage = idxpage + 1
        else:
            idxpage = 1
            idxchar = idxchar + 1
        # time.sleep(1)
    stock_listurl = list(dict.fromkeys(stock_listurl))  # remove dupes
    return stock_listurl


def fetch_MLSE_ETF_list() -> list:
    idxpage = 1
    etf_listurl = []
    while (True):
        print("fetching page " + str(idxpage))
        urllist = "https://www.borsaitaliana.it/borsa/etf/search.html?comparto=ETF&idBenchmarkStyle=&idBenchmark" \
                  "=&indexBenchmark=&sectorization=&lang=en&page=" + str(
            idxpage)
        r = requests.get(urllist)
        # soup = BeautifulSoup(r.text, 'html.parser')
        soup = BeautifulSoup(r.text, features="lxml")
        if r.status_code != 200:
            print("warn: error no " + str(r.status_code) + " fetching " + urllist)
            time.sleep(1)
            continue
        cnt = 0
        for link in soup.find_all('a'):
            if str(link.get('href')).__contains__("scheda"):
                etf_listurl.append(link.get('href'))
                cnt = cnt + 1
                # print(stock_listurl[-1])
        if cnt == 0:
            break
        else:
            idxpage = idxpage + 1
        print(len(etf_listurl))
        # time.sleep(1)
    etf_listurl = list(dict.fromkeys(etf_listurl))  # remove dupes
    return etf_listurl


def details_url(url: str) -> str:
    base = "https://www.borsaitaliana.it"
    idxazioni, idxetf, idxetcn = -1, -1, -1
    try:
        idxazioni = str(url).index('azioni')
    except:
        pass
    try:
        idxetf = str(url).index('etf')
    except:
        pass
    try:
        idxetcn = str(url).index('etc-etn')
    except:
        pass
    idx = str(url).index('scheda')
    if idxazioni > 0:
        deturl = base + str(url)[:idx] + "dati-completi.html?isin=" + str(url)[idx + 7:idx + 19] + "&lang=en"
    elif idxetf > 0:
        deturl = base + str(url)[:idx] + "dettaglio.html?isin=" + str(url)[idx + 7:idx + 19] + "&lang=en"
    elif idxetcn > 0:
        deturl = base + str(url)[:idx] + "dettaglio.html?isin=" + str(url)[idx + 7:idx + 19] + "&lang=en"
    else:
        raise RuntimeError('bad index')
    return deturl


def fetchUrl(url: str, retries: int = 10) -> requests.models.Response:
    response = requests.get(url)
    cnt = 0
    while response.status_code == 429 and cnt < retries:
        secwait = int(response.headers["Retry-After"])
        if secwait > 0:
            time.sleep(int(response.headers["Retry-After"]))
        else:
            time.sleep(1)
        response = requests.get(url)
        cnt = cnt + 1
    cnt = 0
    while response.status_code != 200 and cnt < retries:
        response = requests.get(url)
        cnt = cnt + 1
    if response.status_code != 200:
        raise RuntimeError("error n. " + str(response.status_code) + " fetching " + url)
    return response





def get_dict_info_from_details_url(url: str) -> dict:
    response = fetchUrl(url)
    table_MN = pd.read_html(response.content)
    z1 = table_MN[1].set_index(table_MN[1].columns[0]).to_dict()[1]
    z2 = table_MN[2].set_index(table_MN[1].columns[0]).to_dict()[1]
    if len(table_MN) > 3:
        z3 = table_MN[3].set_index(table_MN[1].columns[0]).to_dict()[1]
    z = dict()
    z.update(z1)
    z.update(z2)
    if len(table_MN) > 3:
        z.update(z3)
    del z["Legenda"]
    soup = BeautifulSoup(response.text, features="lxml")
    title = soup.find('h1', {'class': "t-text -flola-bold -size-xlg -inherit"})
    z['name'] = title.find_all_next('a')[0].text
    print(z)
    return z


def fetch_MLSE_details():
    # etf details
    l = fetch_MLSE_ETF_list()
    a_list = []
    for k in l:
        try:
            d = get_dict_info_from_details_url(details_url(k))
            a_list.append(d)
        except Exception as e:
            logging.log(logging.WARN, e)
    with open("etf_details.txt", "w") as textfile:
        json.dump(a_list, fp=textfile)
    # stock details
    l = fetch_MLSE_list()
    a_list = []
    for k in l:
        try:
            d = get_dict_info_from_details_url(details_url(k))
            a_list.append(d)
        except Exception as e:
            logging.log(logging.WARN, e)
    with open("stock_details.txt", "w") as textfile:
        json.dump(a_list, fp=textfile)


def create_connection(db_file):
    """ create a database connection to the SQLite database
        specified by db_file
    :param db_file: database file
    :return: Connection object or None
    """
    conn = None
    try:
        conn = sqlite3.connect(db_file)
        return conn
    except Error as e:
        print(e)
    return conn


def create_table(conn, create_table_sql):
    """ create a table from the create_table_sql statement
    :param conn: Connection object
    :param create_table_sql: a CREATE TABLE statement
    :return:
    """
    try:
        c = conn.cursor()
        c.execute(create_table_sql)
    except Error as e:
        print(e)


def create_database(database_file: str):
    sql_table = """ CREATE TABLE IF NOT EXISTS quotes (
                                        hash text PRIMARY KEY,
                                        isin text NOT NULL,
                                        name text NOT NULL,
                                        code text NOT NULL,                                                                                
                                        market text NOT NULL,
                                        type text NOT NULL,
                                        currency text NOT NULL,
                                        notes text,
                                        eoddata text                                        
                                    ); """
    conn = create_connection(database_file)
    # create tables
    if conn is not None:
        create_table(conn, sql_table)
    else:
        print("Error! cannot create the database connection.")


def insert_record(conn, values: list):
    """
    Create a new record into the quotes table
    :param conn:
    :param values:
    :return: record id
    """
    sql = ''' INSERT OR REPLACE INTO quotes(hash,isin,name, code, market,type,currency,notes,eoddata)
              VALUES(?,?,?,?,?,?,?,?,?) '''
    cur = conn.cursor()
    cur.execute(sql, values)
    conn.commit()
    return cur.lastrowid


def md5_hash(s: str) -> str:
    hash_object = hashlib.md5(bytes(s, 'UTF-8'))
    return hash_object.hexdigest()


def load_data(database_file: str):
    create_database(database_file)
    conn = create_connection(database_file)
    with open("etf_details.txt", "r") as read_file:
        lst = json.load(read_file)
    for x in lst:
        try:
            name = x['name']
            stype = 'ETF'
            isin = x['Isin Code']
            code = x['Alphanumeric Code']
            market = 'MLSE'
            currency = 'EUR'
            notes = json.dumps(x)
            eoddata = fetch_MLSE_eod_quotes(code + ".ETF")
            hash = md5_hash(str(isin + code + market))
            values = [hash, isin, name, code, market, stype, currency, notes, eoddata.to_json()]
            insert_record(conn, values)
            print(values[0:len(values) - 1])
            print('*' * 20)
        except Exception as e:
            print("cannot insert " + isin)
            print(e)
    with open("stock_details.txt", "r") as read_file:
        lst = json.load(read_file)
    for x in lst:
        try:
            name = x['name']
            stype = 'STOCK'
            isin = x['Isin Code']
            code = x['Alphanumeric Code']
            market = 'MLSE'
            currency = 'EUR'
            notes = json.dumps(x)
            eoddata = fetch_MLSE_eod_quotes(code + ".MTA")
            hash = md5_hash(str(isin + code + market))
            values = [hash, isin, name, code, market, stype, currency, notes, eoddata.to_json()]
            insert_record(conn, values)
            print(values[0:len(values) - 1])
            print('*' * 20)
        except Exception as e:
            print("cannot insert " + isin)
            print(e)


def get_EOD_dataframe(code: str, database_file=database) -> pd.DataFrame:
    return pd.read_json(query2dataframe('code="' + code + '"').loc[0, 'eoddata'])


def query2dataframe(where_cond: str, database_file=database) -> pd.DataFrame:
    conn = create_connection(database_file)
    query = 'select * from quotes where ' + where_cond
    sql_query = pd.read_sql_query(query, conn)
    return pd.DataFrame(sql_query)


def queryDB(query: str, database_file=database) -> sqlite3.Cursor:
    conn = create_connection(database_file)
    cursor = conn.cursor()
    rows = cursor.execute(query).fetchall()
    return rows


if __name__ == "__main__":
    #fetch_MLSE_details()
    #load_data(database)
    df=query2dataframe('type="STOCK"')
    for x in df.values:
        p=pd.read_json(x[-1])
        print(p)



