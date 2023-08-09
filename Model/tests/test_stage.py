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

# Get the current directory
current_dir = os.path.dirname(os.path.abspath(__file__))

# Go two folders up
parent_dir = os.path.abspath(os.path.join(os.path.abspath(os.path.join(current_dir, os.pardir)), os.pardir))

QTM_data_tables = pd.read_csv(parent_dir+'/data/Quantitative_Token_Model_V1.88_radCad_integration - Data Tables.csv')

if __name__ == '__main__'   :
    MONTE_CARLO_RUNS = 1
    TIMESTEPS = 12*10

    model = Model(initial_state=state_variables.initial_state, params=sys_params.sys_param, state_update_blocks=state_update_blocks.state_update_block)
    simulation = Simulation(model=model, timesteps=TIMESTEPS, runs=MONTE_CARLO_RUNS)

    result = simulation.run()
    df = pd.DataFrame(result)

    # post processing
    data_tx1 = postprocessing(df, substep=17) # after adoption buy lp tx
    data_tx2 = postprocessing(df, substep=18) # after vesting sell lp tx
    data_tx3 = postprocessing(df, substep=19) # after vesting sell lp tx
    data_tx4 = postprocessing(df, substep=20) # after vesting sell lp tx
    data = postprocessing(df, substep=df.substep.max()) # at the end of the timestep = last substep



    tests = 1

    if tests == 0:
        ### BEGIN TESTS ###
        print("\n-------------------------------------------------------------------------------------------------------")
        print("\n-------------------------------------------## BEGIN TESTS ##-------------------------------------------")
        print("\n-------------------------------------------------------------------------------------------------------")
        print("\n")

        ### MOCKUPS ###
        ## TEST MOCKUPS ##
        print("\n-------------------------------------------## MOCKUP TESTS ##------------------------------------------")
        print("Testing MOCKUP implementations of radCad timeseries simulation against QTM data tables...")
        test_timeseries(data=data, data_key="holding_supply", data_row_multiplier=1, QTM_data_tables=QTM_data_tables, QTM_row=180, relative_tolerance=0.001)
        print("\n\n")

        
        ### MODEL ###
        ## TEST ADOPTION ##
        print("\n-------------------------------------------## TEST ADOPTION ##-----------------------------------------")
        print("Testing adoption of radCad timeseries simulation against QTM data tables...")
        test_timeseries(data=data, data_key="product_users", data_row_multiplier=1, QTM_data_tables=QTM_data_tables, QTM_row=7, relative_tolerance=0.001)
        test_timeseries(data=data, data_key="token_holders", data_row_multiplier=1, QTM_data_tables=QTM_data_tables, QTM_row=8, relative_tolerance=0.001)

        
        ## TEST AGENT VESTING VALUES ##
        print("\n------------------------------------## TEST AGENT VESTING VALUES ##------------------------------------")
        print("Testing individual vesting values of radCad timeseries simulation against QTM data tables...")
        for i in range(len(stakeholder_names)-3):
            stakeholder = stakeholder_names[i]
            test_timeseries(data=data, data_key=stakeholder+"_a_tokens_vested", data_row_multiplier=1, QTM_data_tables=QTM_data_tables, QTM_row=11+i, relative_tolerance=0.001)
        
        print("Testing cumulative vesting values of radCad timeseries simulation against QTM data tables...")
        for i in range(len(stakeholder_names)-3):
            stakeholder = stakeholder_names[i]
            test_timeseries(data=data, data_key=stakeholder+"_a_tokens_vested_cum", data_row_multiplier=1, QTM_data_tables=QTM_data_tables, QTM_row=28+i, relative_tolerance=0.001)

        
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
        #test_timeseries(data=data, data_key="incentivised_tokens_usd", data_row_multiplier=1, QTM_data_tables=QTM_data_tables, QTM_row=54, relative_tolerance=0.001)


        ## TEST AIRDROPS ##
        print("\n------------------------------------------## TEST AIRDROPS ##------------------------------------------")
        print("Testing airdrops of radCad timeseries simulation against QTM data tables...")
        test_timeseries(data=data, data_key="airdrop_tokens", data_row_multiplier=1, QTM_data_tables=QTM_data_tables, QTM_row=57, relative_tolerance=0.001)
        test_timeseries(data=data, data_key="airdrop_tokens_cum", data_row_multiplier=1, QTM_data_tables=QTM_data_tables, QTM_row=59, relative_tolerance=0.001)
        #test_timeseries(data=data, data_key="airdrop_tokens_usd", data_row_multiplier=1, QTM_data_tables=QTM_data_tables, QTM_row=61, relative_tolerance=0.001)


        ## TEST AGENT META BUCKET ALLOCATIONS ##
        print("\n--------------------------------## TEST AGENT META BUCKET ALLOCATIONS ##--------------------------------")
        print("Testing individual agent meta bucket allocations of radCad timeseries simulation against QTM data tables...")
        for i in range(len(stakeholder_names)-8):
            stakeholder = stakeholder_names[i]
            test_timeseries(data=data, data_key=stakeholder+"_a_selling_tokens", data_row_multiplier=1, QTM_data_tables=QTM_data_tables, QTM_row=64+i, relative_tolerance=0.001)
            test_timeseries(data=data, data_key=stakeholder+"_a_utility_tokens", data_row_multiplier=1, QTM_data_tables=QTM_data_tables, QTM_row=77+i, relative_tolerance=0.001)
            test_timeseries(data=data, data_key=stakeholder+"_a_holding_tokens", data_row_multiplier=1, QTM_data_tables=QTM_data_tables, QTM_row=90+i, relative_tolerance=0.001)

        
        ## TEST FROM HOLDING SUPPLY META BUCKET ALLOCATIONS ##
        print("\n-------------------------## TEST FROM HOLDING SUPPLY META BUCKET ALLOCATIONS ##-------------------------")
        print("Testing from holding supply meta bucket allocations of radCad timeseries simulation against QTM data tables...")
        test_timeseries(data=data, data_key="From_Holding_Supply_Selling", data_row_multiplier=1, QTM_data_tables=QTM_data_tables, QTM_row=73, relative_tolerance=0.001, timestep_cut_off=1)
        test_timeseries(data=data, data_key="From_Holding_Supply_Utility", data_row_multiplier=1, QTM_data_tables=QTM_data_tables, QTM_row=86, relative_tolerance=0.001, timestep_cut_off=1)
        test_timeseries(data=data, data_key="From_Holding_Supply_Holding", data_row_multiplier=1, QTM_data_tables=QTM_data_tables, QTM_row=99, relative_tolerance=0.001, timestep_cut_off=1)


        ## TEST META BUCKET ALLOCATION SUMS ##
        print("\n---------------------------------## TEST META BUCKET ALLOCATION SUMS ##---------------------------------")
        print("Testing meta bucket allocation sums of radCad timeseries simulation against QTM data tables...")
        test_timeseries(data=data, data_key="selling_allocation", data_row_multiplier=1, QTM_data_tables=QTM_data_tables, QTM_row=74, relative_tolerance=0.001, timestep_cut_off=1)
        test_timeseries(data=data, data_key="selling_allocation_cum", data_row_multiplier=1, QTM_data_tables=QTM_data_tables, QTM_row=75, relative_tolerance=0.001, timestep_cut_off=1)
        test_timeseries(data=data, data_key="utility_allocation", data_row_multiplier=1, QTM_data_tables=QTM_data_tables, QTM_row=87, relative_tolerance=0.001, timestep_cut_off=1)
        test_timeseries(data=data, data_key="utility_allocation_cum", data_row_multiplier=1, QTM_data_tables=QTM_data_tables, QTM_row=88, relative_tolerance=0.001, timestep_cut_off=1)
        test_timeseries(data=data, data_key="holding_allocation", data_row_multiplier=1, QTM_data_tables=QTM_data_tables, QTM_row=100, relative_tolerance=0.001, timestep_cut_off=1)
        test_timeseries(data=data, data_key="holding_allocation_cum", data_row_multiplier=1, QTM_data_tables=QTM_data_tables, QTM_row=101, relative_tolerance=0.001, timestep_cut_off=1)

        
        ## TEST META UTILITY SHARE ALLOCATIONS ##
        print("\n--------------------------------## TEST META UTILITY SHARE ALLOCATIONS ##-------------------------------")
        print("Testing meta utility share allocations of radCad timeseries simulation against QTM data tables...")
        # staking: revenue share
        test_timeseries(data=data, data_key="staking_revenue_share_allocation", data_row_multiplier=1, QTM_data_tables=QTM_data_tables, QTM_row=104, relative_tolerance=0.001, timestep_cut_off=1)
        test_timeseries(data=data, data_key="staking_revenue_share_allocation_cum", data_row_multiplier=1, QTM_data_tables=QTM_data_tables, QTM_row=110, relative_tolerance=0.001, timestep_cut_off=1)
        # liquidity mining
        test_timeseries(data=data, data_key="liquidity_mining_allocation", data_row_multiplier=1, QTM_data_tables=QTM_data_tables, QTM_row=105, relative_tolerance=0.001, timestep_cut_off=1)
        test_timeseries(data=data, data_key="liquidity_mining_allocation_cum", data_row_multiplier=1, QTM_data_tables=QTM_data_tables, QTM_row=111, relative_tolerance=0.001, timestep_cut_off=1)
        # burning
        test_timeseries(data=data, data_key="burning_allocation", data_row_multiplier=1, QTM_data_tables=QTM_data_tables, QTM_row=106, relative_tolerance=0.001, timestep_cut_off=1)
        test_timeseries(data=data, data_key="burning_allocation_cum", data_row_multiplier=1, QTM_data_tables=QTM_data_tables, QTM_row=112, relative_tolerance=0.001, timestep_cut_off=1)

        # holding, no cum, already assessed in holding supply
        test_timeseries(data=data, data_key="holding_allocation", data_row_multiplier=1, QTM_data_tables=QTM_data_tables, QTM_row=107, relative_tolerance=0.001, timestep_cut_off=1)


        ## TEST ADOPTION 2 ##
        print("\n------------------------------------------## TEST ADOPTION 2 ##-----------------------------------------")
        print("Testing product revenue and token_buys of radCad timeseries simulation against QTM data tables...")
        test_timeseries(data=data, data_key="product_revenue", data_row_multiplier=1, QTM_data_tables=QTM_data_tables, QTM_row=117, relative_tolerance=0.001)
        test_timeseries(data=data, data_key="token_buys", data_row_multiplier=1, QTM_data_tables=QTM_data_tables, QTM_row=119, relative_tolerance=0.001)

        
        ## TEST TOKEN ALLOCATION REMOVAL PERCENTAGE ##
        print("\n-------------------------------## TEST TOKEN UTILITY REMOVAL PERCENTAGE ##------------------------------")
        print("Testing token utility removal percentage of radCad timeseries simulation against QTM data tables...")
        test_timeseries(data=data, data_key="remove_perc", data_row_multiplier=100, QTM_data_tables=QTM_data_tables, QTM_row=123, relative_tolerance=0.001)

        
        ## TEST BUYBACK FROM REVENUE SHARE FOR STAKERS ##
        print("\n----------------------------## TEST BUYBACK FROM REVENUE SHARE FOR STAKERS ##---------------------------")
        print("Testing token utility removal percentage of radCad timeseries simulation against QTM data tables...")
        test_timeseries(data=data, data_key="buyback_from_revenue_share_usd", data_row_multiplier=1, QTM_data_tables=QTM_data_tables, QTM_row=133, relative_tolerance=0.001)

        
        ## TEST SUM OF BUYBACKS ##
        print("\n----------------------------------------## TEST SUM OF BUYBACKS ##--------------------------------------")
        print("Testing sum of buybacks of radCad timeseries simulation against QTM data tables...")
        test_timeseries(data=data, data_key="buybacks_usd", data_row_multiplier=1, QTM_data_tables=QTM_data_tables, QTM_row=134, relative_tolerance=0.001)


        ## TEST PROTOCOL BUCKET BURN ##
        print("\n----------------------------------------## TEST PROTOCOL BUCKET BURN ##--------------------------------------")
        print("Testing protocol bucket burn of radCad timeseries simulation against QTM data tables...")
        test_timeseries(data=data, data_key="tokens_burned", data_row_multiplier=1, QTM_data_tables=QTM_data_tables, QTM_row=138, relative_tolerance=0.001)


        ## TEST LIQUIDITY POOL TRANSACTIONS ##
        print("\n-------------------------------------## TEST LIQUIDITY POOL TRANSACTIONS ##-----------------------------------")
        print("Testing liquidity pool transactions of radCad timeseries simulation against QTM data tables...")
        print("Tx1 - after adoption..")
        test_timeseries(data=data_tx1, data_key="tokens", data_row_multiplier=1, QTM_data_tables=QTM_data_tables, QTM_row=141, relative_tolerance=0.001, timestep_cut_off=1)
        test_timeseries(data=data_tx1, data_key="usdc", data_row_multiplier=1, QTM_data_tables=QTM_data_tables, QTM_row=142, relative_tolerance=0.001, timestep_cut_off=1)
        test_timeseries(data=data_tx1, data_key="token_price", data_row_multiplier=1, QTM_data_tables=QTM_data_tables, QTM_row=143, relative_tolerance=0.01, timestep_cut_off=1)
        print("Tx2 - after vesting sell..")
        test_timeseries(data=data_tx2, data_key="tokens", data_row_multiplier=1, QTM_data_tables=QTM_data_tables, QTM_row=144, relative_tolerance=0.001, timestep_cut_off=1)
        test_timeseries(data=data_tx2, data_key="usdc", data_row_multiplier=1, QTM_data_tables=QTM_data_tables, QTM_row=145, relative_tolerance=0.001, timestep_cut_off=1)
        test_timeseries(data=data_tx2, data_key="token_price", data_row_multiplier=1, QTM_data_tables=QTM_data_tables, QTM_row=146, relative_tolerance=0.01, timestep_cut_off=1)
        print("Tx3 - after liquidity addition..")
        test_timeseries(data=data_tx3, data_key="tokens", data_row_multiplier=1, QTM_data_tables=QTM_data_tables, QTM_row=147, relative_tolerance=0.001, timestep_cut_off=1)
        test_timeseries(data=data_tx3, data_key="usdc", data_row_multiplier=1, QTM_data_tables=QTM_data_tables, QTM_row=148, relative_tolerance=0.001, timestep_cut_off=1)
        test_timeseries(data=data_tx3, data_key="token_price", data_row_multiplier=1, QTM_data_tables=QTM_data_tables, QTM_row=149, relative_tolerance=0.01, timestep_cut_off=1)
        print("Tx4 - after buyback..")
        test_timeseries(data=data_tx4, data_key="tokens", data_row_multiplier=1, QTM_data_tables=QTM_data_tables, QTM_row=150, relative_tolerance=0.001, timestep_cut_off=1)
        test_timeseries(data=data_tx4, data_key="usdc", data_row_multiplier=1, QTM_data_tables=QTM_data_tables, QTM_row=151, relative_tolerance=0.001, timestep_cut_off=1)
        test_timeseries(data=data_tx4, data_key="token_price", data_row_multiplier=1, QTM_data_tables=QTM_data_tables, QTM_row=152, relative_tolerance=0.01, timestep_cut_off=1)


        ## TEST LIQUIDITY POOL VALUATION AND VOLATILITY ##
        print("\n-------------------------------## TEST LIQUIDITY POOL VALUATION AND VOLATILITY ##------------------------------")
        print("Testing liquidity pool valuation and volatility of radCad timeseries simulation against QTM data tables...")
        test_timeseries(data=data, data_key="lp_valuation", data_row_multiplier=1, QTM_data_tables=QTM_data_tables, QTM_row=154, relative_tolerance=0.001, timestep_cut_off=1)
        test_timeseries(data=data, data_key="volatility", data_row_multiplier=1, QTM_data_tables=QTM_data_tables, QTM_row=156, relative_tolerance=0.001, timestep_cut_off=1)

        
        ## TEST CASH BALANCE ##
        print("\n-----------------------------------------## TEST CASH BALANCE ##----------------------------------------")
        print("Testing cash balance of radCad timeseries simulation against QTM data tables...")
        test_timeseries(data=data, data_key="cash_balance", data_row_multiplier=1, QTM_data_tables=QTM_data_tables, QTM_row=184, relative_tolerance=0.001)


        """ ## TEST A SUPPLY ##
        print("\n-------------------------------------## TEST CIRCULATING SUPPLY ##-------------------------------------")
        print("Testing circulating supply of radCad timeseries simulation against QTM data tables...")
        test_timeseries(data=data, data_key="circulating_supply", QTM_data_tables=QTM_data_tables, QTM_row=182, relative_tolerance=0.001)"""
        
        
      ## TEST APR ##
        print("\n---------------------------------------## Rewards apr ##--------------------------------------")
        print("Testing apr of radCad timeseries simulation against QTM data tables...")
        test_timeseries(data=data, data_key="staking_rewards", data_row_multiplier=1, QTM_data_tables=QTM_data_tables, QTM_row=159, relative_tolerance=0.001, timestep_cut_off=1)
       #NOT READY TO TEST YET ->    test_timeseries(data=data, data_key="apr_tokens_usd", data_row_multiplier=1, QTM_data_tables=QTM_data_tables, QTM_row=166, relative_tolerance=0.001)

        ### END OF TESTS ###
        print("\n")
        print(u'\u2713'+" ALL TESTS PASSED!")
        print("\n------------------------------------")

    else:

    # holding
        test_timeseries(data=data, data_key="holding_allocation", data_row_multiplier=1, QTM_data_tables=QTM_data_tables, QTM_row=107, relative_tolerance=0.001, timestep_cut_off=1)



