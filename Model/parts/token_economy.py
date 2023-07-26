# POLICY FUNCTIONS
def token_economy_metrics(params, substep, state_history, prev_state, **kwargs):
    """
    Calculate the initial token economy metrics, such as MC, FDV MC, circ. supply, and tokens locked.
    """

    liquidity_pool = prev_state['liquidity_pool']
    agents = prev_state['agents']
    total_token_supply = params['initial_total_supply']

    circulating_tokens = 0
    locked_apr_tokens = 0
    locked_buyback_tokens = 0

    for stakeholder in agents:
        circulating_tokens += agents[stakeholder]['tokens']
        locked_apr_tokens += agents[stakeholder]['tokens_apr_locked']
        locked_buyback_tokens += agents[stakeholder]['tokens_buyback_locked']
    
    MC = liquidity_pool['token_price'] * circulating_tokens
    FDV_MC = liquidity_pool['token_price'] * total_token_supply

    return {'total_token_supply': total_token_supply, 'circulating_supply': circulating_tokens, 'MC': MC, 'FDV_MC': FDV_MC, 'tokens_apr_locked': locked_apr_tokens, 'tokens_buyback_locked': locked_buyback_tokens}

# STATE UPDATE FUNCTIONS
def update_token_economy(params, substep, state_history, prev_state, policy_input, **kwargs):
    """
    Function to update the agents based on the changes in business funds to seed the liquidity pool.
    """
    total_token_supply = policy_input['total_token_supply']
    circulating_supply = policy_input['circulating_supply']
    MC = policy_input['MC']
    FDV_MC = policy_input['FDV_MC']
    tokens_apr_locked = policy_input['tokens_apr_locked']
    tokens_buyback_locked = policy_input['tokens_buyback_locked']

    updated_token_economy = {
        'total_supply' : total_token_supply,
        'circulating_supply' : circulating_supply,
        'MC' : MC,
        'FDV_MC' : FDV_MC,
        'tokens_apr_locked' : tokens_apr_locked,
        'tokens_buyback_locked' : tokens_buyback_locked
    }

    return ('token_economy', updated_token_economy)