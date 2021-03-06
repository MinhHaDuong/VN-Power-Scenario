# encoding: utf-8
# Economic of co-firing in two power plants in Vietnam
#
# (c) Minh Ha-Duong, An Ha Truong 2016-2017
# minh.haduong@gmail.com
# Creative Commons Attribution-ShareAlike 4.0 International
#
"""Regression test."""

#import pytest
import numpy as np
from parameter_reference import reference
from plan_baseline import baseline
from plan_more_gas import moreGas
from plan_with_ccs import withCCS
from prices_data_local import local_prices
from production_data_local import local_production
from Run import RunPair
from prices_data_international import import_prices_path, price_gas, price_coal
from price_fuel import price_fuel
from run_sensitivity_lcoe import multiple_LCOE
from run_sensitivity_analysis_ccs import RUNPAIRS
# pylint and pytest known compatibility bug
# pylint: disable=redefined-outer-name


def test_reference_str(regtest):
    regtest.write(str(reference))


def test_reference_summary(regtest):
    regtest.write(reference.summary())


def test_withCCS_str(regtest):
    regtest.write(str(withCCS))


def test_withCCS_summary(regtest):
    regtest.write(withCCS.summary())


def test_baseline_str(regtest):
    regtest.write(str(baseline))


def test_baseline_summary(regtest):
    regtest.write(baseline.summary())


def test_moreGas_summary(regtest):
    regtest.write(moreGas.summary())


def test_runpair_summary(regtest):
    pair = RunPair(baseline, withCCS, reference)
    regtest.write(pair.summary(["Baseline", "High CCS", "difference"]))


def test_analysis(regtest):
    analysis = '\n'.join([runpair.summary(["BAU", "ALT", "difference"]) for runpair in RUNPAIRS])
    regtest.write(analysis)


def test_past_data(regtest):
    import_prices = import_prices_path(price_gas, price_coal)
    regtest.write(import_prices.summary())


def test_fuel_price(regtest):
    np.random.seed(0)
    fuel_prices = price_fuel(local_prices, price_gas, price_coal, local_production, baseline)
    regtest.write(fuel_prices.summary())


def test_lcoe_prices(regtest):
    lcoe_list = multiple_LCOE(baseline, 100)
    regtest.write(lcoe_list.summary())
