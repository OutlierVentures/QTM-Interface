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
            'type': 'angle',
            'initial_usd_funds': 10000000,
            'initial_tokens': (sys_param['angle_initial_vesting']/100) * (sys_param['angle_allocation']/100) * sys_param['initial_total_supply'],
            'initial_tokens_vested': (sys_param['angle_initial_vesting']/100) * (sys_param['angle_allocation']/100) * sys_param['initial_total_supply'],
            'initial_tokens_locked': 0,
            'action_list': list(agent_behavior_dict['angle'].keys()),
            'action_weights': tuple(agent_behavior_dict['angle'].values()),
            'current_action': 'hold'
        },
        uuid.uuid4(): {
            'type': 'seed',
            'initial_usd_funds': 10000000,
            'initial_tokens': (sys_param['seed_initial_vesting']/100) * (sys_param['seed_allocation']/100) * sys_param['initial_total_supply'],
            'initial_tokens_vested': (sys_param['seed_initial_vesting']/100) * (sys_param['seed_allocation']/100) * sys_param['initial_total_supply'],
            'initial_tokens_locked': 0,
            'action_list': list(agent_behavior_dict['seed'].keys()),
            'action_weights': tuple(agent_behavior_dict['seed'].values()),
            'current_action': 'hold'
        },
        uuid.uuid4(): {
            'type': 'presale_1',
            'initial_usd_funds': 10000000,
            'initial_tokens': (sys_param['presale_1_initial_vesting']/100) * (sys_param['presale_1_allocation']/100) * sys_param['initial_total_supply'],
            'initial_tokens_vested': (sys_param['presale_1_initial_vesting']/100) * (sys_param['presale_1_allocation']/100) * sys_param['initial_total_supply'],
            'initial_tokens_locked': 0,
            'action_list': list(agent_behavior_dict['presale_1'].keys()),
            'action_weights': tuple(agent_behavior_dict['presale_1'].values()),
            'current_action': 'hold'
        },
        uuid.uuid4(): {
            'type': 'presale_2',
            'initial_usd_funds': 10000000,
            'initial_tokens': (sys_param['presale_2_initial_vesting']/100) * (sys_param['presale_2_allocation']/100) * sys_param['initial_total_supply'],
            'initial_tokens_vested': (sys_param['presale_2_initial_vesting']/100) * (sys_param['presale_2_allocation']/100) * sys_param['initial_total_supply'],
            'initial_tokens_locked': 0,
            'action_list': list(agent_behavior_dict['presale_2'].keys()),
            'action_weights': tuple(agent_behavior_dict['presale_2'].values()),
            'current_action': 'hold'
        },
        uuid.uuid4(): {
            'type': 'public_sale',
            'initial_usd_funds': 10000000,
            'initial_tokens': (sys_param['public_sale_initial_vesting']/100) * (sys_param['public_sale_allocation']/100) * sys_param['initial_total_supply'],
            'initial_tokens_vested': (sys_param['public_sale_initial_vesting']/100) * (sys_param['public_sale_allocation']/100) * sys_param['initial_total_supply'],
            'initial_tokens_locked': 0,
            'action_list': list(agent_behavior_dict['public_sale'].keys()),
            'action_weights': tuple(agent_behavior_dict['public_sale'].values()),
            'current_action': 'hold'
        },
        uuid.uuid4(): {
            'type': 'team',
            'initial_usd_funds': 0,
            'initial_tokens': (sys_param['team_initial_vesting']/100) * (sys_param['team_allocation']/100) * sys_param['initial_total_supply'],
            'initial_tokens_vested': (sys_param['team_initial_vesting']/100) * (sys_param['team_allocation']/100) * sys_param['initial_total_supply'],
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
            'type': 'community',
            'initial_usd_funds': 0,
            'initial_tokens': (sys_param['community_initial_vesting']/100) * (sys_param['community_allocation']/100) * sys_param['initial_total_supply'],
            'initial_tokens_vested': (sys_param['community_initial_vesting']/100) * (sys_param['community_allocation']/100) * sys_param['initial_total_supply'],
            'initial_tokens_locked': 0,
            'action_list': list(agent_behavior_dict['community'].keys()),
            'action_weights': tuple(agent_behavior_dict['community'].values()),
            'current_action': 'hold'
        },
        uuid.uuid4(): {
            'type': 'foundation',
            'initial_usd_funds': 0,
            'initial_tokens': (sys_param['foundation_initial_vesting']/100) * (sys_param['foundation_allocation']/100) * sys_param['initial_total_supply'],
            'initial_tokens_vested': (sys_param['foundation_initial_vesting']/100) * (sys_param['foundation_allocation']/100) * sys_param['initial_total_supply'],
            'initial_tokens_locked': 0,
            'action_list': list(agent_behavior_dict['foundation'].keys()),
            'action_weights': tuple(agent_behavior_dict['foundation'].values()),
            'current_action': 'hold'
        },
        uuid.uuid4(): {
            'type': 'placeholder_1',
            'initial_usd_funds': 0,
            'initial_tokens': (sys_param['placeholder_1_initial_vesting']/100) * (sys_param['placeholder_1_allocation']/100) * sys_param['initial_total_supply'],
            'initial_tokens_vested': (sys_param['placeholder_1_initial_vesting']/100) * (sys_param['placeholder_1_allocation']/100) * sys_param['initial_total_supply'],
            'initial_tokens_locked': 0,
            'action_list': list(agent_behavior_dict['placeholder_1'].keys()),
            'action_weights': tuple(agent_behavior_dict['placeholder_1'].values()),
            'current_action': 'hold'
        },
        uuid.uuid4(): {
            'type': 'placeholder_2',
            'initial_usd_funds': 0,
            'initial_tokens': (sys_param['placeholder_2_initial_vesting']/100) * (sys_param['placeholder_2_allocation']/100) * sys_param['initial_total_supply'],
            'initial_tokens_vested': (sys_param['placeholder_2_initial_vesting']/100) * (sys_param['placeholder_2_allocation']/100) * sys_param['initial_total_supply'],
            'initial_tokens_locked': 0,
            'action_list': list(agent_behavior_dict['placeholder_2'].keys()),
            'action_weights': tuple(agent_behavior_dict['placeholder_2'].values()),
            'current_action': 'hold'
        }
    },
}