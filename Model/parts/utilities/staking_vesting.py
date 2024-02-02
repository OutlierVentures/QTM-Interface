# POLICIY FUNCTIONS
def staking_vesting_allocation(params, substep, state_history, prev_state, **kwargs):
    """
    Policy function to for the staking vesting calculation (rewards based on fixed vesting schedule)
    """
    # get parameters
    staking_share = params['staking_share']/100
    agent_behavior = params['agent_behavior']
    
    # get state variables
    agents = prev_state['agents'].copy()
    utilities = prev_state['utilities'].copy()

    # policy logic
    # initialize policy logic variables
    agent_utility_sum = 0
    agent_utility_removal_sum = 0
    agents_staking_allocations = {}
    agents_staking_removal = {}
    agents_staking_vesting_rewards = {}
    staking_vesting_bucket_tokens = [agents[agent]['a_tokens'] for agent in agents if agents[agent]['a_name'] == 'staking_vesting'][0] # get the amount of tokens in the staking vesting bucket
    max_staking_share = max([agents[agent]['a_actions']['St'] for agent in agents])

    if staking_vesting_bucket_tokens > 0 or max_staking_share > 0:
        # calculate the staking vesting allocations per agent
        for agent in agents:
            if agent_behavior == 'simple':
                staking_share = agents[agent]['a_actions']['St']
            utility_removal_perc = agents[agent]['a_actions']['remove_tokens']
            utility_tokens = agents[agent]['a_utility_tokens'] + agents[agent]['a_utility_from_holding_tokens'] # get the new agent utility token allocations from vesting, airdrops, incentivisation, and holdings of previous timestep
            tokens_staked_cum = agents[agent]['a_tokens_staked_cum'] # get amount of staked tokens from last timestep
            
            agents_staking_allocations[agent] = utility_tokens * staking_share # calculate the amount of tokens that shall be allocated to the staking utility from this timestep
            agents_staking_removal[agent] = tokens_staked_cum * utility_removal_perc # calculate the amount of tokens that shall be removed from the staking utility for this timestep based on the tokens allocated in the previous timestep
            
            agent_utility_sum += agents_staking_allocations[agent] # sum up the total amount of tokens allocated to the staking utility for this timestep
            agent_utility_removal_sum += agents_staking_removal[agent] # sum up the total amount of tokens removed from the staking utility for this timestep#

    # calculate the staking vesting rewards per agent
    if staking_vesting_bucket_tokens > 0 or staking_vesting_bucket_tokens > 0 or max_staking_share > 0:
        for agent in agents:
            if (utilities['u_staking_allocation_cum'] + agent_utility_sum - agent_utility_removal_sum) > 0:
                agents_staking_vesting_rewards[agent] = staking_vesting_bucket_tokens * (
                    (agents[agent]['a_tokens_staked_cum'] + agents_staking_allocations[agent]-agents_staking_removal[agent])
                    / (utilities['u_staking_allocation_cum'] + agent_utility_sum - agent_utility_removal_sum))
            else:
                agents_staking_vesting_rewards[agent] = 0

    return {'agents_staking_allocations': agents_staking_allocations,'agents_staking_removal':agents_staking_removal,
            'agents_staking_vesting_rewards': agents_staking_vesting_rewards, 'agent_utility_sum': agent_utility_sum,
            'agent_utility_removal_sum': agent_utility_removal_sum, 'staking_vesting_bucket_tokens': staking_vesting_bucket_tokens}


# STATE UPDATE FUNCTIONS
def update_utilties_after_staking_vesting(params, substep, state_history, prev_state, policy_input, **kwargs):
    """
    Function to update the utilities after staking vesting
    """
    # get state variables
    updated_utilities = prev_state['utilities'].copy()

    # get policy input
    agent_utility_sum = policy_input['agent_utility_sum']
    agent_utility_removal_sum = policy_input['agent_utility_removal_sum']
    agent_utility_rewards_sum = policy_input['staking_vesting_bucket_tokens']

    # update logic
    updated_utilities['u_staking_vesting_rewards'] = agent_utility_rewards_sum
    updated_utilities['u_staking_allocation'] = (agent_utility_sum)
    updated_utilities['u_staking_allocation_cum'] += (agent_utility_sum - agent_utility_removal_sum)
    updated_utilities['u_staking_remove'] = agent_utility_removal_sum
    
    return ('utilities', updated_utilities)



def update_agents_after_staking_vesting(params, substep, state_history, prev_state, policy_input, **kwargs):
    """
    Function to update the utilities after apr
    """
    # get state variables
    updated_agents = prev_state['agents'].copy()

    # get policy input
    agents_staking_allocations = policy_input['agents_staking_allocations']
    agents_staking_removal = policy_input['agents_staking_removal']
    agents_staking_vesting_rewards = policy_input['agents_staking_vesting_rewards']
    staking_vesting_bucket_tokens = policy_input['staking_vesting_bucket_tokens']

    # update logic
    if agents_staking_allocations != {} or agents_staking_vesting_rewards != {}:
        for agent in updated_agents:
            updated_agents[agent]['a_tokens_staked'] = (agents_staking_allocations[agent])
            updated_agents[agent]['a_tokens_staked_cum'] += (agents_staking_allocations[agent] - agents_staking_removal[agent])
            updated_agents[agent]['a_tokens_staked_remove'] = agents_staking_removal[agent]
            updated_agents[agent]['a_tokens_staking_vesting_rewards'] = agents_staking_vesting_rewards[agent]
            updated_agents[agent]['a_tokens_staking_vesting_rewards_cum'] += agents_staking_vesting_rewards[agent]
            updated_agents[agent]['a_tokens'] += (agents_staking_vesting_rewards[agent] + agents_staking_removal[agent])

            # subtract tokens from payout source agent
            if updated_agents[agent]['a_name'].lower() == "staking_vesting":
                updated_agents[agent]['a_tokens'] -= staking_vesting_bucket_tokens

    return ('agents', updated_agents)



