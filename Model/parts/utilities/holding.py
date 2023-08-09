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
    

    # reward logic


    initial_lp_token_allocation = params['initial_lp_token_allocation']
    token_payout_apr = params['holding_apr']

    liquidity_pool = prev_state['liquidity_pool'].copy()
    lp_tokens = liquidity_pool['lp_tokens']
    holding_allocation = prev_state['utilities']['u_holding_allocation']

    #WILL NEED TO ADJUST SUBSTEPS TO PUT THIS ONE RIGHT AFTER ADOPTION

    #=(holding_allocation+(initial_lp_token_allocation-token_after_adoption)+agent_utility_sum)*token_payout_apr/100/12
    return {'u_holding_allocation': agent_utility_sum, 'agents_holding_allocations': agents_holding_allocations}


# STATE UPDATE FUNCTIONS
def update_holding_agent_allocation(params, substep, state_history, prev_state, policy_input, **kwargs):
    """
    Function to update agent holding allocations
    """
    # get parameters
    holding_payout_source = params['holding_payout_source']

    # get state variables
    updated_agents = prev_state['agents'].copy()

    # get policy input
    agents_holding_allocations = policy_input['agents_holding_allocations']

    # update logic
    for agent in updated_agents:
        updated_agents[agent]['a_tokens'] += agents_holding_allocations[agent]

        # update reward payout bucket

    return ('agents', updated_agents)



def update_holding_meta_allocation(params, substep, state_history, prev_state, policy_input, **kwargs):
    """
    Function to update meta burning allocations
    """
    # get parameters

    # get state variables
    updated_utilities = prev_state['utilities'].copy()

    # get policy input
    holding_allocation = policy_input['u_holding_allocation']

    # update logic
    updated_utilities['u_holding_allocation'] = holding_allocation

    return ('utilities', updated_utilities)

