"""Initialisation, testing, and minor helper functions.

Functions:
    convert_date:

    calculate_raised_capital:

    new_agent:

    generate_agents:

    create_parameter_list:

    compose_initial_parameters:

    calculate_investor_allocation:

    calc_initial_lp_tokens:

    initialize_dex_liquidity:

    generate_initial_token_economy_metrics:

    initialize_user_adoption:

    initialize_business_assumptions:

    initialize_utilities:

    test_timeseries:

    import_dummy_data:

    convert_to_json:

"""

import numpy as np
import math
import uuid
import random
import sys
import os
from datetime import datetime
from typing import *
import pandas as pd
import json
import sqlite3

# Helper Functions
def convert_date(sys_param):
    if type(sys_param['launch_date'][0]) == datetime:
        date_transformed = sys_param['launch_date'][0].strftime("%d.%m.%Y")
    else:
        date_transformed = sys_param['launch_date'][0]

    if "." in date_transformed:
        return datetime.strptime(date_transformed,'%d.%m.%Y')
    elif "/" in sys_param:
        return datetime.strptime(date_transformed,'%d/%m/%Y')
    elif "-" in sys_param:
        return datetime.strptime(date_transformed,'%d-%m-%Y')

def get_initial_date(sys_param):
    initial_date = pd.to_datetime(sys_param['launch_date'][0] if isinstance(sys_param['launch_date'], list) else sys_param['launch_date'], format='%d.%m.%Y')
    # use the following code if you want to use the token launch date as the initial date this would forward the user adoption accordingly.
    if 'token_launch' in sys_param:
        token_launch = sys_param['token_launch'][0] if isinstance(sys_param['token_launch'], list) else sys_param['token_launch']
        if not token_launch:
            # set initial date to today's date
            initial_date = pd.to_datetime('today')
    return initial_date

def calculate_raised_capital(param):
    """
    Calculate the overall raised capital from the initial investors.
    """

    raised_capital = 0
    # calculate the raised capital for all investors in sys_param where "_raised" is in the key
    raised_capital = sum([param[key][0] if ("_raised" in key) and isinstance(param[key], list) else param[key] if ("_raised" in key) else 0 for key in param])

    return raised_capital

