from Model.parts.utils import calculate_buyback_share_tokens

# POLICY FUNCTIONS
def business_buyback(params, substep, state_history, prev_state, **kwargs):
    """
    Policy function to calculate the buybacks of the business
    """
    # get state variables
    liquidity_pool = prev_state['liquidity_pool'].copy()
    business_assumptions = prev_state['business_assumptions'].copy()

    # rewards state variables
    lp_tokens_after_liquidity_addition  =  liquidity_pool['lp_tokens_after_liquidity_addition']
    lp_tokens_after_buyback = liquidity_pool['lp_tokens'] # Tokens after trx 4 (buybacks)
    ba_business_buybacks_usd = business_assumptions['ba_business_buybacks_usd']
    ba_buybacks_usd =prev_state['business_assumptions']['ba_buybacks_usd']

    # policy logic
    if ba_business_buybacks_usd >= 0:
        buyback_share_tokens = calculate_buyback_share_tokens(ba_business_buybacks_usd, ba_buybacks_usd, lp_tokens_after_liquidity_addition, lp_tokens_after_buyback)
    else:
        buyback_share_tokens = -liquidity_pool['lp_sold_business_tokens']

    return {'business_buyback': buyback_share_tokens}



# STATE UPDATE FUNCTIONS
def update_agents_after_business_buyback(params, substep, state_history, prev_state, policy_input, **kwargs):
    """
    Function to update buyback_bucket agent after business buybacks
    """
    # get parameters
    buyback_bucket = params['buyback_bucket']

    # get state variables
    updated_agents = prev_state['agents'].copy()

    # get policy input
    business_buyback = policy_input['business_buyback']

    # update logic
    if business_buyback != 0:
        for agent in updated_agents:
            # transfer business bought back tokens to destination
            if updated_agents[agent]['a_name'].lower() in buyback_bucket.lower():
                updated_agents[agent]['a_tokens'] += business_buyback

    return ('agents', updated_agents)
