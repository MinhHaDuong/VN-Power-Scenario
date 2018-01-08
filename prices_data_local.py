# -*- coding: utf-8 -*-
"""
Created on Fri Dec 15 14:46:03 2017

@author: Alice Duval

Prices are in $/T (in 2017 US dollars) for Coal and in $/MM3 for Gas. 

"""

#import sys
from init import pd, start_year
from prices_conversion import USD_Mkal__USD_MMBtu, local_Mkal_ton
from scipy.interpolate import lagrange
#import matplotlib.pyplot as plt
import numpy as np


#Collect of data
local_prices_data = pd.read_csv("data/Oil&Gas_prices/data_prices_local.csv",
                        index_col=0)

local_prices_data.columns = ["Coal", "Gas"]

x = np.array(local_prices_data.index)
y_coal = np.array(local_prices_data.Coal)
y_gas = np.array(local_prices_data.Gas)

#interpolation of data with a langrangian polynom

function_price_coal = lagrange(x, y_coal)
function_price_gas = lagrange(x, y_gas)

interpol_coal_price=[]
interpol_gas_price=[]
index=[]

#Saving interpolating data

for i in range(2030-start_year+1):
    index.append(start_year + i)
    interpol_coal_price.append(round(function_price_coal(start_year + i),2))
    interpol_gas_price.append(round(function_price_gas(start_year + i),2))

local_prices = pd.DataFrame({'nc_Coal': interpol_coal_price, 'nc_Gas': interpol_gas_price},index=index)

#Converting prices from data source unit to USD/MMBtu
local_prices['c_Coal'] = round(local_prices['nc_Coal'] * USD_Mkal__USD_MMBtu / local_Mkal_ton,2)
local_prices['c_Gas'] = local_prices['nc_Gas']
 
        