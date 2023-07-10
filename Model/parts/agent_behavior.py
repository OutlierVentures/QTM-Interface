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
                'locking': params['lock_share'],
                'liquidity': params['liquidity_mining_share'],
                'transfer': params['transfer_share'],
                'burning': params['burning_share']
            }

    return {'agent_behavior_dict': agent_behavior_dict}

def agent_token_allocations(params, substep, state_history, prev_state, **kwargs):
    """
    Define the meta bucket token allocations of all agents with respect to 'sell' 'hold' and 'utility'
    """
    agents = prev_state['agents']

    # initialize meta bucket token allocations
    meta_bucket_allocations= {
        'selling': 0,
        'holding': 0,
        'utility': 0,
        'removed': 0
    }

    utility_bucket_allocations = {
        'locking': 0,
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
            behavior_lst_remove_index = agents[agent]['action_list'].index('remove_locked_tokens')
            behavior_lst_locking_index = agents[agent]['action_list'].index('locking')
            behavior_lst_liquidity_index = agents[agent]['action_list'].index('liquidity')
            behavior_lst_transfer_index = agents[agent]['action_list'].index('transfer')
            behavior_lst_burning_index = agents[agent]['action_list'].index('burning')

            # get agent static behavior percentages
            selling_perc = agents[agent]['action_weights'][behavior_lst_sell_index]
            utility_perc = agents[agent]['action_weights'][behavior_lst_utility_index]
            remove_perc = agents[agent]['action_weights'][behavior_lst_remove_index]
            locking_perc = agents[agent]['action_weights'][behavior_lst_locking_index]
            liquidity_perc = agents[agent]['action_weights'][behavior_lst_liquidity_index]
            transfer_perc = agents[agent]['action_weights'][behavior_lst_transfer_index]
            burn_perc = agents[agent]['action_weights'][behavior_lst_burning_index]

            # calculate corresponding absolute token amounts for meta buckets
            sold_tokens = agents[agent]['tokens'] * selling_perc/100
            utility_tokens = agents[agent]['tokens'] * utility_perc/100
            removed_tokens = (agents[agent]['tokens_locked'] + agents[agent]['tokens_liquidity_provisioning']) * remove_perc/100
            locked_tokens = utility_tokens * locking_perc/100
            liquidity_tokens = utility_tokens * liquidity_perc/100
            transfer_tokens = utility_tokens * transfer_perc/100
            burn_tokens = utility_tokens * burn_perc/100

            # populate meta bucket allocations
            meta_bucket_allocations['selling'] += sold_tokens
            meta_bucket_allocations['holding'] += agents[agent]['tokens'] - sold_tokens - utility_tokens + removed_tokens
            meta_bucket_allocations['utility'] += utility_tokens
            meta_bucket_allocations['removed'] += removed_tokens

            # populate utility bucket allocations
            utility_bucket_allocations['locking'] += locked_tokens
            utility_bucket_allocations['liquidity'] += liquidity_tokens
            utility_bucket_allocations['transfer'] += transfer_tokens
            utility_bucket_allocations['burn'] += burn_tokens

            # update agent token allocations
        agent_allocations[agent] = {
            'selling': sold_tokens,
            'holding': agents[agent]['tokens'] - sold_tokens - utility_tokens + removed_tokens,
            'utility': utility_tokens,
            'removed': removed_tokens,
            'locking': locked_tokens,
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

        if updated_agents[key]['tokens'] - agent_allocations[key]['selling'] - agent_allocations[key]['selling'] + agent_allocations[key]['removed'] < 0:
            raise ValueError('Agent ', updated_agents[key]['name'], ' has less tokens: ', updated_agents[key]['tokens'], ' than planned selling allocation ', agent_allocations[key]['selling'],
                             ' and utility allocation ', agent_allocations[key]['utility'], ' plus removing allocation ', agent_allocations[key]['removed'], ' combined!')
        
        # update agent token allocations
        updated_agents[key]['tokens'] = updated_agents[key]['tokens'] - agent_allocations[key]['selling'] - agent_allocations[key]['utility'] + agent_allocations[key]['removed']
        updated_agents[key]['tokens_locked'] = updated_agents[key]['tokens_locked'] + agent_allocations[key]['locking']
        updated_agents[key]['tokens_liquidity_provisioning'] = updated_agents[key]['tokens_liquidity_provisioning'] + agent_allocations[key]['liquidity']
        updated_agents[key]['tokens_transferred'] = updated_agents[key]['tokens_transferred'] + agent_allocations[key]['transfer']
        updated_agents[key]['tokens_burned'] = updated_agents[key]['tokens_burned'] + agent_allocations[key]['burn']

    return ('agents', updated_agents)