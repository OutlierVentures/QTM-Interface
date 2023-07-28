import numpy as np
import math
import uuid
import random
from datetime import datetime
from typing import *
import pandas as pd

# Helper Functions
def convert_date(sys_param):
    if "." in sys_param['launch_date'][0]:
        return datetime.strptime(sys_param['launch_date'][0],'%d.%m.%y')
    elif "/" in sys_param:
        return datetime.strptime(sys_param['launch_date'][0],'%d/%m/%Y')

def calculate_raised_capital(param):
    """
    Calculate the overall raised capital from the initial investors.
    """

    raised_capital = 0
    # calculate the raised capital for all investors in sys_param where "_raised" is in the key
    raised_capital = sum([param[key] if ("_raised" in key) else 0 for key in param])

    return raised_capital

# Initialization
def new_agent(stakeholder_name: str, stakeholder_type: str, usd_funds: float,
              tokens: float, tokens_vested: float, tokens_vested_cum: float, tokens_apr_locked: float,
              tokens_buyback_locked: float, tokens_liquidity_provisioning: float, tokens_transferred: float,
              tokens_transferred_cum: float, tokens_burned: float, tokens_burned_cum: float, action_list: list,
              action_weights: Tuple, current_action: str) -> dict:
    """
    Function to create a new agent aka stakeholder for the token ecosystem.
    """

    agent = {'name': stakeholder_name, # 'incentivisation', 'placeholder', 'market_investors
             'type': stakeholder_type,
             'usd_funds': usd_funds,
             'tokens': tokens,
             'tokens_vested': tokens_vested,
             'tokens_vested_cum': tokens_vested_cum,
             'tokens_apr_locked': tokens_apr_locked,
             'tokens_buyback_locked': tokens_buyback_locked,
             'tokens_liquidity_provisioning': tokens_liquidity_provisioning,
             'tokens_transferred': tokens_transferred,
             'tokens_transferred_cum': tokens_transferred_cum,
             'tokens_burned': tokens_burned,
             'tokens_burned_cum': tokens_burned_cum,
             'action_list': action_list,
             'action_weights': action_weights,
             'current_action': current_action}
    return agent

def generate_agents(stakeholder_name_mapping: dict) -> dict:
    """
    Initialize all token ecosystem agents aka stakeholders.
    """

    initial_agents = {}
    for stakeholder_name, stakeholder_type in stakeholder_name_mapping.items():
        initial_agents[uuid.uuid4()] = new_agent(stakeholder_name = stakeholder_name,
                                    stakeholder_type = stakeholder_type,
                                    usd_funds = 0,
                                    tokens = 0,
                                    tokens_vested = 0,
                                    tokens_vested_cum = 0,
                                    tokens_apr_locked = 0,
                                    tokens_buyback_locked = 0,
                                    tokens_liquidity_provisioning = 0,
                                    tokens_transferred = 0,
                                    tokens_transferred_cum = 0,
                                    tokens_burned = 0,
                                    tokens_burned_cum = 0,
                                    action_list = [],
                                    action_weights = [],
                                    current_action = 'hold')
    return initial_agents

def create_parameter_list(parameter_name, not_iterable_parameters, init_value, min, max, intervals):
    """
    Create list of parameters for parameter sweep based on the QTM input tab 'cadCAD_inputs'.
    """

    if parameter_name in not_iterable_parameters:
        return [init_value.replace(",","").replace("%","")]
    else:
        try:
            if type(init_value) == str:
                init_value = float(init_value.replace(",","").replace("%",""))
            if type(min) == str:
                min = float(min.replace(",","").replace("%",""))
            if type(max) == str:
                max = float(max.replace(",","").replace("%",""))
            if type(intervals) == str and intervals != '':
                intervals = int(float(intervals.replace(",","")).replace("%",""))
        except ValueError:
            return [init_value]
        if math.isnan(min) or math.isnan(max) or math.isnan(intervals) or max<=min:
            if max<=min:
                print("Maximum parameter boundary is lower than minimum parameter boundary: Min: ", min, "; Max:", max, ". Using initial value ", init_value, " instead.")
            return [float(init_value)]
        else:
            if math.isnan(intervals):
                return [float(init_value)]
            else:
                return list(np.linspace(min, max, int(intervals)))

def compose_initial_parameters(QTM_inputs, not_iterable_parameters):
    """
    Compose all initial parameter sets from the Quantitative Token Model inputs tab 'cadCAD_inputs'.
    """

    initial_parameters = {}
    for index, row in QTM_inputs.iterrows():
        parameter_name = row['Parameter Name'].lower().replace(' ', '_').replace('/', '').replace('(', '').replace(')', '')
        initial_parameters[parameter_name] = create_parameter_list(parameter_name, not_iterable_parameters, row['Initial Value'], row['Min'], row['Max'], row['Interval Steps'])
    return initial_parameters

