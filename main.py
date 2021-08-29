import pandas as pd
import time
import datetime
from flask import Flask
from flask_restful import Api,Resource
from scipy.stats import norm
import numpy as np
import requests

app = Flask(__name__)
api = Api(app)

#calculate European call option
def black_scholes(stock,strike,time_to_expiration,risk_free,volatility):
    if strike>=stock:
        call = 0
    else:
      d1 = (np.log(stock/strike) + (risk_free + (volatility**2/2))*time_to_expiration)/(volatility*np.sqrt(time_to_expiration))
      d2 = d1 - volatility*np.sqrt(time_to_expiration)
      call = norm.cdf(d1)*stock - norm.cdf(d2)*strike*np.exp(-(risk_free*time_to_expiration))
    return call

class Stock_Option(Resource):
    def get(self,ticker,yesterday,today,strike,time_to_expiration,volatility,risk_free_rate):
        query_string = f'https://query1.finance.yahoo.com/v7/finance/download/{ticker}?period1={yesterday}&period2={today}&interval=1d&events=history&includeAdjustedClose=true'
        df = pd.read_csv(query_string)
        stock = float(df.Close[len(df.Close)-1])
        call = black_scholes(stock,strike,time_to_expiration,risk_free_rate,volatility)
        return {'call':call}

api.add_resource(Stock_Option,'/stock/<string:ticker>/<string:yesterday>/<string:today>/<float:strike>/<float:time_to_expiration>/<float:volatility>/<float:risk_free_rate>')

if __name__=="__main__":
   app.run(debug=False)