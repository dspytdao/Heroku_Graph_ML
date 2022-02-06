from app import app

from flask import Flask, request, jsonify
import requests
import json
import pandas as pd
import numpy as np
from statsmodels.tsa.arima.model import ARIMA

url ='https://api.thegraph.com/subgraphs/name/uniswap/uniswap-v3'

@app.route("/", methods=["GET","POST"])
def home():
    if request.args.get('f'):
        f = int(request.args.get('f'))
    else:
        f=15
    if request.args.get('a'):
        address = request.args.get('a')
    else:
        address = "0x1f9840a85d5af5bf1d1762f925bdaddc4201f984"
    
    query = """
        {token (id: "%s"){tokenDayData { priceUSD date } } }
        """ % address
    
    r = requests.post(url, json={'query': query})
    json_data = json.loads(r.text)
    
    df_data = json_data['data']['token']['tokenDayData']
    df = pd.DataFrame(df_data)

    df.priceUSD = df.priceUSD.replace(0, np.nan).dropna()
    df.priceUSD = df.priceUSD.astype(float)

    last = df.date.iloc[-1:].values[0]
    timestep = df.date.iloc[-1:].values[0]-df.date.iloc[-2:-1].values[0]
    model = ARIMA(df.priceUSD, order=(1,1,0))
    fitted = model.fit()
    # Forecast
    fc = fitted.forecast(f)

    return jsonify({'predictions': list(fc), 'last_date': str(last), 'timestep': str(timestep)})
