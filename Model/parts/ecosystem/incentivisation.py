# POLICIY FUNCTIONS
def incentivisation(params, substep, state_history, prev_state, **kwargs):
    """
    Policy function to incentivise the ecosystem
    """
    # get parameters
    total_token_supply = params['initial_total_supply']
    incentivisation_payout_source = params['incentivisation_payout_source']
    mint_incentivisation = params['mint_incentivisation']

    # get state variables
    agents = prev_state['agents']

    # policy logic
    # Incentivisation through protocol bucket vesting
    for agent in agents:
        if agents[agent]['a_type'] == 'protocol_bucket' and incentivisation_payout_source.lower() in agents[agent]['a_name'].lower():
            vested_incentivisation_tokens = agents[agent]['a_tokens']

    # Incentivisation through minting
    if incentivisation_payout_source == 'Minting':
        minted_incentivisation_tokens = total_token_supply * mint_incentivisation/100
    else:
        minted_incentivisation_tokens = 0

    return {'vested_incentivisation_tokens': vested_incentivisation_tokens, 'minted_incentivisation_tokens': minted_incentivisation_tokens}

# STATE UPDATE FUNCTIONS
def update_agents_after_incentivisation(params, substep, state_history, prev_state, policy_input, **kwargs):
    """
    Function to update the vested tokens for each investor based on some criteria
    """
    # get parameters
    incentivisation_payout_source = params['incentivisation_payout_source']

    # get state variables
    updated_agents = prev_state['agents']

    # get policy input
    vested_incentivisation_tokens = policy_input['vested_incentivisation_tokens']

    # update logic
    # subtract vested incentivisation tokens from protocol bucket
    for agent in updated_agents:
        if updated_agents[agent]['a_type'] == 'protocol_bucket' and incentivisation_payout_source.lower() in updated_agents[agent]['a_name'].lower():
            updated_agents[agent]['a_tokens'] = updated_agents[agent]['a_tokens'] - vested_incentivisation_tokens

    # add vested incentivisation tokens to market participants
    # count amount of market_investors and early_investors in updated_agents
    incentivisation_receivers = sum([1 for agent in updated_agents if (updated_agents[agent]['a_type'] == 'incentivisation_receivers')])
    for agent in updated_agents:
        if updated_agents[agent]['a_type'] == 'incentivisation_receivers':

            incentivisation_per_incentivisation_receiver = vested_incentivisation_tokens / incentivisation_receivers

            updated_agents[agent]['a_tokens'] += incentivisation_per_incentivisation_receiver
            updated_agents[agent]['a_tokens_incentivised'] = incentivisation_per_incentivisation_receiver
            updated_agents[agent]['a_tokens_incentivised_cum'] += incentivisation_per_incentivisation_receiver

    return ('agents', updated_agents)

def update_token_economy_after_incentivisation(params, substep, state_history, prev_state, policy_input, **kwargs):
    """
    Function to update the token economy after incentivisation
    """
    # get parameters

    # get state variables
    updated_token_economy = prev_state['token_economy'].copy()
    liquidity_pool = prev_state['liquidity_pool']

    # get policy input
    vested_incentivisation_tokens = policy_input['vested_incentivisation_tokens']
    minted_incentivisation_tokens = policy_input['minted_incentivisation_tokens']

    # update logic
    incentivisation_tokens = vested_incentivisation_tokens + minted_incentivisation_tokens
    updated_token_economy['minted_tokens'] = minted_incentivisation_tokens
    updated_token_economy['minted_tokens_cum'] += minted_incentivisation_tokens
    updated_token_economy['minted_tokens_usd'] = minted_incentivisation_tokens  * liquidity_pool['token_price']
    updated_token_economy['incentivised_tokens'] = incentivisation_tokens
    updated_token_economy['incentivised_tokens_usd'] = incentivisation_tokens * liquidity_pool['token_price']
    updated_token_economy['incentivised_tokens_cum'] += incentivisation_tokens

    return ('token_economy', updated_token_economy)