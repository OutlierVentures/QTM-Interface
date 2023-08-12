# POLICY FUNCTIONS
def transfer_agent_allocation(params, substep, state_history, prev_state, **kwargs):
    """
    Policy function to calculate the agent transfer
    """
    # get parameters
    transfer_share = params['transfer_share']/100


    # get state variables
    agents = prev_state['agents'].copy()
    utility_removal_perc = prev_state['token_economy']['te_remove_perc']/100


    # policy logic
    # initialize policy logic variables
    agent_utility_sum = 0
    agent_utility_removal_sum = 0
    agent_utility_rewards_sum = 0
    agents_transfer_allocations = {}
    agents_transfer_removal = {}
    agents_transfer_rewards = {}

    # calculate the staking apr token allocations and removals for each agent
    for agent in agents:
        utility_tokens = agents[agent]['a_utility_tokens'] # get the new agent utility token allocations from vesting, airdrops, and incentivisation
        tokens_apr_locked_cum = agents[agent]['a_tokens_transferred_cum'] # get amount of staked tokens for transfer from last timestep   
        agents_transfer_allocations[agent] = utility_tokens * transfer_share # calculate the amount of tokens that shall be allocated to the transfer utility from this timestep
        agents_transfer_removal[agent] = tokens_apr_locked_cum * utility_removal_perc # calculate the amount of tokens that shall be removed from the transfer for this timestep based on the tokens allocated in the previous timestep
        
        
        #NEED TO CALCULATE REWARDS
        #agents_transfer_rewards
         
                
        agent_utility_sum += agents_transfer_allocations[agent] # sum up the total amount of tokens allocated to the transfer for this timestep
        agent_utility_removal_sum += agents_transfer_removal[agent] # sum up the total amount of tokens removed from the transfer for this timestep
        #agent_utility_rewards_sum += agents_transfer_rewards[agent] # sum up the total amount of tokens rewarded to the agent for transfer for this timestep


    return {'agents_transfer_allocations': agents_transfer_allocations,'agents_transfer_removal':agents_transfer_removal,
            'agents_transfer_rewards': agents_transfer_rewards, 'agent_utility_sum': agent_utility_sum,
            'agent_utility_removal_sum': agent_utility_removal_sum, 'agent_utility_rewards_sum': agent_utility_rewards_sum}








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


    agents_transfer_removal = policy_input['agents_transfer_removal']
    agents_transfer_rewards = policy_input['agents_transfer_rewards']
    #agent_utility_rewards_sum = policy_input['agent_utility_rewards_sum']


    # update logic

    for agent in updated_agents:
        updated_agents[agent]['a_tokens_transferred'] = (agents_transfer_allocations[agent] - agents_transfer_removal[agent])
        updated_agents[agent]['a_tokens_transferred_cum'] += (agents_transfer_allocations[agent] - agents_transfer_removal[agent])
        updated_agents[agent]['a_tokens_transfer_remove'] = agents_transfer_removal[agent]
        #updated_agents[agent]['a_tokens'] += agents_transfer_rewards[agent]

        # update transfer destination bucket
        #if updated_agents[agent]['a_type'] == 'protocol_bucket' and transfer_destination.lower() in updated_agents[agent]['a_name'].lower():
        #    updated_agents[agent]['a_tokens'] = updated_agents[agent]['a_tokens'] + transferred_tokens_by_agent
    

    return ('agents', updated_agents)





def update_utilties_after_transfer(params, substep, state_history, prev_state, policy_input, **kwargs):
    """
    Function to update utilities after transfer 
    """



    # get state variables
    updated_utilities = prev_state['utilities'].copy()

    # get policy input
    agent_utility_sum = policy_input['agent_utility_sum']
    agent_utility_removal_sum = policy_input['agent_utility_removal_sum']
    agent_utility_rewards_sum = policy_input['agent_utility_rewards_sum']

    # update logic
    #updated_utilities['u_transfer_rewards'] = agent_utility_rewards_sum
    updated_utilities['u_transfer_allocation'] = (agent_utility_sum - agent_utility_removal_sum)
    updated_utilities['u_transfer_allocation_cum'] += (agent_utility_sum - agent_utility_removal_sum)
    updated_utilities['u_transfer_allocation_remove'] = agent_utility_removal_sum

    return ('utilities', updated_utilities)