def calculate_investor_allocation(sys_param, stakeholder_name):
    """
    Calculate the initial token allocation of a specific stakeholder considering bonus amounts.
    """
    token_launch_price = [x / y for x in sys_param["public_sale_valuation"] for y in sys_param["initial_total_supply"]]
    effective_token_price = [np.min([x / (1+y/100), z / a]) for x in token_launch_price for y in sys_param[stakeholder_name+"_bonus"] for z in sys_param[stakeholder_name+"_valuation"] for a in sys_param["initial_total_supply"] for a in sys_param["initial_total_supply"]]
    tokens = [x / y for x in sys_param[stakeholder_name+"_raised"] for y in effective_token_price]
    allocation = [x / y for x in tokens for y in sys_param['initial_total_supply']]
    
    return allocation

def calc_initial_lp_tokens(agent_token_allocations, sys_param):
    """
    Calculate the amount of tokens initially allocated to the DEX liquidity pool.
    """

    allocation_sum = []
    # get max length of possible raised_capital parameters
    max_length = max([len(agent_token_allocations[key]) for key in agent_token_allocations])
    # calculate the raised capital for all possible parameter list combinations in sys_param where "_raised" is in the key
    for i in range(max_length):
        allocation_sum.append(sum([agent_token_allocations[key][i] if (i < len(agent_token_allocations[key])) else agent_token_allocations[key][-1] for key in agent_token_allocations]))
    
    lp_token_allocation = [(1 - x) * y for x in allocation_sum for y in sys_param['initial_total_supply']]

    return lp_token_allocation


def initialize_dex_liquidity():
    """
    Initialize the DEX liquidity pool.
    """
    liquidity_pool = {
        'tokens' : 0,
        'usdc' : 0,
        'constant_product' : 0,
        'token_price' : 0
    }

    return liquidity_pool

def generate_initial_token_economy_metrics():
    """
    Set the initial token economy metrics, such as MC, FDV MC, circ. supply, and tokens locked.
    """
    token_economy = {
        'total_supply' : 0,
        'circulating_supply' : 0,
        'MC' : 0,
        'FDV_MC' : 0,
        'selling_perc': 0,
        'utility_perc': 0,
        'holding_perc': 0,
        'tokens_apr_locked' : 0,
        'tokens_buyback_locked' : 0,
        'tokens_vested_cum': 0,
        'tokens_burned': 0,
        'minted_tokens' : 0,
        'incentivised_tokens' : 0,
        'incentivised_tokens_usd' : 0,
        'incentivised_tokens_cum' : 0,
        'airdrop_tokens' : 0,
        'airdrop_tokens_usd' : 0,
        'airdrop_tokens_cum' : 0
    }

    return token_economy



def initialize_user_adoption():
    """
    Initialize the user adoption metrics.
    """
    user_adoption = {
    'product_users': 0,
    'token_holders': 0,
    'product_revenue':0,
    'token_buys': 0
    }

    return user_adoption




def initialize_business_assumptions():
    """
    Initialize the business assumptions metrics.
    """
    business_assumptions = {
    'cash_balance': 0, ## Row 184 in model
    }

    return business_assumptions


def initialize_staking_base_apr():
    """
    Initialize the staking base apr metrics.
    """
    staking_base_apr = {
    'staking_base_apr_cum':0,
    }

    return staking_base_apr




def initalize_meta_bucket_allocations():
    """
    Initialize the business assumptions metrics.
    """
    meta_bucket_allocations = {
        'selling': 0,
        'holding': 0,
        'utility': 0,
        'removed': 0
    }
    return meta_bucket_allocations


### TEST FUNCTIONS ###
def test_timeseries(data, data_key, data_row_multiplier, QTM_data_tables, QTM_row, relative_tolerance=0.001):
    print("Testing "+data_key+" of radCad timeseries simulation at QTM row "+str(QTM_row)+" ("+QTM_data_tables.iloc[QTM_row-2].values[1]+")...")
    for i in range(len(QTM_data_tables.iloc[QTM_row-2].values[2:-1])):
        # get testing values
        QTM_data_table_value = float(QTM_data_tables.iloc[QTM_row-2].values[2:-1][i].replace(",",""))
        radCAD_value = float(data[data_key].values[i]) * data_row_multiplier

        # assert the values
        error_message = ("radCad simulation value "+data_key+" = "+ str(radCAD_value)
        + " at timestep "+str(i+1)+" is not equal to the QTM data table value "+ str(QTM_data_table_value)+" at row "+str(QTM_row)
        +" and date "+str(QTM_data_tables.iloc[3].values[2:-1][i])+". The difference is "+str(radCAD_value - QTM_data_table_value)+" or "
        +str([radCAD_value/QTM_data_table_value * 100 if QTM_data_table_value!= 0 else "NaN"][0])+"%.")

        np.testing.assert_allclose(radCAD_value, QTM_data_table_value, rtol=relative_tolerance, err_msg=error_message)
    print(u'\u2713'+" Test passed!")
    print("------------------------------------")