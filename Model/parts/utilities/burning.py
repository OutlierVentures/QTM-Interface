"""Calculation and processing of token burning at agect level.

Contains policy functions (PF) and state update functions (SUF).


Functions:
    burning_agent_allocation (PF): Policy function to calculate the agent burning.

    update_burning_agent_allocation (SUF): Function to update agent burning allocations.

    update_burning_meta_allocation (SUF): Function to update meta burning allocations.

"""

# POLICY FUNCTIONS
def burning_agent_allocation(params, substep, state_history, prev_state, **kwargs):
    """
    Policy function to calculate the agent burning
    """
    # get parameters
    burning_share = params['burning_share']/100

    # get state variables
    agents = prev_state['agents'].copy()

    # policy logic
    agent_utility_sum = 0
    agents_burning_allocations = {}
    if burning_share > 0:
        for agent in agents:
            utility_tokens = agents[agent]['a_utility_tokens'] + agents[agent]['a_utility_from_holding_tokens']
            agents_burning_allocations[agent] = utility_tokens * burning_share
            agent_utility_sum += agents_burning_allocations[agent]
    
    return {'u_burning_allocation': agent_utility_sum, 'agents_burning_allocations': agents_burning_allocations}


# STATE UPDATE FUNCTIONS
def update_burning_agent_allocation(params, substep, state_history, prev_state, policy_input, **kwargs):
    """
    Function to update agent burning allocations
    """
    # get parameters

    # get state variables
    updated_agents = prev_state['agents'].copy()

    # get policy input
    agents_burning_allocations = policy_input['agents_burning_allocations']

    # update logic
    if agents_burning_allocations != {}:
        for agent in updated_agents:
            updated_agents[agent]['a_tokens_burned'] = agents_burning_allocations[agent]
            updated_agents[agent]['a_tokens_burned_cum'] += agents_burning_allocations[agent]

    return ('agents', updated_agents)

def update_burning_meta_allocation(params, substep, state_history, prev_state, policy_input, **kwargs):
    """
    Function to update meta burning allocations
    """
    # get parameters

    # get state variables
    updated_utilities = prev_state['utilities'].copy()

    # get policy input
    burning_allocation = policy_input['u_burning_allocation']

    # update logic
    updated_utilities['u_burning_allocation'] = burning_allocation
    updated_utilities['u_burning_allocation_cum'] += burning_allocation

    return ('utilities', updated_utilities)