# Initialization
def new_agent(stakeholder_name: str, stakeholder_type: str, usd_funds: float,
              tokens: float, tokens_vested: float, tokens_vested_cum: float, 
              tokens_airdropped: float, tokens_airdropped_cum: float, tokens_incentivised: float, tokens_incentivised_cum: float,
              tokens_staked: float, tokens_staked_cum: float, tokens_staked_remove: float,
              tokens_staking_buyback_rewards: float, tokens_staking_buyback_rewards_cum: float, tokens_staking_vesting_rewards: float, tokens_staking_vesting_rewards_cum: float,
              tokens_staking_minting_rewards: float, tokens_staking_minting_rewards_cum: float, tokens_liquidity_mining: float, tokens_liquidity_mining_cum: float, tokens_liquidity_mining_remove: float,
              tokens_liquidity_mining_rewards: float, tokens_liquidity_mining_rewards_cum: float, tokens_transferred: float, tokens_transferred_cum: float, tokens_burned: float, tokens_burned_cum: float,
              selling_tokens: float, utility_tokens: float, selling_from_holding_tokens: float, utility_from_holding_tokens: float,
              holding_from_holding_tokens: float, holding_tokens: float, actions: dict, current_action: str) -> dict:
    """
    Function to create a new agent aka stakeholder for the token ecosystem.
    """
    agent = {'a_name': stakeholder_name, # seed, advisor, reserve, incentivisation, staking_vesting, market_investors, etc.
             'a_type': stakeholder_type, # early_investor, protocol_bucket, market_investors, airdrop_receiver, incentivisation_receiver
             'a_usd_funds': usd_funds, # amount of USD funds available to this stakeholder (not applicalbe/used in the current version)
             'a_tokens': tokens, # amount of held tokens by this stakeholder group
             'a_tokens_vested': tokens_vested, # amount of vested tokens per timestep
             'a_tokens_vested_cum': tokens_vested_cum, # amount of vested tokens cumulatively
             'a_tokens_airdropped': tokens_airdropped, # amount of airdropped tokens per timestep
             'a_tokens_airdropped_cum': tokens_airdropped_cum, # amount of airdropped tokens cumulatively
             'a_tokens_incentivised': tokens_incentivised, # amount of incentivised tokens per timestep
             'a_tokens_incentivised_cum': tokens_incentivised_cum, # amount of incentivised tokens cumulatively
             'a_tokens_staked': tokens_staked, # amount of tokens staked per timestep
             'a_tokens_staked_cum': tokens_staked_cum, # amount of tokens staked cumulatively
             'a_tokens_staked_remove': tokens_staked_remove, # amount of tokens removed from staking
             'a_tokens_staking_buyback_rewards': tokens_staking_buyback_rewards, # amount of token rewards for staking for buyback share
             'a_tokens_staking_buyback_rewards_cum': tokens_staking_buyback_rewards_cum, # amount of token rewards for staking for buyback share cumulative
             'a_tokens_staking_vesting_rewards': tokens_staking_vesting_rewards, # amount of token rewards for staking for staking vesting
             'a_tokens_staking_vesting_rewards_cum': tokens_staking_vesting_rewards_cum, # amount of token rewards for staking for staking vesting cumulative
             'a_tokens_staking_minting_rewards': tokens_staking_minting_rewards, # amount of token rewards for staking for minting from mint & burn mechanism
             'a_tokens_staking_minting_rewards_cum': tokens_staking_minting_rewards_cum, # amount of token rewards for staking for minting from mint & burn mechanism cumulative
             'a_tokens_liquidity_mining': tokens_liquidity_mining, # amount of tokens used for liquidity mining per timestep
             'a_tokens_liquidity_mining_cum': tokens_liquidity_mining_cum, # amount of tokens used for liquidity mining cumulatively
             'a_tokens_liquidity_mining_remove': tokens_liquidity_mining_remove, # amount of tokens removed from liquidity mining
             'a_tokens_liquidity_mining_rewards': tokens_liquidity_mining_rewards, # amount of token rewards for liquidity mining
             'a_tokens_liquidity_mining_rewards_cum': tokens_liquidity_mining_rewards_cum, # amount of token rewards for liquidity mining cumulative
             'a_tokens_transferred': tokens_transferred, # amount of tokens transferred per timestep
             'a_tokens_transferred_cum': tokens_transferred_cum, # amount of tokens transferred cumulatively
             'a_tokens_burned': tokens_burned, # amount of tokens burned per timestep
             'a_tokens_burned_cum': tokens_burned_cum, # amount of tokens burned cumulatively
             'a_selling_tokens': selling_tokens, # agent meta bucket selling allocations
             'a_utility_tokens': utility_tokens, # agent meta bucket utility allocations
             'a_holding_tokens': holding_tokens, # agent meta bucket holding allocations
             'a_selling_from_holding_tokens': selling_from_holding_tokens, # selling from holding allocations
             'a_utility_from_holding_tokens': utility_from_holding_tokens, # utility from holding allocations
             'a_holding_from_holding_tokens': holding_from_holding_tokens, # holding from holding allocations
             'a_actions': actions, # dictionary of actions taken by this stakeholder
             'a_current_action': current_action # current action taken by this stakeholder
             }
    return agent


