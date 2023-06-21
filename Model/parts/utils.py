import numpy as np
import math
import uuid
import random
from typing import *

# Helper Functions
# function that transforms the single values in a dictionary into list elements of the same value within the same dictionary
def transform_dict_signle_values_into_list_elements(dictionary):
    for key, value in dictionary.items():
        dictionary[key] = [value]
    return dictionary

def calculate_raised_capital(sys_param):
    """
    Calculate the overall raised capital from the initial investors.
    """

    raised_capital = 0
    for key, value in sys_param:
        if "_raised" in key:
            raised_capital += value

    return raised_capital

# Initialization
def new_agent(stakeholder_type: str, usd_funds: int,
              tokens: int, action_list: list, action_weights: Tuple,
              current_action: str) -> dict:
    """
    Function to create a new agent aka stakeholder for the token ecosystem.
    """

    agent = {'type': stakeholder_type,
             'usd_funds': usd_funds,
             'tokens': tokens,
             'tokens_vested': 0,
             'tokens_locked': 0,
             'action_list': action_list,
             'action_weights': action_weights,
             'current_action': current_action}
    return agent

def generate_agents(initial_value):
    """
    Initialize all token ecosystem agents aka stakeholders.
    """

    agents_dict = initial_value["initial_agent_values"]
    initial_agents = {}
    for a in agents_dict:
        initial_agents[a] = new_agent(a['type'],
                                    a['initial_usd_funds'],
                                    a['initial_tokens'],
                                    a['initial_tokens_vested'],
                                    a['initial_tokens_locked'],
                                    a['action_list'],
                                    a['action_weights'],
                                    a['current_action'])
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

    token_launch_price = sys_param["public_sale_valuation"] / sys_param["initial_total_supply"]
    effective_token_price = np.min([token_launch_price / (1+sys_param[stakeholder_name+"_bonus"]/100), sys_param[stakeholder_name+"_valuation"] / sys_param["initial_total_supply"]])
    tokens = sys_param[stakeholder_name+"_raised"] / effective_token_price
    allocation = tokens / sys_param['initial_total_supply']
    
    return allocation

def calc_initial_lp_tokens(agent_token_allocations, sys_param):
    """
    Calculate the amount of tokens initially allocated to the DEX liquidity pool.
    """

    allocation_sum = 0

    for agent, allocation in agent_token_allocations.items():
        allocation_sum += allocation
    
    lp_token_allocation = (100-allocation_sum) * sys_param['initial_total_supply']

    return lp_token_allocation


def seed_dex_liquidity(agent_token_allocations, initial_stakeholders, funding_bucket_name, sys_param):
    """
    Calculate the initial token amounts in the liquidity pool.
    """

    public_sale_valuation = sys_param['public_sale_valuation']
    initial_token_supply = sys_param['initial_total_supply']
    sum_of_raised_capital = calculate_raised_capital(sys_param)
    initial_token_price = public_sale_valuation / initial_token_supply
    lp_token_allocation = calc_initial_lp_tokens(agent_token_allocations, sys_param)

    required_usdc = lp_token_allocation * initial_token_price

    if required_usdc > sum_of_raised_capital:
        raise ValueError('The required funds to seed the DEX liquidity are '+str(required_usdc)+' and higher than the sum of raised capital '+str(sum_of_raised_capital)+'!')
    else:
        # subtract the required funds from the funding bucket.
        found_stakeholder = False
        for stakeholder in initial_stakeholders:
            if initial_stakeholders[stakeholder]['type'] == funding_bucket_name:
                initial_stakeholders[stakeholder]['initial_usd_funds'] -= required_usdc
                if initial_stakeholders[stakeholder]['initial_usd_funds'] < 0:
                    raise ValueError("The stakeholder "+funding_bucket_name+" has only $"+str(initial_stakeholders[stakeholder]['initial_usd_funds']+required_usdc)+" funds, but $"+str(required_usdc)+" are required for seeding the DEX liquidity pool!")
                found_stakeholder = True
        
        if not found_stakeholder:
            raise ValueError("The DEX liquidity couldn't be funded as there is no stakeholder with name: "+funding_bucket_name)
    
    liquidity_pool = {
        'tokens' : lp_token_allocation,
        'usdc' : required_usdc,
        'constant_product' : lp_token_allocation * required_usdc,
        'token_price' : required_usdc / lp_token_allocation
    }

    return liquidity_pool

def generate_initial_token_economy_metrics(initial_stakeholders, initial_liquidity_pool, sys_param):
    """
    Calculate the initial token economy metrics, such as MC, FDV MC, circ. supply, and tokens locked.
    """

    initial_circulating_tokens = 0
    initial_locked_tokens = 0

    for stakeholder in initial_stakeholders:
        initial_circulating_tokens += initial_stakeholders[stakeholder]['tokens']
        initial_locked_tokens += initial_stakeholders[stakeholder]['tokens_locked']
    
    initial_MC = initial_liquidity_pool['token_price'] * initial_circulating_tokens
    initial_FDV_MC = initial_liquidity_pool['token_price'] * sys_param['initial_total_supply']

    token_economy = {
        'total_supply' : sys_param['initial_total_supply'],
        'circulating_supply' : initial_circulating_tokens,
        'MC' : initial_MC,
        'FDV_MC' : initial_FDV_MC,
        'tokens_locked' : initial_locked_tokens
    }

    return token_economy

