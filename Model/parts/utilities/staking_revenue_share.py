# POLICY FUNCTIONS
def staking_revenue_share_buyback_allocation(params, substep, state_history, prev_state, **kwargs):
    """
    Policy function to calculate the agent staking allocation for token buybacks from the revenue share
    """
    # get parameters
    lock_buyback_distribute_share = params['lock_buyback_distribute_share']/100

    # get state variables
    agents = prev_state['agents'].copy()
    utilities = prev_state['utilities'].copy()
    utility_removal_perc = prev_state['token_economy']['te_remove_perc']/100

    # rewards state variables
    lp_tokens_after_liquidity_addition  =  prev_state['liquidity_pool']['lp_tokens_after_liquidity_addition']
    lp_tokens_after_liquidity_buyback = prev_state['liquidity_pool']['lp_tokens'] # Tokens after trx 4 (buybacks)
    u_buyback_from_revenue_share_usd = prev_state['utilities']['u_buyback_from_revenue_share_usd']
    ba_buybacks_usd =prev_state['business_assumptions']['ba_buybacks_usd']

    # policy logic
    # initialize policy logic variables
    agent_utility_sum = 0
    agent_utility_removal_sum = 0
    agent_utility_rewards_sum = 0
    agents_staking_buyback_allocations = {}
    agents_staking_buyback_removal = {}
    agents_staking_buyback_rewards = {}

    # calculate macro rewards from staking revenue share
    agent_utility_rewards_sum = (lp_tokens_after_liquidity_addition - lp_tokens_after_liquidity_buyback) * (u_buyback_from_revenue_share_usd/ba_buybacks_usd) 

    # calculate the staking apr token allocations and removals for each agent
    for agent in agents:
        utility_tokens = agents[agent]['a_utility_tokens'] # get the new agent utility token allocations from vesting, airdrops, and incentivisation
        tokens_buyback_locked_cum = agents[agent]['a_tokens_buyback_locked_cum'] # get amount of staked tokens for revenue share last timestep

        agents_staking_buyback_allocations[agent] = utility_tokens * lock_buyback_distribute_share # calculate the amount of tokens that shall be allocated to the staking apr utility from this timestep
        agents_staking_buyback_removal[agent] = tokens_buyback_locked_cum * utility_removal_perc # calculate the amount of tokens that shall be removed from the staking apr utility for this timestep based on the tokens allocated in the previous timestep
        
        agent_utility_sum += agents_staking_buyback_allocations[agent] # sum up the total amount of tokens allocated to the staking apr utility for this timestep
        agent_utility_removal_sum += agents_staking_buyback_removal[agent] # sum up the total amount of tokens removed from the staking apr utility for this timestep

    # allocate staking rewards for this agent
    for agent in agents:
        if (utilities['u_staking_revenue_share_allocation_cum'] + agent_utility_sum - agent_utility_removal_sum) > 0:
            agents_staking_buyback_rewards[agent] = agent_utility_rewards_sum * (
                (agents[agent]['a_tokens_buyback_locked_cum'] + agents_staking_buyback_allocations[agent]-agents_staking_buyback_removal[agent])
                / (utilities['u_staking_revenue_share_allocation_cum'] + agent_utility_sum - agent_utility_removal_sum))
        else:
            agents_staking_buyback_rewards[agent] = 0
    
    # consistency check (remove later for better performance)
    agent_rewards = 0
    for agent in agents:
        agent_rewards += agents_staking_buyback_rewards[agent]
    assert abs(agent_rewards - agent_utility_rewards_sum) < 0.0000000000001, 'agent rewards '+str(agent_rewards)+' do not match macro rewards'+str(agent_utility_rewards_sum)

    return {'agents_staking_buyback_allocations': agents_staking_buyback_allocations,'agents_staking_buyback_removal':agents_staking_buyback_removal,
            'agents_staking_buyback_rewards': agents_staking_buyback_rewards, 'agent_utility_sum': agent_utility_sum,
            'agent_utility_removal_sum': agent_utility_removal_sum, 'agent_utility_rewards_sum': agent_utility_rewards_sum}



def staking_revenue_share_buyback_amount(params, substep, state_history, prev_state, **kwargs):
    """
    Policy function to calculate the amount of usd to be used for token buyback from the revenue share
    """
    # get parameters
    staking_revenue_utility_share_allocation = params['lock_buyback_distribute_share']
    revenue_share = params['lock_buyback_from_revenue_share'] # revenue share to be used for buyback

    # get state variables
    user_adoption = prev_state['user_adoption'].copy()
    product_revenue = user_adoption['ua_product_revenue']

    # policy logic
    if float(staking_revenue_utility_share_allocation) > 0:
        buyback_amount = product_revenue * float(revenue_share) / 100
    else:
        buyback_amount = 0

    return {'u_buyback_from_revenue_share_usd': buyback_amount}




# STATE UPDATE FUNCTIONS
def update_agents_after_staking_revenue_share_buyback(params, substep, state_history, prev_state, policy_input, **kwargs):
    """
    Function to update agent staking allocation for token buybacks from the revenue share
    """
    # get state variables
    updated_agents = prev_state['agents'].copy()

    # get policy input
    agents_staking_buyback_allocations = policy_input['agents_staking_buyback_allocations']
    agents_staking_buyback_removal = policy_input['agents_staking_buyback_removal']
    agent_rewards = policy_input['agents_staking_buyback_rewards']

    # update logic
    for agent in updated_agents:
        updated_agents[agent]['a_tokens'] += agent_rewards[agent]
        updated_agents[agent]['a_tokens_buyback_locked'] = (agents_staking_buyback_allocations[agent] - agents_staking_buyback_removal[agent])
        updated_agents[agent]['a_tokens_buyback_locked_cum'] += (agents_staking_buyback_allocations[agent] - agents_staking_buyback_removal[agent])
        updated_agents[agent]['a_tokens_buyback_locked_remove'] = agents_staking_buyback_removal[agent]

    return ('agents', updated_agents)


def update_utilities_after_staking_revenue_share_buyback(params, substep, state_history, prev_state, policy_input, **kwargs):
    """
    Function to update meta staking allocation for token buybacks from the revenue share
    """
    # get state variables
    updated_utilities = prev_state['utilities'].copy()

    # get policy input
    agent_utility_sum = policy_input['agent_utility_sum']
    agent_utility_removal_sum = policy_input['agent_utility_removal_sum']
    agent_utility_rewards_sum = policy_input['agent_utility_rewards_sum']

    # update logic
    updated_utilities['u_staking_revenue_share_rewards'] = agent_utility_rewards_sum
    updated_utilities['u_staking_revenue_share_allocation'] = (agent_utility_sum - agent_utility_removal_sum)
    updated_utilities['u_staking_revenue_share_allocation_cum'] += (agent_utility_sum - agent_utility_removal_sum)
    updated_utilities['u_staking_revenue_share_remove'] = agent_utility_removal_sum

    return ('utilities', updated_utilities)

def update_buyback_amount_from_revenue_share(params, substep, state_history, prev_state, policy_input, **kwargs):
    """
    Function to update capital amount for token buybacks from the revenue share
    """
    # get parameters

    # get state variables
    updated_utilities = prev_state['utilities'].copy()

    # get policy input
    buyback_from_revenue_share_usd = policy_input['u_buyback_from_revenue_share_usd']

    # update logic
    updated_utilities['u_buyback_from_revenue_share_usd'] = buyback_from_revenue_share_usd

    return ('utilities', updated_utilities)