def generate_agents(stakeholder_name_mapping: dict, sys_param: dict) -> dict:
    """
    Initialize all token ecosystem agents aka stakeholders.
    """
    
    initial_agents = {}
    for stakeholder_name, stakeholder_type in stakeholder_name_mapping.items():

        initial_total_supply = sys_param['initial_total_supply'][0]
        agent_token_allocation = [sys_param[stakeholder_name+"_token_allocation"][0] if stakeholder_name+"_token_allocation" in sys_param else 0][0]
        agent_initial_vesting_perc = [sys_param[stakeholder_name+"_initial_vesting"][0] if stakeholder_name+"_initial_vesting" in sys_param else 0][0]
        initial_agent_tokens_vested = (agent_initial_vesting_perc / 100) * (agent_token_allocation * initial_total_supply)
        
        if 'token_launch' in sys_param:
            token_launch = sys_param['token_launch'][0]
            current_staked = sys_param[f'{stakeholder_name}_current_staked'][0] if not token_launch and f'{stakeholder_name}_current_staked' in sys_param else 0            
            vested = sys_param[f'{stakeholder_name}_vested_init'][0] if not token_launch and f'{stakeholder_name}_vested_init' in sys_param else initial_agent_tokens_vested
            current_holdings = sys_param[f'{stakeholder_name}_current_holdings'][0] if not token_launch and f'{stakeholder_name}_current_holdings' in sys_param else vested if stakeholder_name != 'incentivisation' else 0
            tokens_incentivised_cum = sys_param[f'{stakeholder_name}_current_holdings'][0] + sys_param[f'{stakeholder_name}_current_staked'][0] if not token_launch and (f'{stakeholder_name}_current_staked' in sys_param and stakeholder_name == 'incentivisation_receivers') else 0
            tokens_airdropped_cum = sys_param[f'{stakeholder_name}_current_holdings'][0] + sys_param[f'{stakeholder_name}_current_staked'][0] if not token_launch and (f'{stakeholder_name}_current_staked' in sys_param and stakeholder_name == 'airdrop_receivers') else 0
        else:         
            current_staked = 0
            vested = initial_agent_tokens_vested
            current_holdings = vested
            tokens_incentivised_cum = 0
            tokens_airdropped_cum = 0

        initial_agents[uuid.uuid4()] = new_agent(stakeholder_name = stakeholder_name,
                                    stakeholder_type = stakeholder_type,
                                    usd_funds = 0,
                                    tokens = current_holdings,
                                    tokens_vested = 0,
                                    tokens_vested_cum = vested,
                                    tokens_airdropped = 0,
                                    tokens_airdropped_cum = tokens_airdropped_cum,
                                    tokens_incentivised = 0,
                                    tokens_incentivised_cum = tokens_incentivised_cum,
                                    tokens_staked = 0,
                                    tokens_staked_cum = current_staked,
                                    tokens_staked_remove = 0,
                                    tokens_staking_buyback_rewards = 0,
                                    tokens_staking_buyback_rewards_cum = 0,
                                    tokens_staking_vesting_rewards = 0,
                                    tokens_staking_vesting_rewards_cum = 0,
                                    tokens_staking_minting_rewards = 0,
                                    tokens_staking_minting_rewards_cum = 0,
                                    tokens_liquidity_mining = 0,
                                    tokens_liquidity_mining_cum = 0,
                                    tokens_liquidity_mining_remove = 0,
                                    tokens_liquidity_mining_rewards = 0,
                                    tokens_liquidity_mining_rewards_cum = 0,
                                    tokens_transferred = 0,
                                    tokens_transferred_cum = 0,
                                    tokens_burned = 0,
                                    tokens_burned_cum = 0,
                                    selling_tokens = 0,
                                    utility_tokens = 0,
                                    holding_tokens = 0,
                                    selling_from_holding_tokens = 0,
                                    utility_from_holding_tokens = 0,
                                    holding_from_holding_tokens = 0,
                                    actions = {},
                                    current_action = 'hold')

    return initial_agents

def create_parameter_list(parameter_name, not_iterable_parameters, init_value, min, max, intervals):
    """
    Create list of parameters for parameter sweep based on the QTM input tab 'cadCAD_inputs'.
    """

    if parameter_name in not_iterable_parameters:
        return [str(init_value).replace(",","").replace("%","")]
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
    3
    return allocation


def calculate_investor_effective_token_price(sys_param, stakeholder_name):
    """
    Calculate the initial token allocation of a specific stakeholder considering bonus amounts.
    """
    token_launch_price = [x / y for x in sys_param["public_sale_valuation"] for y in sys_param["initial_total_supply"]]
    effective_token_price = [np.min([x / (1+y/100), z / a]) for x in token_launch_price for y in sys_param[stakeholder_name+"_bonus"] for z in sys_param[stakeholder_name+"_valuation"] for a in sys_param["initial_total_supply"] for a in sys_param["initial_total_supply"]]
    return effective_token_price

