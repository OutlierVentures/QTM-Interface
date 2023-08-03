# POLICY FUNCTIONS
def generate_agent_meta_bucket_behavior(params, substep, state_history, prev_state, **kwargs):
    """
    Define the agent behavior for each agent type
    """
    if params['agent_behavior'] == 'stochastic':
        """
        Define the agent behavior for each agent type for the stochastic agent behavior
        Agent actions are based on a weighted random choices.
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
            'incentivisation': {
                'trade': 0,
                'hold': 100,
                'utility': 0,
                'remove_locked_tokens': 0,
                'incentivise': 0
            },
            'placeholder': {
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
            },
            'airdrop_receivers': {
                'trade': 60,
                'hold': 10,
                'utility': 25,
                'remove_locked_tokens': 5,
                'incentivise': 0
            },
            'incentivisation_receivers': {
                'trade': 60,
                'hold': 10,
                'utility': 25,
                'remove_locked_tokens': 5,
                'incentivise': 0
            }
        }
    
    elif params['agent_behavior'] == 'static':
        """
        Define the agent behavior for each agent type for the static 1:1 QTM behavior
        ToDo: Consistency checks of correct meta bucket and utility share amounts, which should be 100% in total for each agent type
        """
        agents = prev_state['agents'].copy()
        
        # initialize agent behavior dictionary
        agent_behavior_dict = {}

        # populate agent behavior dictionary
        for agent in agents:
            agent_behavior_dict[agent] = {
                'sell': params['avg_token_selling_allocation'],
                'hold': params['avg_token_holding_allocation'],
                'utility': params['avg_token_utility_allocation']
            }

    return {'agent_behavior_dict': agent_behavior_dict}

def agent_meta_bucket_allocations(params, substep, state_history, prev_state, **kwargs):
    """
    Define the meta bucket token allocations of all agents with respect to 'sell' 'hold' and 'utility'
    """

    # get state variables
    agents = prev_state['agents']

    # initialize meta bucket token allocations
    meta_bucket_allocations= {
        'selling': 0,
        'holding': 0,
        'utility': 0
    }

    # update agent token allocations and update the meta bucket allocations w.r.t. each agents contribution
    # note that protocol buckets are not used for meta bucket allocations
    agent_allocations = {}
    for agent in agents:
        if agents[agent]['type'] == 'market_investor' or agents[agent]['type'] == 'early_investor' or agents[agent]['type'] == 'team':
            # get agent static behavior percentages
            selling_perc = agents[agent]['actions']['sell']
            utility_perc = agents[agent]['actions']['utility']
            hold_perc = agents[agent]['actions']['hold']

            # calculate corresponding absolute token amounts for meta buckets
            # agent meta bucket allocations are based on the agents vested tokens
            sell_tokens = agents[agent]['tokens_vested'] * selling_perc
            utility_tokens = agents[agent]['tokens_vested'] * utility_perc
            holding_tokens = agents[agent]['tokens_vested'] * hold_perc

            # populate meta bucket allocations
            meta_bucket_allocations['selling'] += sell_tokens
            meta_bucket_allocations['holding'] += holding_tokens
            meta_bucket_allocations['utility'] += utility_tokens

        else:
            # calculate corresponding absolute token amounts for meta buckets
            sell_tokens = 0
            utility_tokens = 0
            holding_tokens = 0
        
        # update agent token allocations
        agent_allocations[agent] = {
            'selling': sell_tokens,
            'holding': holding_tokens,
            'utility': utility_tokens,
        }

    return {'meta_bucket_allocations': meta_bucket_allocations, 'agent_allocations': agent_allocations}



# STATE UPDATE FUNCTIONS
def update_agent_meta_bucket_behavior(params, substep, state_history, prev_state, policy_input, **kwargs):
    """
    Function to update the agent behaviors
    """
    updated_agents = prev_state['agents']
    agent_behavior_dict = policy_input['agent_behavior_dict']

    for key in updated_agents:
        updated_agents[key]['actions'] = agent_behavior_dict[key]

    return ('agents', updated_agents)

def update_agent_meta_bucket_allocations(params, substep, state_history, prev_state, policy_input, **kwargs):
    """
    Function to update the agent meta bucket token allocations
    """
    
    # get state variables
    updated_agents = prev_state['agents'].copy()
    
    # get policy inputs
    agent_allocations = policy_input['agent_allocations']

    for key, value in updated_agents.items():
        # update agent token allocations
        updated_agents[key]['selling_tokens'] = agent_allocations[key]['selling']
        updated_agents[key]['utility_tokens'] = agent_allocations[key]['utility']
        updated_agents[key]['holding_tokens'] = agent_allocations[key]['holding']

    return ('agents', updated_agents)


def update_token_economy_meta_bucket_allocations(params, substep, state_history, prev_state, policy_input, **kwargs):
    """
    Function to update the meta bucket allocations for the token economy
    """

    # get state variables
    updated_token_economy = prev_state['token_economy'].copy()

    # get policy inputs
    updated_meta_bucket_allocations = policy_input['meta_bucket_allocations']

    updated_token_economy['selling_allocation'] = updated_meta_bucket_allocations['selling']
    updated_token_economy['utility_allocation'] = updated_meta_bucket_allocations['utility']
    updated_token_economy['holding_allocation'] = updated_meta_bucket_allocations['holding']

    return ('token_economy', updated_token_economy)
