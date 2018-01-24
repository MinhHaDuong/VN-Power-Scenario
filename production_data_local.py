# -*- coding: utf-8 -*-
"""
Created on Mon Jan  8 11:31:01 2018

@author: Alice Duval

Productions are in 1000t for Coal and in Million M3 for Gas.

"""

import numpy as np
from scipy.interpolate import lagrange
from init import pd, start_year, end_year, thousTon_Ton, Mkal__MMBtu, local_Mkal_ton, \
local_millioncubicmeter_TOE, TOE__MMBtu

#Collect of data
local_production_data = pd.read_csv("data/Oil&Gas_prices/data_production_local.csv",
                        index_col=0)
local_production_data.columns = ["Coal", "Gas"]

x = np.array(local_production_data.index)
y_coal = np.array(local_production_data.Coal)
y_gas = np.array(local_production_data.Gas)

#interpolation of data with a langrangian polynom

function_production_coal = lagrange(x, y_coal)
function_production_gas = lagrange(x, y_gas)

interpol_coal_production = []
interpol_gas_production = []

#Saving interpolating data

for i in range(start_year, end_year+1):
    if i <= 2030:
        interpol_coal_production.append(round(function_production_coal(i), 0))
        interpol_gas_production.append(round(function_production_gas(i), 0))
    else:
        interpol_coal_production.append(interpol_coal_production[-1])
        interpol_gas_production.append(interpol_gas_production[-1])

local_production = pd.DataFrame({'nc_Coal': interpol_coal_production,
 'nc_Gas': interpol_gas_production}, index=range(start_year, end_year+1))

#Converting units from data source unit to Btu

local_production['c_Coal'] = round(local_production['nc_Coal']
                                    * thousTon_Ton * local_Mkal_ton * Mkal__MMBtu, 2)
local_production['c_Gas'] = round(local_production['nc_Gas']
                                    *local_millioncubicmeter_TOE * TOE__MMBtu, 2)
