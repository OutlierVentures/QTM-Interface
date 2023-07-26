# POLICIY FUNCTIONS
def incentivisation(params, substep, state_history, prev_state, **kwargs):
    """
    Policy function to incentivise the ecosystem
    """
    
    total_token_supply = params['initial_total_supply']

    # Incentivisation through protocol bucket vesting
    incentivisation_payout_source = params['incentivisation_payout_source']
    agents = prev_state['agents']
    for agent in agents:
        if agents[agent]['type'] == 'protocol_bucket' and incentivisation_payout_source.lower() in agents[agent]['name'].lower():
            vested_incentivisation_tokens = agents[agent]['tokens']

    # Incentivisation through minting
    mint_incentivisation = params['mint_incentivisation']

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

    for agent in updated_agents:
        if updated_agents[agent]['type'] == 'protocol_bucket' and incentivisation_payout_source.lower() in updated_agents[agent]['name'].lower():
            updated_agents[agent]['tokens'] = updated_agents[agent]['tokens'] - vested_incentivisation_tokens


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

    incentivisation_tokens = vested_incentivisation_tokens + minted_incentivisation_tokens
    updated_token_economy['minted_tokens'] = minted_incentivisation_tokens
    updated_token_economy['incentivised_tokens'] = incentivisation_tokens
    updated_token_economy['incentivised_tokens_usd'] = incentivisation_tokens * liquidity_pool['token_price']
    updated_token_economy['incentivised_tokens_cum'] += incentivisation_tokens

    return ('token_economy', updated_token_economy)