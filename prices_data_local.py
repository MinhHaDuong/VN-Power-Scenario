# -*- coding: utf-8 -*-
"""
Created on Fri Dec 15 14:46:03 2017

@author: Alice Duval

Prices are in $/T (in 2017 US dollars) for Coal and in $/MM3 for Gas. 

"""

#import sys
from init import pd, start_year
from scipy.interpolate import lagrange
#import matplotlib.pyplot as plt
import numpy as np


#Collect of data
local_prices_data = pd.read_csv("data/Oil&Gas_prices/data_prices_local.csv",
                        index_col=0)
print(local_prices_data)

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

local_prices = pd.DataFrame({'Coal': interpol_coal_price, 'Gas': interpol_gas_price},index=index)

#def summarize_local_price(self):
#    #print prices
#    print(local_prices)
#    
#def plot_local_prices(self,filename):
#    fig, axarr = plt.subplots(2, 1, figsize=[10, 15], sharex=True)
#    fig.suptitle(str(self), fontsize=15)
    
#def plot_local_prices(self, filename):
#        """Three panels plot of a power development program: production, capacity, additions."""
#        fig, axarr = plt.subplots(3, 1, figsize=[10, 15], sharex=True)
#        fig.suptitle(str(self), fontsize=15)
#        self.plot_additions(axarr[2], True)
#        self.plot_capacity_mix(axarr[1], False)
#        self.plot_production_mix(axarr[0], True)
##        axarr[0].legend(bbox_to_anchor=(1.05, 0), loc='lower left', borderaxespad=0.)
#        fig.tight_layout()
#        plt.subplots_adjust(top=0.94)
#        fig.savefig(filename)
    
#if __name__ == '__main__':
#    if (len(sys.argv) == 2) and (sys.argv[1] == "summarize"):
#        summarize_local_price()
#   if (len(sys.argv) == 3) and (sys.argv[1] == "plot"):
#        plot_local_prices(sys.argv[2])
##        
        