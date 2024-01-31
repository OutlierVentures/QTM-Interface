from Model.parts.utils import calculate_buyback_share_tokens

# POLICY FUNCTIONS
def staking_revenue_share_buyback(params, substep, state_history, prev_state, **kwargs):
    """
    Policy function to calculate the agent staking rewards for token buybacks from the revenue share
    """
    # get state variables
    agents = prev_state['agents'].copy()
    liquidity_pool = prev_state['liquidity_pool'].copy()
    utilities = prev_state['utilities'].copy()

    # rewards state variables
    lp_tokens_after_liquidity_addition  =  liquidity_pool['lp_tokens_after_liquidity_addition']
    lp_tokens_after_buyback = liquidity_pool['lp_tokens'] # Tokens after trx 4 (buybacks)
    u_buyback_from_revenue_share_staking_usd = utilities['u_buyback_from_revenue_share_staking_usd']
    ba_buybacks_usd =prev_state['business_assumptions']['ba_buybacks_usd']

    # policy logic
    # initialize policy logic variables
    agents_staking_buyback_rewards = {}

    buyback_share_tokens = calculate_buyback_share_tokens(u_buyback_from_revenue_share_staking_usd, ba_buybacks_usd, lp_tokens_after_liquidity_addition, lp_tokens_after_buyback)

    # allocate staking rewards for agents
    if buyback_share_tokens > 0:
        for agent in agents:
            if (utilities['u_staking_allocation_cum']) > 0:
                agents_staking_buyback_rewards[agent] = buyback_share_tokens * (
                    (agents[agent]['a_tokens_staked_cum'])
                    / (utilities['u_staking_allocation_cum']))
            else:
                agents_staking_buyback_rewards[agent] = 0

    return {'agents_staking_buyback_rewards': agents_staking_buyback_rewards, 'agent_utility_rewards_sum': buyback_share_tokens}



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

    # update logic
    if agent_rewards != {}:
        for agent in updated_agents:
            if agent_rewards != {}:
                updated_agents[agent]['a_tokens_staking_buyback_rewards'] = agent_rewards[agent]
                updated_agents[agent]['a_tokens_staking_buyback_rewards_cum'] += agent_rewards[agent]
                updated_agents[agent]['a_tokens'] += (agent_rewards[agent])

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