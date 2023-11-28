"""Calculate and process airdrops.

Contains policy functions (PF) and state update functions (SUF) 
relevant for behaviour of each type of agent and for meta bucket allocations.


Functions:
    airdrops (PF): Policy function to calculate airdrop amount for current period.

    update_agents_after_airdrops (SUF): Function to update information on airdrop 
        receiving agent after airdrops distribution.

    update_token_economy_after_airdrops (SUF): Function to update the token economy 
        after airdrops distribution.

"""

import pandas as pd

# POLICY FUNCTIONS
def airdrops(params, substep, state_history, prev_state, **kwargs):
    """
    Policy function to calculate airdrop amount for current period.

    Airdrop amounts are provided as percentages of the airdrop allocation for
    the predefined airdrop dates. The amounts of airdropped tokens for each 
    date are calculated based on the total token supply, airdrop allocation 
    percentage and the airdrop amount. 

    Returns: 
        A dict where key 'te_airdrop_tokens' gets assigned a nonnegative value. 
    """
    # get parameters
    total_token_supply = params['initial_total_supply']
    airdrop_allocation = params['airdrop_allocation']
    airdrop_date1 = pd.to_datetime(params['airdrop_date1'], format='%d.%m.%Y')
    airdrop_date2 = pd.to_datetime(params['airdrop_date2'], format='%d.%m.%Y')
    airdrop_date3 = pd.to_datetime(params['airdrop_date3'], format='%d.%m.%Y')
    airdrop_amount1 = params['airdrop_amount1']
    airdrop_amount2 = params['airdrop_amount2']
    airdrop_amount3 = params['airdrop_amount3']

    # get state variables
    current_date = pd.to_datetime(prev_state['date'])

    # policy logic
    # calculate airdrop amounts
    airdrop_tokens = 0
    # check if current month is airdrop month
    if current_date <= airdrop_date1 and current_date+pd.DateOffset(months=1) > airdrop_date1:
        airdrop_tokens += total_token_supply * airdrop_allocation/100 * airdrop_amount1/100
    if current_date <= airdrop_date2 and current_date+pd.DateOffset(months=1) > airdrop_date2:
        airdrop_tokens += total_token_supply * airdrop_allocation/100 * airdrop_amount2/100
    if current_date <= airdrop_date3 and current_date+pd.DateOffset(months=1) > airdrop_date3:
        airdrop_tokens += total_token_supply * airdrop_allocation/100 * airdrop_amount3/100

    # ensuring that the number of airdrop tokens is never negative
    return {'te_airdrop_tokens': max(airdrop_tokens, 0)}

# STATE UPDATE FUNCTIONS
def update_agents_after_airdrops(params, substep, state_history, prev_state, policy_input, **kwargs):
    """
    Function to update information on airdrop receiving agent after airdrops distribution. 
    
    State update function.

    Returns:
        Tuple ('agents', updated_agents), where updated_agents holds information on the agents
        who are labeled as airdrop receivers.

    Raises:
        ValueError: No airdrop receivers found; Request to add at least one.

    """
    # get parameters

    # get state variables
    updated_agents = prev_state['agents']

    # get policy input
    airdrop_tokens = policy_input['te_airdrop_tokens']

    # update logic
    # add airdropped tokens to airdrop receivers stakeholder group
    airdrop_receivers = sum([1 for agent in updated_agents if (updated_agents[agent]['a_type'] == 'airdrop_receivers')])
    if airdrop_tokens > 0:
        
        if airdrop_receivers == 0:
            raise ValueError("No airdrop receivers found. Please add at least one airdrop receiver in the stakeholder agents if you plan to airdrop tokens.")
        
        for agent in updated_agents:
            if updated_agents[agent]['a_type'] == 'airdrop_receivers':
                
                airdrop_per_airdrop_receiver = airdrop_tokens / airdrop_receivers

                updated_agents[agent]['a_tokens'] += airdrop_per_airdrop_receiver
                updated_agents[agent]['a_tokens_airdropped'] = airdrop_per_airdrop_receiver
                updated_agents[agent]['a_tokens_airdropped_cum'] += airdrop_per_airdrop_receiver

    return ('agents', updated_agents)

def update_token_economy_after_airdrops(params, substep, state_history, prev_state, policy_input, **kwargs):
    """
    Function to update the token economy after airdrops distribution.
    
    State update function.

    Returns:
        Tuple ('token_economy', updated_token_economy), where updated_token_economy 
        is a dict which holds information on the tokens distributed as airdrops
        in the current period (token amount, cumulative amount, USD value).

    """
    # get parameters

    # get state variables
    updated_token_economy = prev_state['token_economy'].copy()
    liquidity_pool = prev_state['liquidity_pool']

    # get policy input
    airdrop_tokens = policy_input['te_airdrop_tokens']

    # update logic
    updated_token_economy['te_airdrop_tokens'] = airdrop_tokens
    updated_token_economy['te_airdrop_tokens_cum'] += airdrop_tokens
    updated_token_economy['te_airdrop_tokens_usd'] = airdrop_tokens * liquidity_pool['lp_token_price']

    return ('token_economy', updated_token_economy)