def calc_initial_lp_tokens(agent_token_allocations, sys_param):
    """
    Calculate the amount of tokens initially allocated to the DEX liquidity pool.
    """

    allocation_sum = []
    # get max length of possible raised_capital parameters
    max_length = max([len(agent_token_allocations[key]) for key in agent_token_allocations])
    
    # calculate the liquidity pool token allocation by summing up the token allocations of all agents and subtracting it from 1 (100%)
    for i in range(max_length):
        allocation_sum.append(sum([agent_token_allocations[key][i] if (i < len(agent_token_allocations[key])) else agent_token_allocations[key][-1] for key in agent_token_allocations]))
    
    lp_token_allocation = [(1 - x) * y for x in allocation_sum for y in sys_param['initial_total_supply']]

    # check if all lp_token_allocations are > 0
    if any([x < 0 for x in lp_token_allocation]):
        raise ValueError("Error: LP token allocation is negative. Please check the initial token allocations of the agents.")

    return lp_token_allocation

def calculate_user_adoption(initial_users,final_users,velocity,timestamp):
    """
    Take in user adoption data and calculate the amount of adoption.

    Can be used for token adoption and product users.
  
    Args:
        initial_users: starting amount of users
        final_users: ending amount of users
        velocity: speed of adoption on those users
        timstep: current timestep in days
    
    Returns:
        Number representing the user adoption.    

    """
    # This is what is shown in the model as a constant as the user adoption numbers refer to 10 years (product_users_after_10y & token_holers_after_10y)
    total_days = 3653

    term1 = (1 / (1 + math.exp(-velocity * 0.002 * (timestamp - 1825 / velocity)))) * final_users + initial_users
    term2 = (1 / (1 + math.exp(-velocity * 0.002 * (0 - 1825 / velocity)))) * final_users
    term3 = initial_users * (timestamp / total_days)
    term4 = final_users - (term1 - term2 - term3)
    result = term1 - term2 - term3 + (term4 * (timestamp / total_days))
    
    return result

def initialize_dex_liquidity(sys_param):
    """
    Initialize the DEX liquidity pool.
    """
    required_usdc = sys_param['initial_required_usdc'][0]
    required_tokens = sys_param['initial_lp_token_allocation'][0]
    total_token_supply = sys_param['initial_total_supply'][0]
    token_launch = sys_param['token_launch'][0] if 'token_launch' in sys_param else True
    token_fdv = sys_param['token_fdv'][0] if not token_launch else 0

    if 'token_launch' in sys_param:
            token_launch = sys_param['token_launch'][0]
            if not token_launch:
                token_price = token_fdv / total_token_supply
                lp_tokens = required_tokens
                lp_usdc = token_price * required_tokens
                lp_constant_product = lp_tokens * lp_usdc

            else:
                constant_product = required_usdc * required_tokens
                token_price = required_usdc / required_tokens

                # initialize the liquidity pool from the system parameters
                lp_tokens = required_tokens
                lp_usdc = required_usdc
                lp_constant_product = constant_product
            
                # check if required funds are available from funds raised
                sum_of_raised_capital = calculate_raised_capital(sys_param)

                if required_usdc > sum_of_raised_capital:
                    raise ValueError(f'The required funds to seed the DEX liquidity are {required_usdc}, '
                                    f'which is higher than the sum of raised capital {sum_of_raised_capital}!')
    else:
        constant_product = required_usdc * required_tokens
        token_price = required_usdc / required_tokens

        # initialize the liquidity pool from the system parameters
        lp_tokens = required_tokens
        lp_usdc = required_usdc
        lp_constant_product = constant_product

        # check if required funds are available from funds raised
        sum_of_raised_capital = calculate_raised_capital(sys_param)

        if required_usdc > sum_of_raised_capital:
            raise ValueError(f'The required funds to seed the DEX liquidity are {required_usdc}, '
                            f'which is higher than the sum of raised capital {sum_of_raised_capital}!')


    liquidity_pool = {
        'lp_tokens' : lp_tokens, # amount of native protocol tokens in LP
        'lp_usdc' : lp_usdc, # amount of USDC in LP
        'lp_constant_product' : lp_constant_product, # constant product of LP tokens and USDC
        'lp_token_price' : token_price, # price of LP token
        'lp_valuation': lp_usdc * 2, # valuation of LP tokens
        'lp_volatility': 0, # volatility of LP tokens
        'lp_token_price_max': 0, # max price of LP token
        'lp_token_price_min': 0, # min price of LP token
        'lp_tokens_after_adoption': 0, # tokens after adoption tx 1
        'lp_tokens_after_liquidity_addition':0, # Token after liquidity addition tx 3
        'lp_tokens_after_buyback': 0 # tokens after buy back tx 4
    }

    return liquidity_pool

