# -*- coding: utf-8 -*-
"""
Created on Mon Jan  8 11:44:08 2018

@author: Alice Duval

Prices are in $/mt (in 2017 US dollars and metric ton) for Coal based on Australian prices and
in $/mmbtu for Gas based on Japan prices.

Data come from World Bank database

ISSUE TO SOLVE : These prices are smaller than local prices
"""

import numpy as np
from scipy.stats import norm
from init import pd, start_year, end_year, t, MBtu, Calo_coal_international


#definition of X functions to determine the correlation factor
def x_function(prices):
    "Define a sequence used in correlation factor calculation"
    x_list = []
    for i in range(len(prices)):
        if i < len(prices)-1:
            x_list.append(np.log(prices[i] / prices[i+1]))
    return x_list

def average_coeff(x_function):
    "Calculate the average of x_function sequence"
    return  1 / len(x_function) * np.sum(x_function)

def realized_pairwise_correlation(gas, coal):
    "Calculate the correlation factor of past data"
    x_gas = x_function(gas)
    x_coal = x_function(coal)
    av_gas = average_coeff(x_gas)
    av_coal = average_coeff(x_coal)
    coef_gas = []
    coef_coal = []
    for i in range(len(x_gas)):
        coef_gas.append(x_gas[i] - av_gas)
        coef_coal.append(x_coal[i] - av_coal)

    coef_cor = sum(a * b for (a, b) in zip(coef_gas, coef_coal)) / np.sqrt(sum(a * b for (a, b)\
                              in zip(coef_gas, coef_gas)) * sum(a * b for (a, b) \
                                    in zip(coef_coal, coef_coal)))
    return coef_cor

#%% Génération de prix avec le coefficient de correlation

def random():
    "Generate random number for N(0,1) distribution"
    return norm.ppf(np.random.rand(for_values, 1))

def log_returns(data):
    "Calculate the log return of a time serie"
    log_returns = np.log(1 + data.pct_change()).loc[1978:2016]
    log_returns.tail()
    u = log_returns.mean()
    var = log_returns.var()
    drift = u - (0.5 * var)
    stdev = log_returns.std()
    return drift.values[0], stdev.values[0]

def price_path(price_gas, price_coal, correlation):
    "Generate two correlated prices paths"
    b = [random(), random()]
    drift = [log_returns(price_gas)[0], log_returns(price_coal)[0]]
    stdev = [log_returns(price_gas)[1], log_returns(price_coal)[1]]
    yearly_returns = [np.exp(drift[0] + stdev[0] * b[0]), np.exp(drift[1] + stdev[1] *
                      (correlation * b[0] + np.sqrt(1-correlation**2) * b[1]))]

    price_list = [np.zeros_like(yearly_returns)[0], np.zeros_like(yearly_returns)[1]]
    last_price = [price_gas.iloc[-1], price_coal.iloc[-1]]
    price_list[0][0] = last_price[0][0]
    price_list[1][0] = last_price[1][0]

    for i in range(1, for_values):
        price_list[0][i] = price_list[0][i - 1] * yearly_returns[0][i]
        price_list[1][i] = price_list[1][i - 1] * yearly_returns[1][i]
    return price_list[0], price_list[1]

#%%Monte Carlo characteristics : 35 forcasted prices from 2016 to 2050
for_values = end_year - start_year +1

#Collect of data
international_prices_data = pd.read_csv("data/Oil&Gas_prices/data_prices_international_past.csv",
                        index_col=0)

international_prices_data.columns = ["Gas", "Coal"]

price_gas = pd.DataFrame({'Price_Gas': international_prices_data['Gas']}).loc[1977:2016] / (MBtu)
price_coal = pd.DataFrame({'Price_Coal': international_prices_data['Coal']}).loc[1970:2016]\
/(Calo_coal_international * t)
coal = []
gas = []
for i in range(len(price_coal)):
    coal.append(np.array(price_coal)[i][0])
for j in range(len(price_gas)):
    gas.append(np.array(price_gas)[j][0])

#%% Calcul correlation factor
cor_gas = gas
cor_coal = coal[7:]


correlation = realized_pairwise_correlation(cor_gas, cor_coal)
forecast_price = price_path(price_gas, price_coal, correlation)


#%% Creation of the DataFrame
for_coal = []
for_gas = []
for i in range(start_year, end_year+1):
    for_coal.append(forecast_price[1][i-start_year][0])
    for_gas.append(forecast_price[0][i-start_year][0])

international_prices = pd.DataFrame({'Coal': for_coal,
                                      'Gas': for_gas},
    index=range(start_year, end_year+1))

print(international_prices)
