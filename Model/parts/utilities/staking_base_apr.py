# POLICIY FUNCTIONS
def staking_apr_allocation(params, substep, state_history, prev_state, **kwargs):
    """
    Policy function to for the staking apr calculation
    """
    # get parameters
    lock_apr = params['lock_apr']/100
    lock_share = params['lock_share']/100
    
    # get state variables
    agents = prev_state['agents'].copy()
    utility_removal_perc = prev_state['token_economy']['te_remove_perc']/100

    # policy logic
    # initialize policy logic variables
    agent_utility_sum = 0
    agent_utility_removal_sum = 0
    agent_utility_rewards_sum = 0
    agents_staking_apr_allocations = {}
    agents_staking_apr_removal = {}
    agents_staking_apr_rewards = {}

    # calculate the staking apr token allocations and removals for each agent
    for agent in agents:
        utility_tokens = agents[agent]['a_utility_tokens'] # get the new agent utility token allocations from vesting, airdrops, and incentivisation
        tokens_apr_locked_cum = agents[agent]['a_tokens_apr_locked_cum'] # get amount of staked tokens for base apr from last timestep
        
        agents_staking_apr_allocations[agent] = utility_tokens * lock_share # calculate the amount of tokens that shall be allocated to the staking apr utility from this timestep
        agents_staking_apr_removal[agent] = tokens_apr_locked_cum * utility_removal_perc # calculate the amount of tokens that shall be removed from the staking apr utility for this timestep based on the tokens allocated in the previous timestep
        agents_staking_apr_rewards[agent] = agents_staking_apr_allocations[agent] * lock_apr/12 # calculate the amount of tokens that shall be rewarded to the agent for staking
        
        agent_utility_sum += agents_staking_apr_allocations[agent] # sum up the total amount of tokens allocated to the staking apr utility for this timestep
        agent_utility_removal_sum += agents_staking_apr_removal[agent] # sum up the total amount of tokens removed from the staking apr utility for this timestep
        agent_utility_rewards_sum += agents_staking_apr_rewards[agent] # sum up the total amount of tokens rewarded to the agent for staking for this timestep

    return {'agents_staking_apr_allocations': agents_staking_apr_allocations,'agents_staking_apr_removal':agents_staking_apr_removal,
            'agents_staking_apr_rewards': agents_staking_apr_rewards, 'agent_utility_sum': agent_utility_sum,
            'agent_utility_removal_sum': agent_utility_removal_sum, 'agent_utility_rewards_sum': agent_utility_rewards_sum}


# STATE UPDATE FUNCTIONS
def update_utilties_after_apr(params, substep, state_history, prev_state, policy_input, **kwargs):
    """
    Function to update the utilities after apr
    """
    # get state variables
    updated_utilities = prev_state['utilities'].copy()

    # get policy input
    agent_utility_sum = policy_input['agent_utility_sum']
    agent_utility_removal_sum = policy_input['agent_utility_removal_sum']
    agent_utility_rewards_sum = policy_input['agent_utility_rewards_sum']

    # update logic
    updated_utilities['u_staking_rewards'] = agent_utility_rewards_sum
    updated_utilities['u_staking_base_apr'] = (agent_utility_sum - agent_utility_removal_sum)
    updated_utilities['u_staking_base_apr_cum'] += (agent_utility_sum - agent_utility_removal_sum)
    updated_utilities['u_staking_base_apr_remove'] = agent_utility_removal_sum

    return ('utilities', updated_utilities)



def update_agents_after_apr(params, substep, state_history, prev_state, policy_input, **kwargs):
    """
    Function to update the utilities after apr
    """
    # get parameters
    lock_payout_source = params['lock_payout_source']

    # get state variables
    updated_agents = prev_state['agents'].copy()

    # get policy input
    agents_staking_apr_allocations = policy_input['agents_staking_apr_allocations']
    agents_staking_apr_removal = policy_input['agents_staking_apr_removal']
    agents_staking_apr_rewards = policy_input['agents_staking_apr_rewards']
    agent_utility_rewards_sum = policy_input['agent_utility_rewards_sum']

    # update logic
    # TODO?
    """'a_tokens_apr_locked': tokens_apr_locked, # amount of tokens locked for APR per timestep
    'a_tokens_apr_locked_cum': tokens_apr_locked_cum, # amount of tokens locked for APR cumulatively
    'a_tokens_apr_locked_remove': tokens_apr_locked_remove, # amount of tokens removed from staking for base apr """

    for agent in updated_agents:
        updated_agents[agent]['a_tokens_apr_locked'] = (agents_staking_apr_allocations[agent] - agents_staking_apr_removal[agent])
        updated_agents[agent]['a_tokens_apr_locked_cum'] += (agents_staking_apr_allocations[agent] - agents_staking_apr_removal[agent])
        updated_agents[agent]['a_tokens_apr_locked_remove'] = agents_staking_apr_removal[agent]
        updated_agents[agent]['a_tokens'] += agents_staking_apr_rewards[agent]

        # subtract tokens from payout source agent
        if updated_agents[agent]['a_name'].lower() in lock_payout_source.lower():
            updated_agents[agent]['a_tokens'] -= agent_utility_rewards_sum

    return ('agents', updated_agents)



