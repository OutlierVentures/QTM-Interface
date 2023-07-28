# POLICY FUNCTIONS
def generate_agent_behavior(params, substep, state_history, prev_state, **kwargs):
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
            agent_behavior_dict[agents[agent]['name']] = {
                'trade': params['avg_token_selling_allocation'],
                'hold': params['avg_token_holding_allocation'],
                'utility': params['avg_token_utility_allocation'],
                'remove_locked_tokens': params['avg_token_utility_removal'],
                'locking_apr': params['lock_share'],
                'locking_buyback': params['lock_buyback_distribute_share'],
                'liquidity': params['liquidity_mining_share'],
                'transfer': params['transfer_share'],
                'burning': params['burning_share']
            }

    return {'agent_behavior_dict': agent_behavior_dict}

def agent_token_allocations(params, substep, state_history, prev_state, **kwargs):
    """
    Define the meta bucket token allocations of all agents with respect to 'sell' 'hold' and 'utility'
    """

    # get state variables
    agents = prev_state['agents']

    # initialize meta bucket token allocations
    meta_bucket_allocations= {
        'selling': 0,
        'holding': 0,
        'utility': 0,
        'removed': 0
    }

    utility_bucket_allocations = {
        'locking_apr': 0,
        'locking_buyback': 0,
        'liquidity': 0,
        'transfer': 0,
        'burn': 0
    }

    # update agent token allocations and update the meta bucket allocations w.r.t. each agents contribution
    # note that protocol buckets are not used for meta bucket allocations
    agent_allocations = {}
    for agent in agents:
        if agents[agent]['type'] != 'protocol_bucket':
            # get agent static behavior indices for behavior list
            behavior_lst_sell_index = agents[agent]['action_list'].index('trade')
            behavior_lst_utility_index = agents[agent]['action_list'].index('utility')
            behavior_lst_hold_index = agents[agent]['action_list'].index('hold')

            # get agent static behavior percentages
            selling_perc = agents[agent]['action_weights'][behavior_lst_sell_index]
            utility_perc = agents[agent]['action_weights'][behavior_lst_utility_index]
            hold_perc = agents[agent]['action_weights'][behavior_lst_hold_index]

            # calculate corresponding absolute token amounts for meta buckets
            # agent meta bucket allocations are based on the agents vested tokens
            sell_tokens = agents[agent]['tokens_vested'] * selling_perc/100
            utility_tokens = agents[agent]['tokens_vested'] * utility_perc/100
            holding_tokens = agents[agent]['tokens_vested'] * hold_perc/100

            # populate meta bucket allocations
            meta_bucket_allocations['selling'] += sell_tokens
            meta_bucket_allocations['holding'] += holding_tokens
            meta_bucket_allocations['utility'] += utility_tokens
            meta_bucket_allocations['removed'] += removed_tokens

            # populate utility bucket allocations
            utility_bucket_allocations['locking_apr'] += locked_apr_tokens
            utility_bucket_allocations['locking_buyback'] += locked_buyback_tokens
            utility_bucket_allocations['liquidity'] += liquidity_tokens
            utility_bucket_allocations['transfer'] += transfer_tokens
            utility_bucket_allocations['burn'] += burn_tokens

        else:
            # calculate corresponding absolute token amounts for meta buckets
            sell_tokens = 0
            utility_tokens = 0
            removed_tokens = 0
            locked_apr_tokens = 0
            locked_buyback_tokens = 0
            liquidity_tokens = 0
            transfer_tokens = 0
            burn_tokens = 0
        
        # update agent token allocations
        agent_allocations[agent] = {
            'selling': sell_tokens,
            'holding': holding_tokens,
            'utility': utility_tokens,
            'removed': removed_tokens,
            'locking_apr': locked_apr_tokens,
            'locking_buyback': locked_buyback_tokens,
            'liquidity': liquidity_tokens,
            'transfer': transfer_tokens,
            'burn': burn_tokens
        }

    return {'meta_bucket_allocations': meta_bucket_allocations, 'utility_bucket_allocations': utility_bucket_allocations, 'agent_allocations': agent_allocations}


# STATE UPDATE FUNCTIONS
def update_agent_behavior(params, substep, state_history, prev_state, policy_input, **kwargs):
    """
    Function to update the agent behaviors
    """
    updated_agents = prev_state['agents']
    agent_behavior_dict = policy_input['agent_behavior_dict']

    for key, value in updated_agents.items():
        updated_agents[key]['action_list'] = list(agent_behavior_dict[updated_agents[key]['name']].keys())
        updated_agents[key]['action_weights'] += tuple(agent_behavior_dict[updated_agents[key]['name']].values())

    return ('agents', updated_agents)

def update_agent_token_allocations(params, substep, state_history, prev_state, policy_input, **kwargs):
    """
    Function to update the agent token allocations
    """
    updated_agents = prev_state['agents'].copy()
    agent_allocations = policy_input['agent_allocations']

    for key, value in updated_agents.items():
        # check if agent has enough tokens for meta bucket allocations

        if updated_agents[key]['tokens'] - agent_allocations[key]['selling'] - agent_allocations[key]['utility'] + agent_allocations[key]['removed'] < 0:
            raise ValueError('Agent ', updated_agents[key]['name'], ' has less tokens: ', updated_agents[key]['tokens'], ' than planned selling allocation ', agent_allocations[key]['selling'],
                             ' and utility allocation ', agent_allocations[key]['utility'], ' plus removing allocation ', agent_allocations[key]['removed'], ' combined!')
        
        # update agent token allocations
        updated_agents[key]['selling_tokens'] = agent_allocations[key]['selling']
        updated_agents[key]['utility_tokens'] = agent_allocations[key]['utility']
        updated_agents[key]['holding_tokens'] = agent_allocations[key]['holding']
        updated_agents[key]['tokens'] = updated_agents[key]['tokens'] - agent_allocations[key]['selling'] - agent_allocations[key]['utility'] + agent_allocations[key]['removed']
        updated_agents[key]['tokens_apr_locked'] = updated_agents[key]['tokens_apr_locked'] + agent_allocations[key]['locking_apr']
        updated_agents[key]['tokens_buyback_locked'] = updated_agents[key]['tokens_buyback_locked'] + agent_allocations[key]['locking_buyback']
        updated_agents[key]['tokens_liquidity_provisioning'] = updated_agents[key]['tokens_liquidity_provisioning'] + agent_allocations[key]['liquidity']
        updated_agents[key]['tokens_transferred'] = updated_agents[key]['tokens_transferred'] + agent_allocations[key]['transfer']
        updated_agents[key]['tokens_burned'] = updated_agents[key]['tokens_burned'] + agent_allocations[key]['burn']

    return ('agents', updated_agents)




def update_meta_bucket_allocations(params, substep, state_history, prev_state, policy_input, **kwargs):
    """
    Function to update the meta bucket allocations
    """
    updated_meta_bucket_allocations = policy_input['meta_bucket_allocations']
    return ('meta_bucket_allocations',updated_meta_bucket_allocations)
