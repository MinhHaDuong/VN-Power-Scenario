# -*- coding: utf-8 -*-
"""
Created on Mon Jan  8 16:54:44 2018

@author: Alice Duval
Fuel_price class deals with different prices and quantity of ressources needed. 

Data are available twice : 
    - nc_information means that data units is the data source' units (nc: non convertes)
    - c_information means that data units are: USD/MBtu for prices and Btu for energy units (c: converted)
    
ISSUES TO SOLVE : lines 47 and 48 take the min btw local_production and needed_production

"""
from collections import namedtuple
from prices_conversion import USD_Mkal__USD_MMBtu, international_Mkal_ton
from init import pd, start_year
import numpy as np
import matplotlib.pyplot as plt

class Fuel_Price(namedtuple('Fuel_Price',
                           ['index',
                            'local_prices',
                            'international_prices',
                            'local_production',
                            'needed_production',
                            'needed_importation',
                            'average_price'
                            ])):
    
    def __new__(cls, index, local_prices, international_prices, local_production, needed_production):
        
        needed_importation = pd.DataFrame(columns=['nc_Coal', 'nc_Gas', 'c_Coal', 'c_Gas'], index = index)
        
        #Qualify what importation have to be done (in MMBtu) 
        needed_importation["c_Coal"] = round(needed_production["Coal"]-local_production["c_Coal"],2)
        needed_importation["c_Gas"] = round(needed_production["Gas"]-local_production["c_Gas"],2)
        
        #Qualify what importation have to be done (Coal is expressed in tons and Gas is still in MMBtu)
        needed_importation["nc_Coal"] = round(needed_importation["c_Coal"] * international_Mkal_ton / USD_Mkal__USD_MMBtu,2)
        needed_importation["nc_Gas"] = needed_importation["c_Gas"]
        
        #importation needs < 0 means that there is not any importation. negative values are replaced by 0
        needed_importation [needed_importation < 0] = 0
        
        #Calculation of the average fuel price (for Coal and Gas) in USD/MMBtu 
        #If there is not any importation, local price is considered
        average_price = pd.DataFrame(columns=['Coal', 'Gas'], index = index)
        average_price['Coal'] = np.where(needed_importation['c_Coal'] == 0, round(local_prices['c_Coal'],2), round((local_production['c_Coal']*local_prices['c_Coal'] + needed_importation['c_Coal'] * international_prices['c_Coal']) / (needed_production['Coal']), 2))
        average_price['Gas'] = np.where(needed_importation['c_Gas'] == 0, round(local_prices['c_Gas'],2), round((local_production['c_Gas']*local_prices['c_Gas'] + needed_importation['c_Gas'] * international_prices['c_Gas']) / (needed_production['Gas']),2))

        return super().__new__(cls, index, local_prices, international_prices, local_production, needed_production, needed_importation, average_price)
    
    def plot_coal_supply(self, ax, legend=True):
        self.needed_production['Coal'].plot(ax=ax, title="Coal supply for the electric system (in BTu)", label= "Coal needs")
        self.local_production["c_Coal"].plot(ax=ax, label="Coal producted in Vietnam")
        self.needed_importation["c_Coal"].plot(ax=ax, label="Coal imported")
        
    
    def plot_coal_price(self, ax, legend=True):
        self.average_price['Coal'].plot(ax=ax, title="Coal price (in USD/BTu)", label="Average price of Coal for the electric system")
        self.local_prices['c_Coal'].plot(ax=ax, label="Coal produced in Vietnam")
        self.international_prices["c_Coal"].plot(ax=ax, label="Imported Coal (Australia)")
        
        
    def plot_coal_information(self, filename):
        """Two panels plot to describe Gas origin and price of the electric system"""
        fig, (ax1, ax2) = plt.subplots(2, 1, figsize=[10, 15], sharex=True)
        fig.suptitle('Coal supply and price for the electric system', fontsize=15)
        self.plot_coal_price(ax1, True)
        self.plot_coal_supply(ax2, True)
        ax1.legend(loc="upper left")
        ax2.legend(loc="upper left")
        fig.tight_layout()
        plt.subplots_adjust(top=0.94)
        fig.savefig(filename+ '_Coal')
        
    def plot_gas_supply(self, ax, legend=True):
        self.needed_production['Gas'].plot(ax=ax, title="Gas supply for the electric system (in BTu)", label= "Gas needs")
        self.local_production["c_Gas"].plot(ax=ax, label="Gas producted in Vietnam")
        self.needed_importation["c_Gas"].plot(ax=ax, label="Gas imported")
        
    
    def plot_gas_price(self, ax, legend=True):
        self.average_price['Gas'].plot(ax=ax, title="Gas price (in USD/BTu)", label="Average price of Gas for the electric system")
        self.local_prices['c_Gas'].plot(ax=ax, label="Gas produced in Vietnam")
        self.international_prices["c_Gas"].plot(ax=ax, label="Imported Gas (Japan)")
        
        
    def plot_gas_information(self, filename):
        """Two panels plot to describe Gas origin and price of the electric system"""
        fig, (ax1, ax2) = plt.subplots(2, 1, figsize=[10, 15], sharex=True)
        fig.suptitle('Gas supply and price for the electric system', fontsize=15)
        self.plot_gas_price(ax1, True)
        self.plot_gas_supply(ax2, True)
        ax1.legend(loc="upper left")
        ax2.legend(loc="upper left")
        fig.tight_layout()
        plt.subplots_adjust(top=0.94)
        fig.savefig(filename+ '_Gas')
    
    def summarize(self):
        """Print object's summary."""
        print(self.summary())
        
    def summary(self):
        """Summary of a power development program, time series shown for key years only."""
        milestones = [start_year, 2020, 2025, 2030]
        return (
            "Coal supply (in Btu)\n"
            + str(self.needed_production.loc[milestones, 'Coal'].round()) 
            + str(self.needed_importation.loc[milestones, 'c_Coal'].round()) 
            + str(self.local_production.loc[milestones, 'c_Coal'])+ '\n\n')
#            + "Old capacity retirement by fuel type (MW)\n"
#            + str(self.retirement.loc[milestones, fuels].round()) + '\n\n'
#            + "Generation capacity by fuel type (MW)\n"
#            + str(self.capacities.loc[milestones, technologies].round()) + '\n\n'
#            + "Electricity production (GWh)\n"
#            + str(self.production.loc[milestones].round()) + '\n\n'
#            + "Capacity factors\n"
#            + str(self.capacity_factor.loc[milestones].round(2)) + '\n')
        #print(self.international_prices)
        #print(self.local_prices)
        #print(self.average_price)