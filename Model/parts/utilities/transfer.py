# POLICY FUNCTIONS
def transfer_agent_allocation(params, substep, state_history, prev_state, **kwargs):
    """
    Policy function to calculate the agent transfer
    """
    # get parameters
    transfer_share = params['transfer_share']/100

    # get state variables
    agents = prev_state['agents'].copy()

    # policy logic
    # initialize policy logic variables
    agent_utility_sum = 0
    agent_utility_rewards_sum = 0
    agents_transfer_allocations = {}
    agents_transfer_rewards = {}

    # calculate the staking apr token allocations and removals for each agent
    for agent in agents:
        utility_tokens = agents[agent]['a_utility_tokens'] + agents[agent]['a_utility_from_holding_tokens'] # get the new agent utility token allocations from vesting, airdrops, incentivisation, and holdings of previous timestep
        agents_transfer_allocations[agent] = utility_tokens * transfer_share # calculate the amount of tokens that shall be allocated to the transfer utility from this timestep
           
        agent_utility_sum += agents_transfer_allocations[agent] # sum up the total amount of tokens allocated to the transfer for this timestep

    return {'agents_transfer_allocations': agents_transfer_allocations, 'agents_transfer_rewards': agents_transfer_rewards,
            'agent_utility_sum': agent_utility_sum, 'agent_utility_rewards_sum': agent_utility_rewards_sum}



# STATE UPDATE FUNCTIONS
def update_agents_after_transfer(params, substep, state_history, prev_state, policy_input, **kwargs):
    """
    Function to update agent transfer allocations
    """
    # get parameters
    transfer_destination = params['transfer_destination']

    # get state variables
    updated_agents = prev_state['agents'].copy()

    # get policy input
    agents_transfer_allocations = policy_input['agents_transfer_allocations']

    a_transfer_allocation = 0


    # update logic
    for agent in updated_agents:
        updated_agents[agent]['a_tokens_transferred'] = (agents_transfer_allocations[agent])
        updated_agents[agent]['a_tokens_transferred_cum'] += (agents_transfer_allocations[agent])
        a_transfer_allocation += updated_agents[agent]['a_tokens_transferred']

    for agent in updated_agents:
       if updated_agents[agent]['a_name'].lower() in transfer_destination.lower():
          updated_agents[agent]['a_tokens'] += a_transfer_allocation

    return ('agents', updated_agents)





def update_utilties_after_transfer(params, substep, state_history, prev_state, policy_input, **kwargs):
    """
    Function to update utilities after transfer 
    """

    # get state variables
    updated_utilities = prev_state['utilities'].copy()

    # get policy input
    agent_utility_sum = policy_input['agent_utility_sum']

    # update logic
    updated_utilities['u_transfer_allocation'] = (agent_utility_sum)
    updated_utilities['u_transfer_allocation_cum'] += (agent_utility_sum)

    return ('utilities', updated_utilities)