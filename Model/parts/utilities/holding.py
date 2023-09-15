# POLICY FUNCTIONS
def holding_agent_allocation(params, substep, state_history, prev_state, **kwargs):
    """
    Policy function to calculate the agent holding

    """
    # get parameters
    holding_share = params['holding_share']/100
    initial_lp_token_allocation = params['initial_lp_token_allocation']
    token_payout_apr = params['holding_apr'] / 100

    # get state variables
    agents = prev_state['agents'].copy()
    liquidity_pool = prev_state['liquidity_pool'].copy()

    #rewards
    token_after_adoption = liquidity_pool['lp_tokens_after_adoption']
    
    # policy logic
    # initialize policy logic variables
    agent_utility_sum = 0
    agent_utility_rewards_sum = 0
    agents_holding_allocations = {}
    agents_holding_rewards = {}

    # calculate the staking apr token allocations and removals for each agent
    for agent in agents:
        utility_tokens = agents[agent]['a_utility_tokens'] + agents[agent]['a_utility_from_holding_tokens'] # get the new agent utility token allocations from vesting, airdrops, incentivisation, and previous timestep holdings

        agents_holding_allocations[agent] = utility_tokens * holding_share # calculate the amount of tokens that shall be allocated to the staking apr utility from this timestep

        agent_utility_sum += agents_holding_allocations[agent] # sum up the total amount of tokens allocated to the staking apr utility for this timestep

        #rewards
        agents_holding_rewards[agent] = [(agents[agent]['a_tokens'] - agents[agent]['a_tokens_apr_locked_rewards'] - agents[agent]['a_tokens_apr_locked_remove']
                                          + agents_holding_allocations[agent]) * token_payout_apr/12 if agents[agent]['a_type'] != 'protocol_bucket' else 0][0] # calculate the amount of tokens that shall be rewarded to the agent for staking for this timestep
        
        agent_utility_rewards_sum += agents_holding_rewards[agent] # sum up the total amount of tokens rewarded to the agent for staking for this timestep

    return {'agents_holding_allocations': agents_holding_allocations, 'agents_holding_rewards': agents_holding_rewards,
            'agent_utility_sum': agent_utility_sum, 'agent_utility_rewards_sum': agent_utility_rewards_sum}


# STATE UPDATE FUNCTIONS
def update_agents_after_holding(params, substep, state_history, prev_state, policy_input, **kwargs):
    """
    Function to update agent holding allocations
    """

    # get parameters
    holding_payout_source = params['holding_payout_source']

    # get state variables
    updated_agents = prev_state['agents'].copy()

    # get policy input
    agents_holding_allocations = policy_input['agents_holding_allocations']
    agents_holding_rewards = policy_input['agents_holding_rewards']
    agent_utility_rewards_sum = policy_input['agent_utility_rewards_sum']

    # update logic
    for agent in updated_agents:
        updated_agents[agent]['a_tokens'] += (agents_holding_allocations[agent] + agents_holding_rewards[agent])

        # subtract tokens from payout source agent
        if updated_agents[agent]['a_name'].lower() in holding_payout_source.lower():
            updated_agents[agent]['a_tokens'] -= agent_utility_rewards_sum


    return ('agents', updated_agents)



def update_utilties_after_holding(params, substep, state_history, prev_state, policy_input, **kwargs):
    """
    Function to update meta burning allocations
    """
    # get parameters

    # get state variables
    updated_utilities = prev_state['utilities'].copy()

    # get policy input
    agent_utility_sum = policy_input['agent_utility_sum']
    agent_utility_rewards_sum = policy_input['agent_utility_rewards_sum']

    # update logic
    updated_utilities['u_holding_rewards'] = agent_utility_rewards_sum
    updated_utilities['u_holding_allocation'] = (agent_utility_sum)
    updated_utilities['u_holding_allocation_cum'] += (agent_utility_sum)

    return ('utilities', updated_utilities)

