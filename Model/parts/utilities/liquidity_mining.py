# POLICY FUNCTIONS
def staking_liquidity_mining_agent_allocation(params, substep, state_history, prev_state, **kwargs):
    """
    Policy function to calculate the agent liquidity mining
    """
    # get parameters
    liquidity_mining_share = params['liquidity_mining_share']/100

    # get state variables
    agents = prev_state['agents'].copy()

    # policy logic
    agent_utility_sum = 0
    agents_liquidity_mining_allocations = {}
    for agent in agents:
        utility_tokens = agents[agent]['a_utility_tokens']
        agents_liquidity_mining_allocations[agent] = utility_tokens * liquidity_mining_share
        agent_utility_sum += agents_liquidity_mining_allocations[agent]
    
    return {'liquidity_mining_allocation': agent_utility_sum, 'agents_liquidity_mining_allocations': agents_liquidity_mining_allocations}


# STATE UPDATE FUNCTIONS
def update_liquidity_mining_agent_allocation(params, substep, state_history, prev_state, policy_input, **kwargs):
    """
    Function to update agent liquidity mining allocations
    """
    # get parameters

    # get state variables
    updated_agents = prev_state['agents'].copy()

    # get policy input
    agents_liquidity_mining_allocations = policy_input['agents_liquidity_mining_allocations']

    # update logic
    for agent in updated_agents:
        updated_agents[agent]['a_tokens_liquidity_mining'] = agents_liquidity_mining_allocations[agent]
        updated_agents[agent]['a_tokens_liquidity_mining_cum'] += agents_liquidity_mining_allocations[agent]

    return ('agents', updated_agents)

def update_liquidity_mining_meta_allocation(params, substep, state_history, prev_state, policy_input, **kwargs):
    """
    Function to update meta liquidity mining allocations
    """
    # get parameters

    # get state variables
    updated_utilities = prev_state['utilities'].copy()

    # get policy input
    liquidity_mining_allocation = policy_input['liquidity_mining_allocation']

    # update logic
    updated_utilities['liquidity_mining_allocation'] = liquidity_mining_allocation
    updated_utilities['liquidity_mining_allocation_cum'] += liquidity_mining_allocation

    return ('utilities', updated_utilities)