def generate_initial_token_economy_metrics(initial_stakeholders, initial_liquidity_pool, sys_param):
    """
    Set the initial token economy metrics, such as MC, FDV MC, and circ. supply.
    """

    if 'token_launch' in sys_param:
        token_launch = sys_param['token_launch'][0]
        token_fdv = sys_param['token_fdv'][0] if not token_launch else sys_param['public_sale_valuation'][0]
    else:
        token_fdv = sys_param['public_sale_valuation'][0]
    
    initial_total_supply = sys_param['initial_total_supply'][0]
    tokens_holding_cum = sum([initial_stakeholders[agent]['a_tokens'] for agent in initial_stakeholders if initial_stakeholders[agent]['a_type'] != 'protocol_bucket'])
    tokens_vested_cum = sum([initial_stakeholders[agent]['a_tokens_vested_cum'] if initial_stakeholders[agent]['a_tokens_vested_cum']>0 else initial_stakeholders[agent]['a_tokens'] for agent in initial_stakeholders])
    tokens_airdropped_cum = sum([initial_stakeholders[agent]['a_tokens_airdropped_cum'] for agent in initial_stakeholders])
    tokens_incentivised_cum = sum([initial_stakeholders[agent]['a_tokens_incentivised_cum'] for agent in initial_stakeholders])
    lp_tokens = initial_liquidity_pool['lp_tokens']
    

    token_economy = {
        'te_total_supply' : initial_total_supply, # total token supply in existence
        'te_circulating_supply' : (tokens_vested_cum + tokens_airdropped_cum + lp_tokens), # circulating token supply
        'te_unvested_supply': initial_total_supply - (tokens_vested_cum + tokens_airdropped_cum + lp_tokens), # unvested token tupply
        'te_holding_supply' : tokens_holding_cum, # supply of tokens held by agents
        'te_MC' : token_fdv * (tokens_vested_cum + tokens_airdropped_cum + lp_tokens) / initial_total_supply, # market capitalization
        'te_FDV_MC' : token_fdv, # fully diluted market capitalization
        'te_selling_perc': 0, # percentage of tokens sold
        'te_utility_perc': 0, # percentage of tokens used for utility
        'te_holding_perc': 0, # percentage of tokens held
        'te_remove_perc': 0, # percentage of tokens removed
        'te_selling_allocation': 0, # from vesting + airdrops + incentivisation
        'te_utility_allocation': 0, # from vesting + airdrops + incentivisation
        'te_holding_allocation': 0, # from vesting + airdrops + incentivisation
        'te_selling_allocation_cum': 0, # from vesting + airdrops + incentivisation
        'te_utility_allocation_cum': 0, # from vesting + airdrops + incentivisation
        'te_holding_allocation_cum': 0, # from vesting + airdrops + incentivisation
        'te_tokens_vested_cum': 0, # tokens vested cumulatively
        'te_tokens_burned': 0, # tokens burned
        'te_tokens_burned_cum': 0, # tokens burned cumulatively
        'te_tokens_burned_usd': 0, # tokens burned in USD
        'te_minted_tokens' : 0, # tokens minted
        'te_minted_tokens_cum': 0, # tokens minted cumulatively
        'te_minted_tokens_usd': 0, # tokens minted in USD
        'te_incentivised_tokens' : 0, # tokens incentivised
        'te_incentivised_tokens_usd' : 0, # tokens incentivised in USD
        'te_incentivised_tokens_usd_cum' : 0, # tokens incentivised in USD cumulatively
        'te_incentivised_tokens_cum' : 0, # tokens incentivised cumulatively
        'te_airdrop_tokens' : 0, # tokens airdropped
        'te_airdrop_tokens_usd' : 0, # tokens airdropped in USD
        'te_airdrop_tokens_usd_cum' : 0, # tokens airdropped in USD cumulatively
        'te_airdrop_tokens_cum' : 0, # tokens airdropped cumulatively
        'te_staking_apr': 0, # staking APR
        'te_p_r_ratio': 0, # price to revenue ratio
        'te_p_e_ratio': 0, # price to earnings ratio
        'te_product_user_per_incentivised_usd': 0, # product users per incentivised token in USD
        'te_incentivised_usd_per_product_user': 0, # incentivised token in USD per product user
        'te_bribe_rewards_for_stakers_usd': 0, # bribe rewards for stakers in USD
        'te_bribe_rewards_for_stakers_usd_cum': 0, # bribe rewards for stakers in USD cumulatively
    }

    return token_economy

