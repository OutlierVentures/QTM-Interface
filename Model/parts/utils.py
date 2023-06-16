import numpy as np
import math
import uuid
import random
from typing import *

# Helper Functions
def calculate_raised_capital(sys_param):
    """
    Calculate the overall raised capital from the initial investors
    """
    raised_capital = 0
    for key, value in sys_param:
        if "_raised" in key:
            raised_capital += value

    return raised_capital

# Initialization
def new_agent(stakeholder_type: str, usd_funds: int,
              tokens: int, action_list: list, action_weights: Tuple) -> dict:
    agent = {'type': stakeholder_type,
             'usd_funds': usd_funds,
             'tokens': tokens,
             'tokens_vested': 0,
             'tokens_locked': 0,
             'action_list': action_list,
             'action_weights': action_weights,
             'current_action': 'hold'}
    return agent


def generate_agent(agents_dict):
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

# chatGPT solution
def create_parameter_list(parameter_name, not_iterable_parameters, init_value, min, max, intervals):
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
    initial_parameters = {}
    for index, row in QTM_inputs.iterrows():
        parameter_name = row['Parameter Name'].lower().replace(' ', '_').replace('/', '').replace('(', '').replace(')', '')
        initial_parameters[parameter_name] = create_parameter_list(parameter_name, not_iterable_parameters, row['Initial Value'], row['Min'], row['Max'], row['Interval Steps'])
    return initial_parameters


def initial_investor_allocation(initial_stakeholder_values, token_economy):
    initial_token_supply = token_economy['initial_token_supply']
    external_equity = token_economy['external_equity']

    initial_stakeholder_values = fund_raising(initial_stakeholder_values,initial_token_supply,external_equity)

    for i, investor in initial_stakeholder_values.items():

        if investor['percentage_allocation'] == 0 and investor['effective_token_price'] != 0:
            investor['percentage_allocation'] = (investor['capital_raise']/investor['effective_token_price'])/initial_token_supply
        #Need to figure this out


        percentage_allocation = investor['percentage_allocation']
    
        total_token_amount = percentage_allocation * initial_token_supply
        initial_vesting = investor['initial_vesting']
        investor['current_allocation'] = initial_vesting * total_token_amount


    initial_stakeholder_values = create_liquidity_pool(initial_stakeholder_values,initial_token_supply)

    token_economy['current_circulating_supply'] = sum([investor['current_allocation'] for i, investor in initial_stakeholder_values.items()])

    token_economy['sum_of_raised_capital'] = sum([investor['capital_raise'] for i, investor in initial_stakeholder_values.items()])

    return initial_stakeholder_values, token_economy







def fund_raising(initial_stakeholder_values,initial_token_supply,external_equity):


    #need a public sale investor to be intiialized no matter what
    initial_stakeholder_values['Public Sale']['effective_token_price'] =  initial_stakeholder_values['Public Sale']['valuation_cap']/initial_token_supply
    initial_stakeholder_values['Public Sale']['token_discount_perc'] = 0
    public_token_price = initial_stakeholder_values['Public Sale']['effective_token_price']



    #Go through the rest of the investors that are not public sale
    for i, investor in initial_stakeholder_values.items():
        

        #Check if its an investor with a fundraise
        investor_type = investor['type']
        investor_subtype = investor['subtype']


        if investor_type == "Investor" and investor_subtype != "Public Sale":


            #deal with angels

            if investor['subtype'] == "Angel":
                investor['percentage_allocation'] = external_equity*(initial_stakeholder_values['Founders']['percentage_allocation']/(1-external_equity))
                percentage_allocation = investor['percentage_allocation']
                                
                investor['valuation_cap'] = (investor['capital_raise'] / (percentage_allocation*initial_token_supply)) * initial_token_supply
                valuation_cap = investor['valuation_cap']
                
                investor['bonus_amount'] = investor['valuation_cap']/initial_token_supply

                investor['effective_token_price'] = min(public_token_price / investor['bonus_amount'], investor['valuation_cap'] / initial_token_supply)
            else:
                valuation_cap = investor['valuation_cap']
                bonus_amount = investor['bonus_amount']
                #Change other variables
                if bonus_amount !=0:
                    investor['effective_token_price'] = min(public_token_price / bonus_amount, valuation_cap / initial_token_supply)
                else:
                    investor['effective_token_price'] = valuation_cap / initial_token_supply
                
                
            investor['token_discount_perc'] = investor['effective_token_price']/public_token_price



    return initial_stakeholder_values



def create_liquidity_pool(initial_stakeholder_values,initial_token_supply):
    percentage_allocation = 0
    percentage_allocation = 1-sum([investor['percentage_allocation'] for i, investor in initial_stakeholder_values.items()])
    


    initial_stakeholder_values['Liquidity Pool']['percentage_allocation'] = percentage_allocation
    total_token_amount = percentage_allocation * initial_token_supply
    
    initial_vesting = initial_stakeholder_values['Liquidity Pool']['initial_vesting']
    initial_stakeholder_values['Liquidity Pool']['current_allocation']= initial_vesting * total_token_amount
    initial_stakeholder_values['Liquidity Pool']['total_token_amount']= total_token_amount

    return initial_stakeholder_values



def liquidity_pool_module(initial_stakeholder_values,token_economy,liquidity_pool):


    public_sale_valuation = token_economy['public_sale_valuation']
    initial_token_supply = token_economy['initial_token_supply']
    sum_of_raised_capital = token_economy['sum_of_raised_capital']
    current_circulating_supply = token_economy['current_circulating_supply']
    lp_paring_token_price = liquidity_pool['lp_paring_token_price']
    token_lp_weighting = liquidity_pool['token_lp_weighting']




    token_launch_price = public_sale_valuation / initial_token_supply

    liquidity_pool_fund_allocation = token_launch_price*initial_stakeholder_values['Liquidity Pool']['total_token_amount']*100

    allocation_by_raised_amount = liquidity_pool_fund_allocation/sum_of_raised_capital

    initial_token_MC_price = token_launch_price*current_circulating_supply

    initial_token_FDV_price = initial_token_supply*token_launch_price

    initial_pairing_amount = liquidity_pool_fund_allocation/lp_paring_token_price

    token_pair_weighting = 1-token_lp_weighting


    liquidity_pool_module_data = {
        'token_launch_price': token_launch_price,
        'liquidity_pool_fund_allocation': liquidity_pool_fund_allocation,
        'allocation_by_raised_amount': allocation_by_raised_amount,
        'initial_token_MC_price': initial_token_MC_price,
        'initial_token_FDV_price': initial_token_FDV_price,
        'initial_pairing_amount': initial_pairing_amount,
        'token_pair_weighting': token_pair_weighting
    }



    return liquidity_pool_module_data