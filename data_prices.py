# -*- coding: utf-8 -*-
"""
Created on Fri Dec 15 14:46:03 2017

@author: Alice Duval

Prices are in $/mT (in 2017 US dollars) for Coal and in $/MMBtu for Gas. These prices are converted into $/Btu
According to the scale order, mT is for metric tons. 

These prices will be linked with the heat rate that come from OpenEI data (in 	US$/MMBtu) . 

Different units: 
    MMBtu: british unit amount of heat required to increase the temperature of a pint of water (which weighs exactly 16 ounces)

Heat rate is "The efficiency of the power plant in converting fuel into electricity". 
http://en.openei.org/apps/TCDB/#blank, https://www.nrel.gov/analysis/tech-lcoe-documentation.html
Heat rate is expressed in Btu/kWh -> 3412 BTUs = 1 kWh 
For example:
Heat rate = 3412 implies that the rendement is 100%.
Heat rate = 9200 implies that the rendement is 37% (to be verified - Coal)  
"""

from init import pd, years

#Collect of data from the world bank
WB_prices = pd.read_csv("data/Oil&Gas_prices/data_prices.csv",
                        index_col=0)

WB_prices.columns = ["Coal", "Gas"]

#Units conversion between data and units used in the model
_1_MMBtu_1_Btu = 1/10**6
_1_mt_1_Btu = 1/(27.778243*10**3) 
_1_mt_1_MMBtu = 1/(27.7778243)

#Creation of the DataFrame for fuel prices in $/BtU (conversion to add) for years that are considered in the model 
fuel_prices = pd.DataFrame(index=years)

#Added data from the csv to the data frame for considered years
fuel_prices = pd.concat([WB_prices, fuel_prices], axis=1, join_axes=[fuel_prices.index])

#Convert data of the dataframe (in MMBtu )
fuel_prices.loc[:,'Coal'] *= _1_mt_1_MMBtu 
fuel_prices.loc[:,'Gas'] *= 1

print(fuel_prices)