def initialize_user_adoption(sys_param):
    """
    Initialize the user adoption metrics.
    """
    initial_product_users = sys_param['initial_product_users'][0]
    initial_token_holders = sys_param['initial_token_holders'][0]
    launchDate = pd.to_datetime(sys_param['launch_date'][0], format='%d.%m.%Y')
    current_date = get_initial_date(sys_param)

    current_day = (pd.to_datetime(current_date)+pd.DateOffset(months=1) - launchDate).days

    # This is what is shown in the model as a constant as the user adoption numbers refer to 10 years (product_users_after_10y & token_holers_after_10y)
    total_days = 3653

    ## Product user adoption
    initial_product_users = sys_param['initial_product_users'][0]
    product_users_after_10y = sys_param['product_users_after_10y'][0]
    product_adoption_velocity = sys_param['product_adoption_velocity'][0]
    one_time_product_revenue_per_user = sys_param['one_time_product_revenue_per_user'][0]
    regular_product_revenue_per_user = sys_param['regular_product_revenue_per_user'][0]

    # print all calculate_user_adoption inputs
    # product_users = calculate_user_adoption(initial_product_users,product_users_after_10y,product_adoption_velocity,current_day) # use this only for first day at token_launch
    product_users = initial_product_users
    
    ## Product Revenue    
    product_revenue = product_users*(one_time_product_revenue_per_user+regular_product_revenue_per_user)

    ## Token holder adoption
    initial_token_holders = sys_param['initial_token_holders'][0]
    token_holders_after_10y = sys_param['token_holders_after_10y'][0]
    token_adoption_velocity = sys_param['token_adoption_velocity'][0]
    one_time_token_buy_per_user = sys_param['one_time_token_buy_per_user'][0]
    regular_token_buy_per_user = sys_param['regular_token_buy_per_user'][0]

    # token_holders = calculate_user_adoption(initial_token_holders,token_holders_after_10y,token_adoption_velocity,current_day) # use this only for first day at token_launch
    token_holders = initial_token_holders

    ## Calculating Token Buys
    token_buys =(one_time_token_buy_per_user+regular_token_buy_per_user)*token_holders

    user_adoption = {
    'ua_product_users': product_users, # amount of product users
    'ua_token_holders': token_holders, # amount of token holders
    'ua_product_revenue':product_revenue, # product revenue
    'ua_token_buys': token_buys, # amount of effective token buys
    }

    return user_adoption

