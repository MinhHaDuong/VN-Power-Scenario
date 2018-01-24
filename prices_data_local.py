# -*- coding: utf-8 -*-
"""
Created on Fri Dec 15 14:46:03 2017

@author: Alice Duval

Prices are in $/T (in 2017 US dollars) for Coal and in $/MM3 for Gas.

"""

import numpy as np
from scipy.interpolate import lagrange
from init import pd, start_year, end_year, USD_Mkal__USD_MMBtu, local_Mkal_ton

#Collect of data
local_prices_data = pd.read_csv("data/Oil&Gas_prices/data_prices_local.csv",
                        index_col=0)

local_prices_data.columns = ["Coal", "Gas"]

x_coal = np.array(local_prices_data.index)
y_coal = np.array(local_prices_data.Coal)

#Gas plannification is until 2025: 2030 gas price is assumed to be the same than in 2025. To find
#Gas price langrangian polynomn coefficients, we consider the period 2015 - 2025
x_gas = np.delete(x_coal, -1)
y_gas = np.array(local_prices_data.Gas)
y_gas = np.delete(y_gas, -1)

#interpolation of data with a langrangian polynom
function_price_coal = lagrange(x_coal, y_coal)
function_price_gas = lagrange(x_gas, y_gas)
interpol_coal_price = []
interpol_gas_price = []
index = []

#Saving interpolating data
#for i in range(2030-start_year+1):
for i in range(start_year, end_year+1):
    if i <= 2025:
        interpol_coal_price.append(round(function_price_coal(i), 2))
        interpol_gas_price.append(round(function_price_gas(i), 2))
    elif i <= 2030:
        interpol_coal_price.append(round(function_price_coal(i), 2))
        interpol_gas_price.append(interpol_gas_price[-1])
    else:
        interpol_coal_price.append(interpol_coal_price[-1])
        interpol_gas_price.append(interpol_gas_price[-1])

local_prices = pd.DataFrame({'nc_Coal': interpol_coal_price, 'nc_Gas': interpol_gas_price},
                            index=range(start_year, end_year+1))

#Converting prices from data source unit to USD/MMBtu
local_prices['c_Coal'] = round(local_prices['nc_Coal'] * USD_Mkal__USD_MMBtu / local_Mkal_ton, 2)
local_prices['c_Gas'] = local_prices['nc_Gas']
