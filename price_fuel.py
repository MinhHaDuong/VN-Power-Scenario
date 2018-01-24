# -*- coding: utf-8 -*-
"""
Created on Mon Jan  8 16:54:44 2018

@author: Alice Duval
Fuel_price class deals with different prices and quantity of ressources needed.

Data are available twice :
    - nc_information means that data units is the data source' units (nc: non convertes)
    - c_information means that data units are: USD/MBtu for prices and Btu for energy units
      (c: converted)

"""
from collections import namedtuple
import numpy as np
import matplotlib.pyplot as plt
from init import pd, start_year, USD_Mkal__USD_MMBtu, international_Mkal_ton

class Fuel_Price(namedtuple('Fuel_Price',
                           ['index',
                            'local_prices',
                            'international_prices',
                            'local_production',
                            'needed_production',
                            'needed_importation',
                            'average_price'
                            ])):
    """An average price for fuels"""

    def __new__(cls, index, local_prices, international_prices, local_production,
               needed_production):
        needed_importation = pd.DataFrame(columns=['nc_Coal', 'nc_Gas', 'c_Coal', 'c_Gas'],
                                          index=index)

        #Qualify what importation have to be done (in MMBtu)
        needed_importation["c_Coal"] = round(needed_production["Coal"]-
                          local_production["c_Coal"], 2)
        needed_importation["c_Gas"] = round(needed_production["Gas"]-local_production["c_Gas"], 2)

        #Qualify what importation have to be done
        #(Coal is expressed in tons and Gas is still in MMBtu)
        needed_importation["nc_Coal"] = round(needed_importation["c_Coal"] *
                          international_Mkal_ton / USD_Mkal__USD_MMBtu, 2)
        needed_importation["nc_Gas"] = needed_importation["c_Gas"]

        #Importation needs < 0 means that there is not any importation.
        #Negative values are replaced by 0
        needed_importation[needed_importation < 0] = 0

        #Calculation of the average fuel price (for Coal and Gas) in USD/MMBtu
        #If there is not any importation, local price is considered
        average_price = pd.DataFrame(columns=['Coal', 'Gas'], index=index)
        average_price['Coal'] = np.where(needed_importation['c_Coal'] == 0,
                     round(local_prices['c_Coal'], 2), round((local_production['c_Coal']*
                          local_prices['c_Coal'] + needed_importation['c_Coal'] *
                          international_prices['c_Coal']) / (needed_production['Coal']), 2))

        average_price['Gas'] = np.where(needed_importation['c_Gas'] == 0,
                     round(local_prices['c_Gas'], 2), round((local_production['c_Gas']*
                          local_prices['c_Gas'] + needed_importation['c_Gas'] *
                          international_prices['c_Gas']) / (needed_production['Gas']), 2))

        return super().__new__(cls, index, local_prices, international_prices, local_production,
                    needed_production, needed_importation, average_price)

    def plot_coal_supply(self, ax):
        """Describe Coal supply of the electric system."""
        self.needed_production['Coal'].plot(ax=ax, title="Coal supply \
                              for the electric system (in MMBTu)", label="Coal needs")
        self.local_production["c_Coal"].plot(ax=ax, label="Coal producted in Vietnam")
        self.needed_importation["c_Coal"].plot(ax=ax, label="Coal imported")

    def plot_coal_price(self, ax):
        """Describe Coal price of the electric system."""
        self.average_price['Coal'].plot(ax=ax, title="Coal price (in USD/MMBTu)",
                          label="Average price of Coal for the electric system")
        self.local_prices['c_Coal'].plot(ax=ax, label="Coal produced in Vietnam")
        self.international_prices["c_Coal"].plot(ax=ax, label="Imported Coal (Australia)")

    def plot_coal_information(self, filename):
        """Describe Coal origin and price of the electric system."""
        fig, (ax1, ax2) = plt.subplots(2, 1, figsize=[10, 15], sharex=True)
        fig.suptitle('Coal supply and price for the electric system', fontsize=15)
        self.plot_coal_price(ax1)
        self.plot_coal_supply(ax2)
        ax1.legend(loc="upper left")
        ax2.legend(loc="upper left")
        fig.tight_layout()
        plt.subplots_adjust(top=0.94)
        fig.savefig(filename+ '_Coal')

    def plot_gas_supply(self, ax):
        """Describe Gas supply of the electric system."""
        self.needed_production['Gas'].plot(ax=ax,
                              title="Gas supply for the electric system (in MMBTu)",
                              label="Gas needs")
        self.local_production["c_Gas"].plot(ax=ax, label="Gas producted in Vietnam")
        self.needed_importation["c_Gas"].plot(ax=ax, label="Gas imported")

    def plot_gas_price(self, ax):
        """Describe Gas price of the electric system."""
        self.average_price['Gas'].plot(ax=ax, title="Gas price (in USD/MMBTu)",
                          label="Average price of Gas for the electric system")
        self.local_prices['c_Gas'].plot(ax=ax, label="Gas produced in Vietnam")
        self.international_prices["c_Gas"].plot(ax=ax, label="Imported Gas (Japan)")

    def plot_gas_information(self, filename):
        """Describe Gas origin and price of the electric system."""
        fig, (ax1, ax2) = plt.subplots(2, 1, figsize=[10, 15], sharex=True)
        fig.suptitle('Gas supply and price for the electric system', fontsize=15)
        self.plot_gas_price(ax1)
        self.plot_gas_supply(ax2)
        ax1.legend(loc="upper left")
        ax2.legend(loc="upper left")
        fig.tight_layout()
        plt.subplots_adjust(top=0.94)
        fig.savefig(filename+ '_Gas')

    def plot_information(self, filename):
        """Gather gas and coal informations of the electric system."""
        fig, (ax1, ax2) = plt.subplots(2, 1, figsize=[15, 10])
        self.plot_gas_information(ax1)
        self.plot_coal_information(ax2)
        fig.savefig(filename)

    def summarize(self):
        """Print object's summary."""
        print(self.summary())

    def summary(self):
        """Summary of Coal and Gas supply and prices."""
        milestones = [start_year, 2020, 2025, 2030]

        supply_coal = pd.DataFrame({'Coal imported': self.needed_importation['c_Coal']/10**8,
                                    'Coal locally produced': self.local_production['c_Coal']/10**8,
                                    'Coal needs': self.needed_production['Coal']/10**8})

        prices_coal = pd.DataFrame({'Average coal price': self.average_price['Coal'],
                                    'Local coal price': self.local_prices['c_Coal'],
                                    'Imported coal price': self.international_prices["c_Coal"]})

        supply_gas = pd.DataFrame({'Gas needs': self.needed_production['Gas']/10**8,
                                   'Gas locally produced': self.local_production['c_Gas']/10**8,
                                   'Gas imported': self.needed_importation['c_Gas']/10**8})

        prices_gas = pd.DataFrame({'Average gas price': self.average_price['Gas'],
                                   'Local gas price': self.local_prices['c_Gas'],
                                   'Imported gas price': self.international_prices["c_Gas"]})

        return (
            "Coal supply (in E+8 MMBtu)\n"
            + str(supply_coal.loc[milestones].round()) + '\n\n'
            +"Coal prices (in $/MMBtu)\n"
            + str(prices_coal.loc[milestones].round()) + '\n\n'
            +"Gas supply (in E+8 MMBtu)\n"
            + str(supply_gas.loc[milestones].round()) + '\n\n'
            +"Gas prices (in $/MMBtu)\n"
            + str(prices_gas.loc[milestones].round()) + '\n\n'
            )


            #print(self.international_prices)
            #print(self.local_prices)
            #print(self.average_price)
