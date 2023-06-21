# POLICY FUNCTIONS
def generate_agent_behavior(params, substep, state_history, prev_state, **kwargs):
    agent_behavior_dict = {
        'angle': {
            'trade': params['avg_token_selling_allocation']-params['avg_token_utility_removal']/3,
            'hold': params['avg_token_holding_allocation']-params['avg_token_utility_removal']/3,
            'utility': params['avg_token_utility_allocation']-params['avg_token_utility_removal']/3,
            'remove_locked_tokens': params['avg_token_utility_removal'],
        },
        'seed': {
            'trade': params['avg_token_selling_allocation']-params['avg_token_utility_removal']/3,
            'hold': params['avg_token_holding_allocation']-params['avg_token_utility_removal']/3,
            'utility': params['avg_token_utility_allocation']-params['avg_token_utility_removal']/3,
            'remove_locked_tokens': params['avg_token_utility_removal'],
        },
        'presale_1': {
            'trade': params['avg_token_selling_allocation']-params['avg_token_utility_removal']/3,
            'hold': params['avg_token_holding_allocation']-params['avg_token_utility_removal']/3,
            'utility': params['avg_token_utility_allocation']-params['avg_token_utility_removal']/3,
            'remove_locked_tokens': params['avg_token_utility_removal'],
        },
        'presale_2': {
            'trade': params['avg_token_selling_allocation']-params['avg_token_utility_removal']/3,
            'hold': params['avg_token_holding_allocation']-params['avg_token_utility_removal']/3,
            'utility': params['avg_token_utility_allocation']-params['avg_token_utility_removal']/3,
            'remove_locked_tokens': params['avg_token_utility_removal'],
        },
        'public_sale': {
            'trade': params['avg_token_selling_allocation']-params['avg_token_utility_removal']/3,
            'hold': params['avg_token_holding_allocation']-params['avg_token_utility_removal']/3,
            'utility': params['avg_token_utility_allocation']-params['avg_token_utility_removal']/3,
            'remove_locked_tokens': params['avg_token_utility_removal'],
        },
        'team': {
            'trade': params['avg_token_selling_allocation']-params['avg_token_utility_removal']/3,
            'hold': params['avg_token_holding_allocation']-params['avg_token_utility_removal']/3,
            'utility': params['avg_token_utility_allocation']-params['avg_token_utility_removal']/3,
            'remove_locked_tokens': params['avg_token_utility_removal'],
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
        'market_investors': {
            'trade': 60,
            'hold': 10,
            'utility': 25,
            'remove_locked_tokens': 5,
            'incentivise': 0
        }
    }
    return {'agent_behavior_dict': agent_behavior_dict}

# STATE UPDATE FUNCTIONS
def update_agent_behavior(params, substep, state_history, prev_state, policy_input, **kwargs):
    """
    Function to update the agent behaviors
    """
    updated_agents = prev_state['agents']
    agent_behavior_dict = policy_input['agent_behavior_dict']

    for key, value in updated_agents.items():
        updated_agents[key]['action_list'] = list(agent_behavior_dict[updated_agents[key]['type']].keys())
        updated_agents[key]['action_weights'] += tuple(agent_behavior_dict[updated_agents[key]['type']].values())

    return ('agents', updated_agents)

"""
initial_values = {
    "initial_agent_values" : {
        uuid.uuid4(): {
            'type': 'angle',
            'initial_usd_funds': 0,
            'initial_tokens': (sys_param['angle_initial_vesting']/100) * agent_token_allocation["angle_token_allocation"] * sys_param['initial_total_supply'],
            'initial_tokens_vested': (sys_param['angle_initial_vesting']/100) * agent_token_allocation["angle_token_allocation"] * sys_param['initial_total_supply'],
            'initial_tokens_locked': 0,
            'action_list': list(agent_behavior_dict['angle'].keys()),
            'action_weights': tuple(agent_behavior_dict['angle'].values()),
            'current_action': 'hold'
        },
        uuid.uuid4(): {
            'type': 'seed',
            'initial_usd_funds': 0,
            'initial_tokens': (sys_param['seed_initial_vesting']/100) * agent_token_allocation["seed_token_allocation"] * sys_param['initial_total_supply'],
            'initial_tokens_vested': (sys_param['seed_initial_vesting']/100) * agent_token_allocation["seed_token_allocation"] * sys_param['initial_total_supply'],
            'initial_tokens_locked': 0,
            'action_list': list(agent_behavior_dict['seed'].keys()),
            'action_weights': tuple(agent_behavior_dict['seed'].values()),
            'current_action': 'hold'
        },
        uuid.uuid4(): {
            'type': 'presale_1',
            'initial_usd_funds': 0,
            'initial_tokens': (sys_param['presale_1_initial_vesting']/100) * agent_token_allocation["presale_1_token_allocation"] * sys_param['initial_total_supply'],
            'initial_tokens_vested': (sys_param['presale_1_initial_vesting']/100) * agent_token_allocation["presale_1_token_allocation"] * sys_param['initial_total_supply'],
            'initial_tokens_locked': 0,
            'action_list': list(agent_behavior_dict['presale_1'].keys()),
            'action_weights': tuple(agent_behavior_dict['presale_1'].values()),
            'current_action': 'hold'
        },
        uuid.uuid4(): {
            'type': 'presale_2',
            'initial_usd_funds': 0,
            'initial_tokens': (sys_param['presale_2_initial_vesting']/100) * agent_token_allocation["presale_2_token_allocation"] * sys_param['initial_total_supply'],
            'initial_tokens_vested': (sys_param['presale_2_initial_vesting']/100) * agent_token_allocation["presale_2_token_allocation"] * sys_param['initial_total_supply'],
            'initial_tokens_locked': 0,
            'action_list': list(agent_behavior_dict['presale_2'].keys()),
            'action_weights': tuple(agent_behavior_dict['presale_2'].values()),
            'current_action': 'hold'
        },
        uuid.uuid4(): {
            'type': 'public_sale',
            'initial_usd_funds': 0,
            'initial_tokens': (sys_param['public_sale_initial_vesting']/100) * agent_token_allocation["public_sale_token_allocation"] * sys_param['initial_total_supply'],
            'initial_tokens_vested': (sys_param['public_sale_initial_vesting']/100) * agent_token_allocation["public_sale_token_allocation"] * sys_param['initial_total_supply'],
            'initial_tokens_locked': 0,
            'action_list': list(agent_behavior_dict['public_sale'].keys()),
            'action_weights': tuple(agent_behavior_dict['public_sale'].values()),
            'current_action': 'hold'
        },
        uuid.uuid4(): {
            'type': 'team',
            'initial_usd_funds': 0,
            'initial_tokens': (sys_param['team_initial_vesting']/100) * agent_token_allocation["team_token_allocation"] * sys_param['initial_total_supply'],
            'initial_tokens_vested': (sys_param['team_initial_vesting']/100) * agent_token_allocation["team_token_allocation"] * sys_param['initial_total_supply'],
            'initial_tokens_locked': 0,
            'action_list': list(agent_behavior_dict['team'].keys()),
            'action_weights': tuple(agent_behavior_dict['team'].values()),
            'current_action': 'hold'
        },
        uuid.uuid4(): {
            'type': 'reserve',
            'initial_usd_funds': calculate_raised_capital(sys_param),
            'initial_tokens': (sys_param['reserve_initial_vesting']/100) * agent_token_allocation["reserve_token_allocation"] * sys_param['initial_total_supply'],
            'initial_tokens_vested': (sys_param['reserve_initial_vesting']/100) * agent_token_allocation["reserve_token_allocation"] * sys_param['initial_total_supply'],
            'initial_tokens_locked': 0,
            'action_list': list(agent_behavior_dict['reserve'].keys()),
            'action_weights': tuple(agent_behavior_dict['reserve'].values()),
            'current_action': 'hold'
        },
        uuid.uuid4(): {
            'type': 'community',
            'initial_usd_funds': 0,
            'initial_tokens': (sys_param['community_initial_vesting']/100) * agent_token_allocation["community_token_allocation"] * sys_param['initial_total_supply'],
            'initial_tokens_vested': (sys_param['community_initial_vesting']/100) * agent_token_allocation["community_token_allocation"] * sys_param['initial_total_supply'],
            'initial_tokens_locked': 0,
            'action_list': list(agent_behavior_dict['community'].keys()),
            'action_weights': tuple(agent_behavior_dict['community'].values()),
            'current_action': 'hold'
        },
        uuid.uuid4(): {
            'type': 'foundation',
            'initial_usd_funds': 0,
            'initial_tokens': (sys_param['foundation_initial_vesting']/100) * agent_token_allocation["foundation_token_allocation"] * sys_param['initial_total_supply'],
            'initial_tokens_vested': (sys_param['foundation_initial_vesting']/100) * agent_token_allocation["foundation_token_allocation"] * sys_param['initial_total_supply'],
            'initial_tokens_locked': 0,
            'action_list': list(agent_behavior_dict['foundation'].keys()),
            'action_weights': tuple(agent_behavior_dict['foundation'].values()),
            'current_action': 'hold'
        },
        uuid.uuid4(): {
            'type': 'placeholder_1',
            'initial_usd_funds': 0,
            'initial_tokens': (sys_param['placeholder_1_initial_vesting']/100) * agent_token_allocation["placeholder_1_token_allocation"] * sys_param['initial_total_supply'],
            'initial_tokens_vested': (sys_param['placeholder_1_initial_vesting']/100) * agent_token_allocation["placeholder_1_token_allocation"] * sys_param['initial_total_supply'],
            'initial_tokens_locked': 0,
            'action_list': list(agent_behavior_dict['placeholder_1'].keys()),
            'action_weights': tuple(agent_behavior_dict['placeholder_1'].values()),
            'current_action': 'hold'
        },
        uuid.uuid4(): {
            'type': 'placeholder_2',
            'initial_usd_funds': 0,
            'initial_tokens': (sys_param['placeholder_2_initial_vesting']/100) * agent_token_allocation["placeholder_2_token_allocation"] * sys_param['initial_total_supply'],
            'initial_tokens_vested': (sys_param['placeholder_2_initial_vesting']/100) * agent_token_allocation["placeholder_2_token_allocation"] * sys_param['initial_total_supply'],
            'initial_tokens_locked': 0,
            'action_list': list(agent_behavior_dict['placeholder_2'].keys()),
            'action_weights': tuple(agent_behavior_dict['placeholder_2'].values()),
            'current_action': 'hold'
        },
        uuid.uuid4(): {
            'type': 'market_investors',
            'initial_usd_funds': 0,
            'initial_tokens': 0,
            'initial_tokens_vested': 0,
            'initial_tokens_locked': 0,
            'action_list': list(agent_behavior_dict['market_investors_token_allocation'].keys()),
            'action_weights': tuple(agent_behavior_dict['market_investors_token_allocation'].values()),
            'current_action': 'hold'
        }
    },
}
"""