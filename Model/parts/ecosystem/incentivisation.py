"""Calculation and processing of ecosystem incentivisation.

Contains policy functions (PF) and state update functions (SUF).


Functions:
    incentivisation (PF): Policy function to incentivise the ecosystem.

    update_agents_after_incentivisation (SUF): Function to update the 
        vested tokens for each investor based on some criteria.

    update_token_economy_after_incentivisation (SUF): Function to update
        the token economy after incentivisation.


"""
from Model.parts.utils import calculate_buyback_share_tokens

# POLICY FUNCTIONS
def incentivisation(params, substep, state_history, prev_state, **kwargs):
    """
    Policy function to incentivise the ecosystem.

    The possible sources of incentivisation include minting and protocol bucket
    vesting.

    Returns:
        A dict which provides values for tokens intended for incentivisation for
        the possible sources: minting and protocol bucket vesting.

    """
    # get parameters
    incentivisation_payout_source = params['incentivisation_payout_source']

    # get state variables
    agents = prev_state['agents']

    # policy logic
    # Incentivisation through protocol bucket vesting
    for agent in agents:
        if agents[agent]['a_type'] == 'protocol_bucket' and incentivisation_payout_source.lower() in agents[agent]['a_name'].lower():
            vested_incentivisation_tokens = agents[agent]['a_tokens']

    return {'vested_incentivisation_tokens': vested_incentivisation_tokens}

def incentivisation_revenue_share_buyback(params, substep, state_history, prev_state, **kwargs):
    """
    Policy function to calculate the incentivisation token buybacks from the revenue share
    """
    # get state variables
    liquidity_pool = prev_state['liquidity_pool'].copy()
    business_assumptions = prev_state['business_assumptions'].copy()

    # rewards state variables
    lp_tokens_after_liquidity_addition  =  liquidity_pool['lp_tokens_after_liquidity_addition']
    lp_tokens_after_buyback = liquidity_pool['lp_tokens'] # Tokens after trx 4 (buybacks)
    ba_buyback_from_revenue_share_incentivisation_usd = business_assumptions['ba_buyback_from_revenue_share_incentivisation_usd']
    ba_buybacks_usd =prev_state['business_assumptions']['ba_buybacks_usd']

    # policy logic
    buyback_share_tokens = calculate_buyback_share_tokens(ba_buyback_from_revenue_share_incentivisation_usd, ba_buybacks_usd, lp_tokens_after_liquidity_addition, lp_tokens_after_buyback)

    return {'incentivisation_buyback': buyback_share_tokens}


# STATE UPDATE FUNCTIONS
def update_agents_after_incentivisation(params, substep, state_history, prev_state, policy_input, **kwargs):
    """
    Function to update the vested tokens for each investor based on some criteria.

    State update function.

    The amount of tokens in protocol buckets get decreased due to incentivisation.
    The amount of tokens that the incentivisation receivers will receive, will
    increase by their fraction of the incentivisation amount.

    Returns: 
        Tuple ('agents', updated_agents), where updated_agents is a dict that maps
        the agent types (protocol buckets or incentivisation receivers) onto their
        respective values after incentivisation.
    """
    # get parameters
    incentivisation_payout_source = params['incentivisation_payout_source']

    # get state variables
    updated_agents = prev_state['agents']

    # get policy input
    vested_incentivisation_tokens = policy_input['vested_incentivisation_tokens']

    # update logic
    if vested_incentivisation_tokens > 0:
        # subtract vested incentivisation tokens from protocol bucket
        for agent in updated_agents:
            if updated_agents[agent]['a_type'] == 'protocol_bucket' and incentivisation_payout_source.lower() in updated_agents[agent]['a_name'].lower():
                updated_agents[agent]['a_tokens'] -= vested_incentivisation_tokens

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
    Function to update the token economy after incentivisation.

    State update function.

    Returns: 
        Tuple ('token_economy', updated_token_economy), where updated_agents is a dict 
        that provides amounts of tokens that were vested / minted.
    """
    # get parameters

    # get state variables
    updated_token_economy = prev_state['token_economy'].copy()

    # get policy input
    vested_incentivisation_tokens = policy_input['vested_incentivisation_tokens']

    # update logic
    incentivisation_tokens = vested_incentivisation_tokens
    updated_token_economy['te_incentivised_tokens'] = incentivisation_tokens
    updated_token_economy['te_incentivised_tokens_cum'] += incentivisation_tokens

    return ('token_economy', updated_token_economy)


def update_agents_after_incentivisation_revenue_share_buyback(params, substep, state_history, prev_state, policy_input, **kwargs):
    """
    Function to update incentivisation agent token buybacks from the revenue share
    """
    # get parameters

    # get state variables
    updated_agents = prev_state['agents'].copy()

    # get policy input
    incentivisation_buyback = policy_input['incentivisation_buyback']

    # update logic
    if incentivisation_buyback != 0:
        for agent in updated_agents:
            # transfer incentivisation bought back tokens to incentivisation_receiver agents
            if updated_agents[agent]['a_name'].lower() == 'incentivisation_receivers':
                updated_agents[agent]['a_tokens'] += incentivisation_buyback
                updated_agents[agent]['a_tokens_incentivised'] += incentivisation_buyback
                updated_agents[agent]['a_tokens_incentivised_cum'] += incentivisation_buyback

    return ('agents', updated_agents)


def update_business_assumptions_after_incentivisation_revenue_share_buyback(params, substep, state_history, prev_state, policy_input, **kwargs):
    """
    Function to update business assumptions after incentivisation revenue share buyback
    """
    # get state variables
    updated_business_assumptions = prev_state['business_assumptions'].copy()

    # get policy input
    agent_incentives = policy_input['incentivisation_buyback']

    # update logic
    updated_business_assumptions['ba_buyback_from_revenue_share_incentives'] = agent_incentives

    return ('business_assumptions', updated_business_assumptions)

def update_token_economy_after_incentivisation_revenue_share(params, substep, state_history, prev_state, policy_input, **kwargs):
    """
    Function to update the token economy after incentivisation from revenue share.

    State update function.

    Returns: 
        Tuple ('token_economy', updated_token_economy), where updated_agents is a dict 
        that provides amounts of tokens that were distributed as incentivisation from
        revenue share.
    """
    # get parameters

    # get state variables
    updated_token_economy = prev_state['token_economy'].copy()

    # get policy input
    agent_incentives = policy_input['incentivisation_buyback']

    # update logic
    updated_token_economy['te_incentivised_tokens'] += agent_incentives
    updated_token_economy['te_incentivised_tokens_cum'] += agent_incentives

    return ('token_economy', updated_token_economy)