def initialize_business_assumptions(sys_param, initial_user_adoption):
    """
    Initialize the business assumptions metrics.
    """
    if 'token_launch' in sys_param:
        token_launch = sys_param['token_launch'][0]
    else:
        token_launch = True
    
    if token_launch:
        initial_capital = calculate_raised_capital(sys_param)
    else:
        initial_capital = sys_param['initial_cash_balance'][0]
    

    product_revenue = initial_user_adoption['ua_product_revenue']

    # revenue shares if provided by the UI
    staker_rev_share = sys_param['staker_rev_share'][0] if sys_param['staking_vesting_token_allocation'][0] <= 0 else 0
    if 'business_rev_share' in sys_param:
        business_rev_share = sys_param['business_rev_share'][0]
    else:
        business_rev_share = 100 - staker_rev_share
    if 'service_provider_rev_share' in sys_param:
        service_provider_rev_share = sys_param['service_provider_rev_share'][0]
    else:
        service_provider_rev_share = 0
    if 'incentivisation_rev_share' in sys_param:
        incentivisation_rev_share = sys_param['incentivisation_rev_share'][0]
    else:
        incentivisation_rev_share = 0

    business_assumptions = {
    'ba_cash_balance': initial_capital, ## cash balance of the company
    'ba_cash_flow': product_revenue, ## cash flow of the company
    'ba_buybacks_usd': 0, ## buybacks in USD per month
    'ba_buybacks_cum_usd': 0, ## buybacks in USD cumulatively
    'ba_fix_expenditures_usd': 0, ## fixed expenditures in USD per month
    'ba_fix_expenditures_cum_usd': 0, ## fixed expenditures in USD cumulatively
    'ba_var_expenditures_usd': 0, ## fixed expenditures in USD per month
    'ba_var_expenditures_cum_usd': 0, ## fixed expenditures in USD cumulatively
    'ba_fix_business_revenue_usd': 0, # fixed business revenue
    'ba_fix_business_revenue_cum_usd': 0, # fixed business revenue cumulatively
    'ba_var_business_revenue_usd': product_revenue * (business_rev_share/100), # business revenue
    'ba_var_business_revenue_cum_usd': product_revenue * (business_rev_share/100), # business revenue cumulatively
    'ba_staker_revenue_usd': product_revenue * (staker_rev_share/100), # staker revenue
    'ba_staker_revenue_cum_usd': product_revenue * (staker_rev_share/100), # staker revenue cumulatively
    'ba_service_provider_revenue_usd': product_revenue * (service_provider_rev_share/100), # service provider revenue
    'ba_service_provider_revenue_cum_usd': product_revenue * (service_provider_rev_share/100), # service provider revenue cumulatively
    'ba_incentivisation_revenue_usd': 0, # incentivisation revenue
    'ba_incentivisation_revenue_cum_usd': 0, # incentivisation revenue cumulatively
    'ba_buyback_from_revenue_share_incentivisation_usd': 0, # buyback from revenue share in USD for incentivisations
    'ba_buyback_from_revenue_share_incentives' : 0, # buyback incentives from revenue share in tokens
    'ba_business_buybacks_usd' : 0, # business buybacks in USD
    }

    return business_assumptions


def initialize_utilities(initial_stakeholders, sys_param):
    """
    Initialize the utility meta bucket metrics.
    """

    staked_tokens = sum([initial_stakeholders[agent]['a_tokens_staked_cum'] for agent in initial_stakeholders])
    liquidity_mining_tokens = sum([initial_stakeholders[agent]['a_tokens_liquidity_mining_cum'] for agent in initial_stakeholders])
    
    utilities = {
    'u_staking_allocation':0, # staking allocation per timestep
    'u_staking_allocation_cum':staked_tokens, # staking allocation cumulatively
    'u_staking_remove':0, # staking token removal
    'u_buyback_from_revenue_share_staking_usd': 0, # buyback from revenue share in USD as reward for stakers
    'u_staking_revenue_share_rewards':0, # revenue sharing rewards in tokens
    'u_staking_vesting_rewards':0, # staking vesting rewards in tokens
    'u_staking_minting_rewards':0, # staking minting rewards in tokens
    'u_liquidity_mining_rewards': 0, # liquidity mining rewards in tokens
    'u_liquidity_mining_allocation': 0, # liquidity mining token allocation per timestep
    'u_liquidity_mining_allocation_cum': liquidity_mining_tokens, # liquidity mining token allocation cumulatively
    'u_liquidity_mining_allocation_remove': 0, # liquidity mining token removal
    'u_burning_allocation': 0, # burning token allocation per timestep
    'u_burning_allocation_cum': 0, # burning token allocation cumulatively
    'u_holding_allocation': 0, # holding token allocation per timestep from utility bucket
    'u_holding_allocation_cum': 0, # holding token allocation cumulatively from utility bucket
    'u_holding_rewards':0, # holding token rewards
    'u_transfer_allocation':0, # transfer token allocation per timestep
    'u_transfer_allocation_cum': 0, # transfer token allocation cumulatively
    }

    return utilities


