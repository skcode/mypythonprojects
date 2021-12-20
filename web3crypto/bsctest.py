
from web3 import Web3
import requests
import time, json
from eth_abi import encode_abi, decode_abi
from hexbytes import HexBytes
#https://bscscan-python.pankotsias.com/bscscan.modules.html

address = '0xA499dEEc5c59d813f40B823a73dF3044E62B91Bb'

BinanceExchangeKeys = {
    "apiKey": 'Uq628P6Xk6AefNd7R4I23xeAlSOcEztugt9PPQOf2GcO9OHXf0LkcQZ783hMJ85l',
    "secret": 'CtWmB8gilBNpKmMAbZcr2d9OKSfWjyFg4qMYmS6etxMrPKVCTADfZzkQRCZzwCqr'
}


TokenAddress={'BUSD': '0xe9e7cea3dedca5984780bafc599bd69add087d56'}
###########
from  bscscan import BscScan
from bscscan.utils.conversions import Conversions
import asyncio
bscscanAPI = "RS6VFRXAZZZI41PT65PV8Z3CSHRX2RPGDP"

async def get_bsc_bnb_balance(address):
  async with BscScan(bscscanAPI) as bsc:
    res = await bsc.get_bnb_balance(address=address)
    return Conversions.to_ticker_unit(res, decimals=18)

async def get_bsc_all_bep20(address):
    async with BscScan(bscscanAPI) as client:
        return await client.get_bep20_token_transfer_events_by_address(
            address=address,
            startblock=0,
            endblock=999999999,
            sort="asc"
        )
async def get_bsc_all_bep721(address):
    async with BscScan(bscscanAPI) as client:
        return await client.get_bep721_token_transfer_events_by_address(
            address=address,
            startblock=0,
            endblock=999999999,
            sort="asc"
        )

print("BNB amount on BSC: ",asyncio.run(get_bsc_bnb_balance(address)))
lst=asyncio.run(get_bsc_all_bep20(address))
import pandas as pd

data=pd.DataFrame()
cnt=0
for l in lst:
    t1=pd.DataFrame(l,index=[cnt])
    if data.empty:
        data=t1
    else:
        data=pd.concat([data,t1],axis=0)
    cnt=cnt+1
    print ("from ",l['from']," to ", l['to'])
    print("value ",Conversions.to_ticker_unit(int(l['value']),int(l['tokenDecimal'])),' token ',l['tokenSymbol'])

print("################")
print(data)
print(data.columns)
data.to_csv('~/out.csv',index=False)
async def get_contractABI(address):
    async with BscScan(bscscanAPI) as client:
        print(
            await client.get_contract_abi(contract_address=address)
        )

async def get_normal_transactions(address):
    async with BscScan(bscscanAPI) as client:
        return await client.get_normal_txs_by_address(
                address=address,
                startblock=0,
                endblock=99999999,
                sort="asc"
        )

lst=asyncio.run(get_normal_transactions(address))
data=pd.DataFrame()
cnt=0
for l in lst:
    t1=pd.DataFrame(l,index=[cnt])
    if data.empty:
        data=t1
    else:
        data=pd.concat([data,t1],axis=0)
    cnt=cnt+1

print("################")
print(data)
print(data.columns)
data.to_csv('~/outnorm.csv',index=False)

from bs4 import BeautifulSoup
import requests

url_base = 'https://api.bscscan.com/api?module=stats&action=tokensupply&contractaddress='
contract = '0x10ED43C718714eb63d5aA57B78B54704E256024E'
url_fin = '&apikey='+bscscanAPI
url = url_base+contract+url_fin

page = requests.get(url)
soup = BeautifulSoup(page.content, 'html')