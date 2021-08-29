import requests
import json
import time
import datetime
import pandas as pd

#ensuring correct black-scholes inputs
def handle_volatility():
  '''Repeatedly asks user to input a floating volatilility until a valid input is given

  :return: (float) Valid volatility input
  '''
  volatility_given = False
  while  not volatility_given:
    try:
      volatility = float(input('Enter the implied volatility of the asset as a decimal (e.g. 0.2 represents 20%)'))
      if volatility>0:
        volatility_given = True
      else:
        print('You need to enter a positive value for volatility')
    except Exception as e:
      print('You need to give a floating value for volatility',e)
  return volatility

def handle_strike():
  '''Repeatedly asks user to input a floating strike price until valid strike price is given

  :return: (float) Valid strike price
  '''
  strike_given = False
  while  not strike_given:
    try:
      strike = float(input('Enter the strike value'))
      if strike>0:
        strike_given = True
      else:
        print('You need to enter a positive value for strike')
    except Exception as e:
      print('You need to give a floating value for strike',e)
  return strike

#ensuring correct expiration date input
def handle_expiration_date():
  ''' Repeatedly asks user to input a future expiration date until a valid expiration date is given

  :return: (int) Valid expiration date in seconds
  '''
  this_year = datetime.datetime.now().year
  this_month = datetime.datetime.now().month
  this_day = datetime.datetime.now().day
  todays_date = datetime.date(this_year, this_month, this_day)
  date_given = False
  while not date_given:
    try:
      exp_year = int(input('Enter the expiration year in the form YYYY'))
      exp_month = int(input('Enter the expiration day in the form MM'))
      exp_day = int(input('Enter the expiration day in the form DD'))
      exp_date = datetime.date(exp_year, exp_month, exp_day)
      exp_date_in_seconds = int(time.mktime(exp_date.timetuple()))
      if exp_date>=todays_date:
        date_given = True
      else:
        print('You need to enter a date in the future (today onwards)')
    except Exception as e:
      print('Expiry date needs to be an existing future date of the form YYYY-MM-DD',e)
  return exp_date, exp_date_in_seconds

def handle_risk_free_rate():
  '''Repeatedly asks user to input a floating risk-free interest rate until a valid interest rate is given

  :return: (float) Valid risk-free interest rate
  '''
  risk_free_rate_given = False
  while  not risk_free_rate_given:
    try:
      risk_free = float(input('Enter the current risk free rate of interest as a decimal (e.g. 0.2 represents 20%)'))
      if risk_free>0:
        risk_free_rate_given = True
      else:
        print('You need to enter a positive value for the risk free interest rate')
    except Exception as e:
      print('You need to give a floating value for the risk free interest rate',e)
  return risk_free

#Ensuring correct ticker input
def handle_ticker():
  '''Repeatedly asks user to input a ticker until a valid ticker is given.
  Validity is determined by searching the web to check if such a ticker exists.

  :return: (str) Valid ticker
  '''
  ticker_given = False
  while not ticker_given:
    try:
      ticker = str(input('Enter a ticker'))
      today_in_seconds = int(time.mktime(datetime.date(datetime.datetime.now().year,datetime.datetime.now().month,datetime.datetime.now().day).timetuple()))
      interval = '1d'
      query_string = f'https://query1.finance.yahoo.com/v7/finance/download/{ticker}?period1={today_in_seconds-1*24*60*60}&period2={today_in_seconds}&interval={interval}&events=history&includeAdjustedClose=true'
      df = pd.read_csv(query_string)
      ticker_given = True
    except Exception as e:
      print(e,'Ticker cannot be found')
  return ticker

BASE = 'http://127.0.0.1:5000/'

exit = False
while not exit:
  try:
    play = str(input("Press 'Y' to run the program, and 'N' to exit the program"))
    if play == 'Y' or play.lower() == 'y':
      #user inputs
      ticker = handle_ticker()
      expiration_date_in_seconds = handle_expiration_date()[1]
      strike = handle_strike()
      volatility = handle_volatility()
      risk_free_rate = handle_risk_free_rate()

      #calculate time to expiration
      today = int(time.mktime(datetime.date.today().timetuple()))
      seconds_in_a_day = 24*60*60
      yesterday = today - seconds_in_a_day
      days_in_a_year = 365
      time_to_expiration = ((expiration_date_in_seconds - today)/(seconds_in_a_day))/days_in_a_year

      #turning today, yesterday into strings for query
      today = str(today)
      yesterday = str(yesterday)

      #viewing resulting call option
      # result = requests.get(BASE + 'stock/' + ticker + '/' + yesterday + '/' + today + '/' + str(strike) + '/'+ str(time_to_expiration) + '/' + str(volatility))
      result = requests.get(f'{BASE}stock/{ticker}/{yesterday}/{today}/{strike}/{time_to_expiration}/{volatility}/{risk_free_rate}')
      print('call of',ticker,'asset at strike price of',strike,'and time to maturity of',time_to_expiration,'years: $',result.json()['call'])
    elif play=='N' or play.lower()=='n':
      print('Goodbye!')
      exit = True
    else:
      print('You need to enter either Y or N')
  except Exception as e:
    print('Incorrect input. Try again', e)