### TEST FUNCTIONS ###
def test_timeseries(data, data_key, data_row_multiplier, QTM_data_tables, QTM_row, relative_tolerance=0.001, timestep_cut_off=0, shift=0):
    # get amount of accounted for timesteps
    n_timesteps = len(QTM_data_tables.iloc[QTM_row-2].values[2:-1]) - [len(QTM_data_tables.iloc[QTM_row-2].values[2:-1])-timestep_cut_off if timestep_cut_off > 0 else 0][0] - shift

    if isinstance(data_key, dict):
        sign = list(data_key.keys())[0]
        data_key1 = data_key[sign][0]
        data_key2 = data_key[sign][1]

    key_string = f"{data_key1} {sign} {data_key2}" if isinstance(data_key, dict) else f"{data_key}"
    
    print(f"Testing {key_string} of radCad timeseries simulation at QTM row "+str(QTM_row)+" ("+QTM_data_tables.iloc[QTM_row-2].values[1]+") for "+str(n_timesteps)+" / "+str(len(QTM_data_tables.iloc[QTM_row-2].values[2:-1]))+" timesteps...")

    for i in range(n_timesteps):
        # get testing values
        QTM_data_table_value = float(QTM_data_tables.iloc[QTM_row-2].values[2:-1][i].replace(",",""))
        if isinstance(data_key, dict):
            radCAD_value1 = float(data[data_key1].values[i+shift]) * data_row_multiplier
            radCAD_value2 = float(data[data_key2].values[i+shift]) * data_row_multiplier
            if sign == '-':
                radCAD_value = radCAD_value1 - radCAD_value2
            elif sign == '+':
                radCAD_value = radCAD_value1 + radCAD_value2
            elif sign == '*':
                radCAD_value = radCAD_value1 * radCAD_value2
            elif sign == '/':
                radCAD_value = radCAD_value1 / radCAD_value2
        else:
            radCAD_value = float(data[data_key].values[i+shift]) * data_row_multiplier

        # assert the values
        error_message = (f"radCad simulation value {key_string} = "+ str(radCAD_value)
                        + " at timestep "+str(i+1)+" is not equal to the QTM data table value "+ str(QTM_data_table_value)+" at row "+str(QTM_row)
                        +" and date "+str(QTM_data_tables.iloc[3].values[2:-1][i])+". The difference is "+str(radCAD_value - QTM_data_table_value)+" or "
                        +str([radCAD_value/QTM_data_table_value * 100 if QTM_data_table_value!= 0 else "NaN"][0])+"%.")

        if QTM_data_table_value == 0:
            if np.abs(radCAD_value) < relative_tolerance:
                pass
        elif radCAD_value == 0:
            if np.abs(QTM_data_table_value) < relative_tolerance:
                pass
        else:
            np.testing.assert_allclose(radCAD_value, QTM_data_table_value, rtol=relative_tolerance, err_msg=error_message)
    if n_timesteps == len(QTM_data_tables.iloc[QTM_row-2].values[2:-1]):
        print(u'\u2713'+" Test passed!")
    else:
        print("("+u'\u2713'+") Test passed for "+str(n_timesteps)+" / "+str(len(QTM_data_tables.iloc[QTM_row-2].values[2:-1]))+" timesteps!")
    print("------------------------------------")

def import_dummy_data(row, timestep):
    # Get the current directory
    current_dir = os.path.dirname(os.path.abspath(__file__))

    # Go two folders up
    parent_dir = os.path.abspath(os.path.join(os.path.abspath(os.path.join(current_dir, os.pardir)), os.pardir))

    QTM_data_tables = pd.read_csv(parent_dir+'/data/Quantitative_Token_Model_V1.88_radCad_integration - Data Tables.csv')

    QTM_row = row
    QTM_data_table_value = float(QTM_data_tables.iloc[QTM_row-2].values[2:-1][timestep].replace(",",""))
    
    return  QTM_data_table_value

def convert_to_json(x):
    try:
        return json.dumps(x)
    except:
        return x

def months_difference(date1, date2):
    year_diff = date2.year - date1.year
    month_diff = date2.month - date1.month
    total_months = year_diff * 12 + month_diff
    return total_months

def calculate_buyback_share_tokens(buyback_share_amount_usd, buyback_all_amount_usd, lp_tokens_after_liquidity_addition, lp_tokens_after_buyback):
    # calculate macro rewards from staking revenue share
    bought_back_tokens = (lp_tokens_after_liquidity_addition - lp_tokens_after_buyback)
    if buyback_all_amount_usd > 0:
        buyback_share_tokens = bought_back_tokens * (buyback_share_amount_usd/buyback_all_amount_usd)
    elif buyback_all_amount_usd == 0:
        buyback_share_tokens = 0
    else:
        raise ValueError(f"Business buybacks in USD terms buyback_all_amount_usd({buyback_all_amount_usd}) must not be negative!")
    return buyback_share_tokens