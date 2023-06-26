# POLICY FUNCTIONS
def generate_agent_behavior(params, substep, state_history, prev_state, **kwargs):
    """
    Define the agent behavior for each agent type
    """

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
        'placeholder_2': {
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
