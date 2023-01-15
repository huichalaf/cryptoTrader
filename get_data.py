import requests as rq
import pandas as pd
from finta import TA
import numpy as np
import sys

def getData(symbol):
    
    try:
        data = pd.DataFrame()
        #aqui hay que obtener los datos de cotizacion y tenerlos en un dataframe con las claves: close, open, high, low, volume
    except Exception as e:
        print(e)
        sys.exit()

    rsi = np.array(TA.RSI(data, 9))[-1]
    adx = np.array(TA.ADX(data, 9))[-1]
    volume = np.array(data['volume'])[-1]
    volumeAvg = np.mean(np.array(data['volume']))
    price = float(np.array(data['close'])[-1])
    last_price = float(np.array(data['close'])[-2])
    
    return {'rsi': rsi,'adx': adx, 'volume': volume/volumeAvg, 'price': price, 'last_price': last_price}
