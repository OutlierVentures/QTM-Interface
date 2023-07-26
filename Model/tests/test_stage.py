# Dependences
import pandas as pd
import numpy as np
import os
import sys
import traceback

# radCAD
from radcad import Model, Simulation, Experiment
from radcad.engine import Engine, Backend


# Project dependences
# Get the current directory
current_dir = os.path.dirname(os.path.abspath(__file__))

# Go up one folder
parent_dir = os.path.abspath(os.path.join(current_dir, os.pardir))

# Append the parent directory to sys.path
sys.path.append(parent_dir)

from sys_params import *
import state_variables
import state_update_blocks
import sys_params
from parts.utils import *
from plots import *
from post_processing import *

import importlib
importlib.reload(state_variables)
importlib.reload(state_update_blocks)
importlib.reload(sys_params)

QTM_data_tables = pd.read_csv('./Quantitative_Token_Model_V1.88_radCad_integration - Data Tables.csv')

if __name__ == '__main__'   :
    MONTE_CARLO_RUNS = 1
    TIMESTEPS = 12*10

    model = Model(initial_state=state_variables.initial_state, params=sys_params.sys_param, state_update_blocks=state_update_blocks.state_update_block)
    simulation = Simulation(model=model, timesteps=TIMESTEPS, runs=MONTE_CARLO_RUNS)

    result = simulation.run()
    df = pd.DataFrame(result)

    # post processing
    data = postprocessing(df)

    ### BEGIN TESTS ###
    print("\n-------------------------------------------## BEGIN TESTS ##-------------------------------------------")

    
    ## TEST ADOPTION ##
    print("\n-------------------------------------------## TEST ADOPTION ##-----------------------------------------")
    print("Testing adoption of radCad timeseries simulation against QTM data tables...")
    test_timeseries(data=data, data_key="product_users", data_row_multiplier=1, QTM_data_tables=QTM_data_tables, QTM_row=7, relative_tolerance=0.001)
    test_timeseries(data=data, data_key="token_holders", data_row_multiplier=1, QTM_data_tables=QTM_data_tables, QTM_row=8, relative_tolerance=0.001)

    
    ## TEST AGENT VESTING VALUES ##
    print("\n------------------------------------## TEST AGENT VESTING VALUES ##------------------------------------")
    print("Testing individual vesting values of radCad timeseries simulation against QTM data tables...")
    # test individual vesting numbers of all agents except for the market investors (market investors don't receive vested tokens)
    for i in range(len(stakeholder_names)-1):
        stakeholder = stakeholder_names[i]
        test_timeseries(data=data, data_key=stakeholder+"_tokens_vested", data_row_multiplier=1, QTM_data_tables=QTM_data_tables, QTM_row=11+i, relative_tolerance=0.001)
    
    print("Testing cumulative vesting values of radCad timeseries simulation against QTM data tables...")
    # test cumulative vesting numbers of all agents except for the market investors (market investors don't receive vested tokens)
    for i in range(len(stakeholder_names)-1):
        stakeholder = stakeholder_names[i]
        test_timeseries(data=data, data_key=stakeholder+"_tokens_vested_cum", data_row_multiplier=1, QTM_data_tables=QTM_data_tables, QTM_row=28+i, relative_tolerance=0.001)

    
    ## TEST FREE SUPPLY USAGE ##
    print("\n--------------------------------------## TEST FREE SUPPLY USAGE ##-------------------------------------")
    print("Testing free supply usage of radCad timeseries simulation against QTM data tables...")
    test_timeseries(data=data, data_key="selling_perc", data_row_multiplier=100, QTM_data_tables=QTM_data_tables, QTM_row=45, relative_tolerance=0.001)
    test_timeseries(data=data, data_key="utility_perc", data_row_multiplier=100, QTM_data_tables=QTM_data_tables, QTM_row=46, relative_tolerance=0.001)
    test_timeseries(data=data, data_key="holding_perc", data_row_multiplier=100, QTM_data_tables=QTM_data_tables, QTM_row=47, relative_tolerance=0.001)


    ## TEST INCENTIVISATION ##
    print("\n---------------------------------------## TEST INCENTIVISATION ##--------------------------------------")
    print("Testing incentivisation of radCad timeseries simulation against QTM data tables...")
    test_timeseries(data=data, data_key="minted_tokens", data_row_multiplier=1, QTM_data_tables=QTM_data_tables, QTM_row=50, relative_tolerance=0.001)
    test_timeseries(data=data, data_key="incentivised_tokens", data_row_multiplier=1, QTM_data_tables=QTM_data_tables, QTM_row=51, relative_tolerance=0.001)
    test_timeseries(data=data, data_key="incentivised_tokens_cum", data_row_multiplier=1, QTM_data_tables=QTM_data_tables, QTM_row=52, relative_tolerance=0.001)


    """ ## TEST CIRCULATING SUPPLY ##
    print("\n-------------------------------------## TEST CIRCULATING SUPPLY ##-------------------------------------")
    print("Testing circulating supply of radCad timeseries simulation against QTM data tables...")
    test_timeseries(data=data, data_key="circulating_supply", QTM_data_tables=QTM_data_tables, QTM_row=182, relative_tolerance=0.001)
    
    
    ## TEST META BUCKET ALLOCATIONS ##
    print("\n-----------------------------------## TEST META BUCKET ALLOCATIONS ##----------------------------------")
    print(data["meta_bucket_allocations"]) """
    
    
    ### END OF TESTS ###
    print("\n")
    print(u'\u2713'+" ALL TESTS PASSED!")
    print("\n------------------------------------")
        

