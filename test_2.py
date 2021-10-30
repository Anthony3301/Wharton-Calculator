import yfinance as yf
import FundamentalAnalysis as fa
import numpy as np
import pandas as pd


def EOY_values(ticker):
    data_2016 = yf.download(ticker, start='2016-12-30', end='2017-01-02')["Close"][0]
    data_2017 = yf.download(ticker, start='2017-12-29', end='2018-01-02')["Close"][0]
    data_2018 = yf.download(ticker, start='2018-12-29', end='2019-01-02')["Close"][0]
    data_2019 = yf.download(ticker, start='2019-12-31', end='2020-01-02')["Close"][0]
    data_2020 = yf.download(ticker, start='2020-12-31', end='2021-01-02')["Close"][0]


    values = [data_2020, data_2019, data_2018, data_2017, data_2016]

    return values

def latest_price(ticker):
    data_curr = yf.download(ticker, period='5d')["Close"][-1]

    return data_curr
