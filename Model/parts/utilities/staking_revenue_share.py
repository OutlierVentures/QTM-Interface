# POLICY FUNCTIONS
def staking_revenue_share_buyback(params, substep, state_history, prev_state, **kwargs):
    """
    Policy function to calculate the agent staking rewards for token buybacks from the revenue share
    """
    # get state variables
    agents = prev_state['agents'].copy()
    utilities = prev_state['utilities'].copy()

    # rewards state variables
    lp_tokens_after_liquidity_addition  =  prev_state['liquidity_pool']['lp_tokens_after_liquidity_addition']
    lp_tokens_after_buyback = prev_state['liquidity_pool']['lp_tokens'] # Tokens after trx 4 (buybacks)
    u_buyback_from_revenue_share_usd = prev_state['utilities']['u_buyback_from_revenue_share_usd']
    ba_buybacks_usd =prev_state['business_assumptions']['ba_buybacks_usd']

    # policy logic
    # initialize policy logic variables
    agent_utility_rewards_sum = 0
    agents_staking_buyback_rewards = {}

    # calculate macro rewards from staking revenue share
    bought_back_tokens = (lp_tokens_after_liquidity_addition - lp_tokens_after_buyback)
    if ba_buybacks_usd > 0:
        agent_utility_rewards_sum = bought_back_tokens * (u_buyback_from_revenue_share_usd/ba_buybacks_usd)
        business_buyback = bought_back_tokens * (1 - u_buyback_from_revenue_share_usd/ba_buybacks_usd)
    elif ba_buybacks_usd == 0:
        agent_utility_rewards_sum = 0
        business_buyback = 0
    else:
        raise ValueError("Business buybacks in USD terms (ba_buybacks_usd) must not be negative!")

    # allocate staking rewards for agents
    if agent_utility_rewards_sum > 0:
        for agent in agents:
            if (utilities['u_staking_allocation_cum']) > 0:
                agents_staking_buyback_rewards[agent] = agent_utility_rewards_sum * (
                    (agents[agent]['a_tokens_staked_cum'])
                    / (utilities['u_staking_allocation_cum']))
            else:
                agents_staking_buyback_rewards[agent] = 0

    return {'agents_staking_buyback_rewards': agents_staking_buyback_rewards, 'agent_utility_rewards_sum': agent_utility_rewards_sum, 'business_buyback': business_buyback}



# STATE UPDATE FUNCTIONS
def update_agents_after_staking_revenue_share_buyback(params, substep, state_history, prev_state, policy_input, **kwargs):
    """
    Function to update agent staking allocation for token buybacks from the revenue share
    """
    # get parameters
    buyback_bucket = params['buyback_bucket']

    # get state variables
    updated_agents = prev_state['agents'].copy()

    # get policy input
    agent_rewards = policy_input['agents_staking_buyback_rewards']
    business_buyback = policy_input['business_buyback']

    # update logic
    if agent_rewards != {} or business_buyback != 0:
        for agent in updated_agents:
            if agent_rewards != {}:
                updated_agents[agent]['a_tokens_staking_buyback_rewards'] = agent_rewards[agent]
                updated_agents[agent]['a_tokens_staking_buyback_rewards_cum'] += agent_rewards[agent]
                updated_agents[agent]['a_tokens'] += (agent_rewards[agent])

            # transfer business bought back tokens to destination
            if updated_agents[agent]['a_name'].lower() in buyback_bucket.lower():
                updated_agents[agent]['a_tokens'] += business_buyback

    return ('agents', updated_agents)


def update_utilities_after_staking_revenue_share_buyback(params, substep, state_history, prev_state, policy_input, **kwargs):
    """
    Function to update meta staking allocation for token buybacks from the revenue share
    """
    # get state variables
    updated_utilities = prev_state['utilities'].copy()

    # get policy input
    agent_utility_rewards_sum = policy_input['agent_utility_rewards_sum']

    # update logic
    updated_utilities['u_staking_revenue_share_rewards'] = agent_utility_rewards_sum

    return ('utilities', updated_utilities)