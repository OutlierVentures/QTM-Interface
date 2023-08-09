# POLICY FUNCTIONS
def holding_agent_allocation(params, substep, state_history, prev_state, **kwargs):
    """
    Policy function to calculate the agent holding

    """
    # get parameters
    holding_share = params['holding_share']/100

    # get state variables
    agents = prev_state['agents'].copy()

    # policy logic
    agent_utility_sum = 0
    agents_holding_allocations = {}
    for agent in agents:
        utility_tokens = agents[agent]['a_utility_tokens']
        agents_holding_allocations[agent] = utility_tokens * holding_share
        agent_utility_sum += agents_holding_allocations[agent]
    
    return {'holding_allocation': agent_utility_sum, 'agents_holding_allocations': agents_holding_allocations}


# STATE UPDATE FUNCTIONS
def update_holding_agent_allocation(params, substep, state_history, prev_state, policy_input, **kwargs):
    """
    Function to update agent holding allocations
    """
    # get parameters

    # get state variables
    updated_agents = prev_state['agents'].copy()

    # get policy input
    agents_holding_allocations = policy_input['agents_holding_allocations']

    # update logic
    for agent in updated_agents:
        updated_agents[agent]['a_holding_tokens'] = agents_holding_allocations[agent]

    return ('agents', updated_agents)



def update_holding_meta_allocation(params, substep, state_history, prev_state, policy_input, **kwargs):
    """
    Function to update meta burning allocations
    """
    # get parameters

    # get state variables
    updated_utilities = prev_state['utilities'].copy()

    # get policy input
    holding_allocation = policy_input['holding_allocation']

    # update logic
    updated_utilities['holding_allocation'] = holding_allocation
    
    return ('utilities', updated_utilities)

