import uuid
from parts.utils import *
import pandas as pd
import sys
sys.path.append('../')
from data.not_iterable_variables import *


QTM_inputs = pd.read_csv('../data/Quantitative_Token_Model_V1.87 - cadCAD_inputs.csv')

# System parameters
sys_param = compose_initial_parameters(QTM_inputs, parameter_list)

# initial values
foundation_agent = new_agent('foundation', initial_foundation_usd_funds, initial_foundation_tokens, ['trade', 'hold', 'lock', 'remove_locked_tokens', 'incentivise'], (0,50,0,0,50))
early_investor_agent = new_agent('early_investor', initial_early_investor_usd_funds, initial_early_investor_tokens, ['trade', 'hold', 'lock', 'remove_locked_tokens'], (60,20,6,14))
market_investor_agent = new_agent('market_investor', initial_market_investor_usd_funds, initial_market_investor_tokens, ['trade', 'hold', 'lock', 'remove_locked_tokens'], (60,15,16,9))

agent_behavior_dict = {
    'angle': {
        'trade': sys_param['avg_token_selling_allocation']-sys_param['avg_token_utility_removal']/3,
        'hold': sys_param['avg_token_holding_allocation']-sys_param['avg_token_utility_removal']/3,
        'utility': sys_param['avg_token_utility_allocation']-sys_param['avg_token_utility_removal']/3,
        'remove_locked_tokens': sys_param['avg_token_utility_removal'],
    },
    'seed': {
        'trade': sys_param['avg_token_selling_allocation']-sys_param['avg_token_utility_removal']/3,
        'hold': sys_param['avg_token_holding_allocation']-sys_param['avg_token_utility_removal']/3,
        'utility': sys_param['avg_token_utility_allocation']-sys_param['avg_token_utility_removal']/3,
        'remove_locked_tokens': sys_param['avg_token_utility_removal'],
    },
    'presale_1': {
        'trade': sys_param['avg_token_selling_allocation']-sys_param['avg_token_utility_removal']/3,
        'hold': sys_param['avg_token_holding_allocation']-sys_param['avg_token_utility_removal']/3,
        'utility': sys_param['avg_token_utility_allocation']-sys_param['avg_token_utility_removal']/3,
        'remove_locked_tokens': sys_param['avg_token_utility_removal'],
    },
    'presale_2': {
        'trade': sys_param['avg_token_selling_allocation']-sys_param['avg_token_utility_removal']/3,
        'hold': sys_param['avg_token_holding_allocation']-sys_param['avg_token_utility_removal']/3,
        'utility': sys_param['avg_token_utility_allocation']-sys_param['avg_token_utility_removal']/3,
        'remove_locked_tokens': sys_param['avg_token_utility_removal'],
    },
    'public_sale': {
        'trade': sys_param['avg_token_selling_allocation']-sys_param['avg_token_utility_removal']/3,
        'hold': sys_param['avg_token_holding_allocation']-sys_param['avg_token_utility_removal']/3,
        'utility': sys_param['avg_token_utility_allocation']-sys_param['avg_token_utility_removal']/3,
        'remove_locked_tokens': sys_param['avg_token_utility_removal'],
    },
    'team': {
        'trade': sys_param['avg_token_selling_allocation']-sys_param['avg_token_utility_removal']/3,
        'hold': sys_param['avg_token_holding_allocation']-sys_param['avg_token_utility_removal']/3,
        'utility': sys_param['avg_token_utility_allocation']-sys_param['avg_token_utility_removal']/3,
        'remove_locked_tokens': sys_param['avg_token_utility_removal'],
    },
    'reserve': {
        'trade': 0,
        'hold': 50,
        'utility': 0,
        'remove_locked_tokens': 0,
        'incentivise': 50
    },
    'community': {
        'trade': 0,
        'hold': 100,
        'utility': 0,
        'remove_locked_tokens': 0,
        'incentivise': 0
    },
    'foundation': {
        'trade': 0,
        'hold': 100,
        'utility': 0,
        'remove_locked_tokens': 0,
        'incentivise': 0
    },
    'placeholder_1': {
        'trade': 0,
        'hold': 100,
        'utility': 0,
        'remove_locked_tokens': 0,
        'incentivise': 0
    },
    'placeholder_1': {
        'trade': 0,
        'hold': 100,
        'utility': 0,
        'remove_locked_tokens': 0,
        'incentivise': 0
    },
}

initial_values = {
    "initial_agent_values" : {
        uuid.uuid4(): {
            'type': 'team',
            'initial_usd_funds': 0,
            'initial_tokens': 0,
            'initial_tokens_vested': 0,
            'initial_tokens_locked': 0,
            'action_list': list(agent_behavior_dict['team'].keys()),
            'action_weights': tuple(agent_behavior_dict['team'].values()),
            'current_action': 'hold'
        },
        uuid.uuid4(): {
            'type': 'reserve',
            'initial_usd_funds': calculate_raised_capital(sys_param),
            'initial_tokens': (sys_param['reserve_initial_vesting']/100) * (sys_param['reserve_allocation']/100) * sys_param['initial_total_supply'],
            'initial_tokens_vested': (sys_param['reserve_initial_vesting']/100) * (sys_param['reserve_allocation']/100) * sys_param['initial_total_supply'],
            'initial_tokens_locked': 0,
            'action_list': list(agent_behavior_dict['reserve'].keys()),
            'action_weights': tuple(agent_behavior_dict['reserve'].values()),
            'current_action': 'hold'
        },
        uuid.uuid4(): {
            'type': 'foundation',
            'initial_usd_funds': 0,
            'initial_tokens': 0,
            'initial_tokens_vested': 0,
            'initial_tokens_locked': 0,
            'action_list': ['trade', 'hold', 'lock', 'remove_locked_tokens', 'incentivise'],
            'action_weights': (0,100,0,0,0),
            'current_action': 'hold'
        },
        uuid.uuid4(): {
            'type': 'team',
            'initial_usd_funds': 0,
            'initial_tokens': 0,
            'initial_tokens_vested': 0,
            'initial_tokens_locked': 0,
            'action_list': ['trade', 'hold', 'lock', 'remove_locked_tokens'],
            'action_weights': (0,0,100,0),
            'current_action': 'hold'
        },
        uuid.uuid4(): {
            'type': 'team',
            'initial_usd_funds': 0,
            'initial_tokens': 0,
            'initial_tokens_vested': 0,
            'initial_tokens_locked': 0,
            'action_list': ['trade', 'hold', 'lock', 'remove_locked_tokens'],
            'action_weights': (0,0,100,0),
            'current_action': 'hold'
        },
    },
}