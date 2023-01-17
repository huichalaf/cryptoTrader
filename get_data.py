import requests as rq
import pandas as pd
from finta import TA
import numpy as np
import sys, os
import binance

def sortDictToDataframe(file_name, data):
    
    OpenTime = []
    open = []
    high = []
    low = []
    close = []
    volume = []
    closeTime = []
    quoteVolume = []
    numTrades = []

    for i in data:
        OpenTime.append(i['openTime'])
        open.append(i['open'])
        high.append(i['high'])
        low.append(i['low'])
        close.append(i['close'])
        volume.append(i['volume'])
        closeTime.append(i['closeTime'])
        quoteVolume.append(i['quoteVolume'])
        numTrades.append(i['numTrades'])

    df = pd.DataFrame()
    df['openTime'] = list(reversed(OpenTime))
    df['open'] = list(reversed(open))
    df['high'] = list(reversed(high))
    df['low'] = list(reversed(low))
    df['close'] = list(reversed(close))
    df['volume'] = list(reversed(volume))
    df['closeTime'] = list(reversed(closeTime))
    df['quotevolume'] = list(reversed(quoteVolume))
    df['numTrades'] = list(reversed(numTrades))
    df.to_csv(file_name)
    
    return df

def getData(symbol, periodo):
    
    try:
        file_name = f'{symbol}_data.csv'
        data = binance.klines(symbol, periodo)
        data_ready = sortDictToDataframe(file_name, data)
    except Exception as e:
        print(e)
        sys.exit()
    data_ready = pd.read_csv(file_name)
    #print(data_ready)
    rsi = np.array(TA.RSI(data_ready, 9))[-1]
    adx = np.array(TA.ADX(data_ready, 9))[-1]
    volume = np.array(data_ready['volume'])[0]
    volumeAvg = np.mean(np.array(data_ready['volume']))
    price = float(np.array(data_ready['close'])[0])
    last_price = float(np.array(data_ready['close'])[1])
    os.system(f'mv {file_name} priceData/')
    
    return {'rsi': rsi,'adx': adx, 'volume': volume/volumeAvg, 'price': price, 'last_price': last_price, 'pureData': data_ready}
