# -*- coding: utf-8 -*-
"""
Created on Mon Jan  8 11:31:01 2018

@author: Alice Duval

Productions are in 1000t for Coal and in Million M3 for Gas. 

"""

#import sys
from init import pd, start_year
from scipy.interpolate import lagrange
#import matplotlib.pyplot as plt
import numpy as np

#Collect of data
local_production_data = pd.read_csv("data/Oil&Gas_prices/data_production_local.csv",
                        index_col=0)
print(local_production_data)

local_production_data.columns = ["Coal", "Gas"]

x = np.array(local_production_data.index)
y_coal = np.array(local_production_data.Coal)
y_gas = np.array(local_production_data.Gas)

#interpolation of data with a langrangian polynom

function_production_coal = lagrange(x, y_coal)
function_production_gas = lagrange(x, y_gas)

interpol_coal_production=[]
interpol_gas_production=[]
index=[]

#Saving interpolating data

for i in range(2030-start_year+1):
    index.append(start_year + i)
    interpol_coal_production.append(round(function_production_coal(start_year + i),0))
    interpol_gas_production.append(round(function_production_gas(start_year + i),0))

local_production = pd.DataFrame({'Coal': interpol_coal_production, 'Gas': interpol_gas_production},index=index)

print(local_production)