"""main file"""
import json
from flask import request, jsonify

import requests

import pandas as pd
import numpy as np
from statsmodels.tsa.arima.model import ARIMA

from app import app

URL ='https://api.thegraph.com/subgraphs/name/uniswap/uniswap-v3'


@app.route("/", methods=["GET","POST"])
def home():
    """default"""
    if request.args.get('f'):
        forward_steps = int(request.args.get('f'))
    else:
        forward_steps=15
    if request.args.get('a'):
        address = request.args.get('a')
    else:
        address = "0x1f9840a85d5af5bf1d1762f925bdaddc4201f984"

    query = f"""
        {{token (id: "{address}"){{tokenDayData {{ priceUSD date }} }} }}
        """

    response = requests.post(URL, json={'query': query})
    json_data = json.loads(response.text)

    in_df_data = json_data['data']['token']['tokenDayData']
    df_out = pd.DataFrame(in_df_data)

    df_out.priceUSD = df_out.priceUSD.replace(0, np.nan).dropna()
    df_out.priceUSD = df_out.priceUSD.astype(float)

    last = df_out.date.iloc[-1:].values[0]
    timestep = df_out.date.iloc[-1:].values[0]-df_out.date.iloc[-2:-1].values[0]
    model = ARIMA(df_out.priceUSD, order=(1,1,0))
    fitted = model.fit()
    # Forecast
    forecast = fitted.forecast(forward_steps)
    forecast = list(forecast)
    return jsonify({'predictions': forecast, 'last_date': str(last), 'timestep': str(timestep)})
