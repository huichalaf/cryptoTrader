import pandas as pd
import os
from keras.models import load_model
from get_data import getData
import numpy as np

files = os.listdir('dataCsv/')

def get_dataframe(file_name) -> pd.DataFrame:
    df = pd.read_csv(f'dataCsv/{file_name}')
    return df

class desition_maker:

    def __init__(self):
        self.pares = []
        self.mayor = ''
        self.menor = ''
        self.volumeNormalized1 = 0
        self.volumeNormalized2 = 0
        self.adx1 = 0
        self.adx2 = 0
        self.rsi1 = 0
        self.rsi2 = 0
        self.spread_std = 0

    def add_data(self, volumeNormalized, volumeNormalized2, adx1, adx2, rsi1, rsi2, spread_std):
        self.volumeNormalized1 = volumeNormalized
        self.volumeNormalized2 = volumeNormalized2
        self.adx1 = adx1
        self.adx2 = adx2
        self.rsi1 = rsi1
        self.rsi2 = rsi2
        self.spread_std = spread_std

    def predict(self):
        self.prediction = model.predict(np.array([[self.volumeNormalized1, self.volumeNormalized2, self.adx1, self.adx2, self.rsi1, self.rsi2, self.spread_std]]))
        return self.prediction > 0.9


dMaker = desition_maker()
model = load_model('main.h5')
predicciones = {}

for file in files:
    
    lista = file.split('_')
    dataFrame = get_dataframe(file)

    data1 = getData(lista[0])
    data2 = getData(lista[1])
    
    price1 = data1['price']
    price2 = data2['price']
    last_price1 = data1['last_price']
    last_price2 = data2['last_price']

    spread_std = (price1 - price2)/float(dataFrame['std'][0])
    last_spread_std = (last_price1 - last_price2)/float(dataFrame['std'][0])

    if (last_spread_std >= 0 and spread_std < 0) or (last_spread_std <= 0 and spread_std > 0):
        prediccion = -1
    else:
        dMaker.add_data(data1['volume'], data2['volume'], data1['adx'], data2['adx'], data1['rsi'], data2['rsi'], spread_std)
        prediccion = dMaker.predict()
    
    print(file, int(prediccion))
    name = str(lista[0])+'_'+str(lista[1])
    predicciones[name] = int(prediccion)