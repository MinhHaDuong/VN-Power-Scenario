# -*- coding: utf-8 -*-
"""
Created on Mon Jan  8 14:13:45 2018

@author: Alice Duval

Energy unit (for Gas and Coal) is Btu

"""
from plan_baseline import baseline
from param_reference import heat_rate
from init import pd, start_year

electric_production = baseline.production[['Coal','Gas']].loc[start_year:2030]
useful_heat_rate  = heat_rate[['Coal','Gas']].loc[start_year:2030]

needed_energy = pd.DataFrame(electric_production.values*useful_heat_rate.values, columns=useful_heat_rate.columns, index=useful_heat_rate.index)
