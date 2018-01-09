# -*- coding: utf-8 -*-
"""
Created on Mon Jan  8 14:13:45 2018

@author: Alice Duval

Energy unit (for Gas and Coal) is Btu

"""
from plan_baseline import baseline
from param_reference import heat_rate

from price_fuel import Fuel_Price
#
from prices_data_local import local_prices
from prices_data_international import international_prices
from production_data_local import local_production

from init import pd, start_year

import sys

# electric production is in Gwh
electric_production = baseline.production[['Coal','Gas']].loc[start_year:2030]

# Heat_rate is in Btu/kWh or in MMBtu/Gwh
useful_heat_rate  = heat_rate[['Coal','Gas']].loc[start_year:2030]

#needed_energy is in MMBtu here

needed_energy = pd.DataFrame(electric_production.values*useful_heat_rate.values, columns=useful_heat_rate.columns, index=useful_heat_rate.index)



#Here: No need to convert: Values are already in MBtu 

index = list(range(start_year, 2031))
average_price = Fuel_Price(index,local_prices, international_prices, local_production, needed_energy)

if __name__ == '__main__':
    if (len(sys.argv) == 2) and (sys.argv[1] == "summarize"):
        average_price.summarize()
    if (len(sys.argv) == 3) and (sys.argv[1] == "plot"):
        average_price.plot_coal_information(sys.argv[2])
        average_price.plot_gas_information(sys.argv[2])
    