# POLICIY FUNCTIONS
def staking_mint_burn(params, substep, state_history, prev_state, **kwargs):
    """
    Policy function to for the staking minting calculation (rewards based on minted tokens based on burned tokens)
    """
    # get parameters
    mint_burn_ratio = params['mint_burn_ratio']
    
    # get state variables
    agents = prev_state['agents'].copy()
    utilities = prev_state['utilities'].copy()
    token_economy = prev_state['token_economy'].copy()

    # policy logic
    # initialize policy logic variables
    te_tokens_burned = token_economy['te_tokens_burned']
    new_tokens_minted = te_tokens_burned * mint_burn_ratio
    agents_staking_minting_rewards = {}

    # calculate the staking minting rewards per agent
    if new_tokens_minted > 0:
        for agent in agents:
            if (utilities['u_staking_allocation_cum']) > 0:
                agents_staking_minting_rewards[agent] = new_tokens_minted * (
                    (agents[agent]['a_tokens_staked_cum'])
                    / (utilities['u_staking_allocation_cum']))
            else:
                agents_staking_minting_rewards[agent] = 0

    return {'agents_staking_minting_rewards': agents_staking_minting_rewards, 'new_tokens_minted': new_tokens_minted}


# STATE UPDATE FUNCTIONS
def update_utilties_after_staking_mint_burn(params, substep, state_history, prev_state, policy_input, **kwargs):
    """
    Function to update the utilities after staking vesting
    """
    # get state variables
    updated_utilities = prev_state['utilities'].copy()
    liquidity_pool = prev_state['liquidity_pool'].copy()

    # get policy input
    new_tokens_minted = policy_input['new_tokens_minted']

    # update logic
    updated_utilities['u_staking_minting_rewards'] = new_tokens_minted
    updated_utilities['u_staking_minting_rewards_cum'] += new_tokens_minted
    updated_utilities['u_staking_minting_rewards_cum_usd'] += new_tokens_minted * liquidity_pool['lp_token_price']
    
    return ('utilities', updated_utilities)


def update_agents_after_staking_mint_burn(params, substep, state_history, prev_state, policy_input, **kwargs):
    """
    Function to update the utilities after apr
    """
    # get state variables
    updated_agents = prev_state['agents'].copy()

    # get policy input
    agents_staking_minting_rewards = policy_input['agents_staking_minting_rewards']

    # update logic
    if agents_staking_minting_rewards != {}:
        for agent in updated_agents:
            updated_agents[agent]['a_tokens_staking_minting_rewards'] = agents_staking_minting_rewards[agent]
            updated_agents[agent]['a_tokens_staking_minting_rewards_cum'] += agents_staking_minting_rewards[agent]
            updated_agents[agent]['a_tokens'] += (agents_staking_minting_rewards[agent])

    return ('agents', updated_agents)

def update_token_economy_after_staking_mint_burn(params, substep, state_history, prev_state, policy_input, **kwargs):
    """
    Function to update the token economy after tokens burned by means of the burning utility.

    State update function.

    Returns: 
        A tuple ('token_economy', updated_token_economy), where updated_token_economy 
        is a dict that reports respective updated amounts of tokens, tokens
        burned in the current period, and cumulatively at the token economy level.

    """
    # get parameters

    # get state variables
    updated_token_economy = prev_state['token_economy'].copy()
    liquidity_pool = prev_state['liquidity_pool'].copy()

    # get policy input
    new_tokens_minted = policy_input['new_tokens_minted']

    # update logic
    updated_token_economy['te_minted_tokens'] = new_tokens_minted
    updated_token_economy['te_minted_tokens_cum'] += new_tokens_minted
    updated_token_economy['te_minted_tokens_usd'] = new_tokens_minted  * liquidity_pool['lp_token_price']

    return ('token_economy', updated_token_economy)



