"""Liquidity pool initialisation and updating after transactions.

Contains policy functions (PF) and state update functions (SUF).


Functions:
    initialize_liquidity_pool (PF): Function to initialize the liquidity pool in 
        the first timestep.

    liquidity_pool_tx1_after_adoption (PF): Function to calculate the liquidity pool 
        after the adoption buys. 

    liquidity_pool_tx2_after_vesting_sell (PF): Function to calculate the liquidity 
        pool after the vesting sell.

    liquidity_pool_tx3_after_liquidity_addition (PF): Function to calculate the 
        liquidity pool after liquidity addition.

    liquidity_pool_tx4_after_buyback (PF): Function to calculate the liquidity pool
        after buyback.

    update_lp_after_lp_seeding (SUF): Function to update the agents based on the 
        changes in business funds to seed the liquidity pool.

    update_agents_tx1_after_adoption (SUF): Function to update the agents after the
        adoption buys.

    update_agents_tx2_after_vesting_sell (SUF): Function to update the agents after
        the vesting sell.
    
    update_liquidity_pool_after_transaction (SUF): Update the liquidity pool after
        adoption buys, vesting sell, liquidity addition or buyback.

"""


import numpy as np

from Model.parts.utils import *

# POLICY FUNCTIONS
def liquidity_pool_tx1_after_adoption(params, substep, state_history, prev_state, **kwargs):
    """
    Function to calculate the liquidity pool after the adoption buys. 

    Policy function.
    
    Returns:
        A dict which provides amount of native protocol tokens in LP, 
        amount of USDC in LP, value of the constant product invariant,
        token price, and transaction flag.

    Attributes:
        token_lp_weight (float): Weight of the token in the liquidity pool.
        usdc_lp_weight (float): Weight of USDC in the liquidity pool. 

    Raises:
        AssertionError: Constant product has changed after the adoption buys.
    
    """

    # parameters
    token_lp_weight = 0.5
    usdc_lp_weight = 0.5

    # state variables
    liquidity_pool = prev_state['liquidity_pool'].copy()
    user_adoption = prev_state['user_adoption'].copy()
    token_buys = user_adoption['ua_token_buys']

    # policy variables
    lp_tokens = liquidity_pool['lp_tokens']
    lp_usdc = liquidity_pool['lp_usdc']
    constant_product = liquidity_pool['lp_constant_product']
    token_price = liquidity_pool['lp_token_price']

    # policy logic
    # calculate the liquidity pool after the adoption buys
    lp_tokens = lp_tokens - lp_tokens * (1 - (lp_usdc / (lp_usdc + token_buys))**(usdc_lp_weight/token_lp_weight))
    lp_usdc = lp_usdc + token_buys

    token_price = lp_usdc / lp_tokens

    error_message = (
    f'The constant product is not allowed to change after adoption buys! '
    f'Old constant product: {constant_product} New constant product: {lp_usdc * lp_tokens}')
    
    np.testing.assert_allclose(constant_product, lp_usdc * lp_tokens, rtol=0.001, err_msg=error_message)

    return {'lp_tokens': lp_tokens, 'lp_usdc': lp_usdc, 'lp_constant_product': constant_product, 'lp_token_price': token_price, 'tx': 1}

def liquidity_pool_tx2_after_vesting_sell(params, substep, state_history, prev_state, **kwargs):
    """
    Function to calculate the liquidity pool after the vesting sell.

    Policy function.

    Includes selling from airdrops and incentivisation allocations.
    
    Returns:
        A dict which provides amount of native protocol tokens in LP, 
        amount of USDC in LP, value of the constant product invariant,
        token price, mapping for agents selling from holding and 
        transaction flag.

    Attributes:
        token_lp_weight (float): Weight of the token in the liquidity pool.
        usdc_lp_weight (float): Weight of USDC in the liquidity pool. 

    """

    # parameters
    token_lp_weight = 0.5
    usdc_lp_weight = 0.5

    # state variables
    liquidity_pool = prev_state['liquidity_pool'].copy()
    agents = prev_state['agents'].copy()
    token_economy = prev_state['token_economy'].copy()

    # policy variables
    lp_tokens = liquidity_pool['lp_tokens']
    lp_usdc = liquidity_pool['lp_usdc']
    constant_product = liquidity_pool['lp_constant_product']
    token_price = liquidity_pool['lp_token_price']
    selling_allocation = token_economy['te_selling_allocation']

    # policy logic
    # get amount of tokens to be sold by agents from vesting + airdrops + incentivisation
    tokens_to_sell = 0
    a_selling_tokens_sum = 0
    a_selling_from_holding_tokens_sum = 0
    for agent in agents:
        # selling from vesting + airdrops + incentivisation allocations
        tokens_to_sell += agents[agent]['a_selling_tokens'] + agents[agent]['a_selling_from_holding_tokens']
        a_selling_tokens_sum += agents[agent]['a_selling_tokens']
        a_selling_from_holding_tokens_sum += agents[agent]['a_selling_from_holding_tokens']

    # consistency check for the amount of tokens to be sold being equivalent to meta bucket selling allocation
    error_message = (
    f'The amount of tokens to be sold {tokens_to_sell} '
    f'is not equal to the meta bucket selling allocation {selling_allocation}!')
    
    np.testing.assert_allclose(tokens_to_sell, selling_allocation, rtol=0.001, err_msg=error_message)

    # calculate the liquidity pool after the vesting sells
    lp_usdc = lp_usdc - lp_usdc * (1 - (lp_tokens / (lp_tokens + tokens_to_sell))**(token_lp_weight/usdc_lp_weight))
    lp_tokens = lp_tokens + tokens_to_sell


    token_price = lp_usdc / lp_tokens

    error_message = (
    f'The constant product is not allowed to change after adoption buys! '
    f'Old constant product: {constant_product} New constant product: {lp_usdc * lp_tokens}')
    
    np.testing.assert_allclose(constant_product, lp_usdc * lp_tokens, rtol=0.001, err_msg=error_message)
        
    return {'lp_tokens': lp_tokens, 'lp_usdc': lp_usdc, 'lp_constant_product': constant_product, 'lp_token_price': token_price, 'tx': 2}

def liquidity_pool_tx3_after_liquidity_addition(params, substep, state_history, prev_state, **kwargs):
    """
    Function to calculate the liquidity pool after liquidity addition.

    Policy function.
    
    Returns:
        A dict which provides amount of native protocol tokens in LP, 
        amount of USDC in LP, value of the constant product invariant,
        token price, and transaction flag.
    """

    # parameters

    # state variables
    liquidity_pool = prev_state['liquidity_pool'].copy()
    agents = prev_state['agents'].copy()

    # policy variables
    lp_tokens = liquidity_pool['lp_tokens']
    lp_usdc = liquidity_pool['lp_usdc']
    constant_product = liquidity_pool['lp_constant_product']
    token_price = liquidity_pool['lp_token_price']

    # policy logic
    # get amount of tokens to be used for liquidity mining
    tokens_for_liquidity = 0
    for agent in agents:
        tokens_for_liquidity += (agents[agent]['a_tokens_liquidity_mining'] - agents[agent]['a_tokens_liquidity_mining_remove'])

    # calculate the liquidity pool after the vesting sells
    lp_usdc = lp_usdc + tokens_for_liquidity * token_price
    lp_tokens = lp_tokens + tokens_for_liquidity

    # ensure that token price can never be negative
    token_price = max(lp_usdc / lp_tokens, 0)
    constant_product = lp_usdc * lp_tokens
        
    return {'lp_tokens': lp_tokens, 'lp_usdc': lp_usdc, 'lp_constant_product': constant_product, 'lp_token_price': token_price, 'tx': 3}

def liquidity_pool_tx4_after_buyback(params, substep, state_history, prev_state, **kwargs):
    """
    Function to calculate the liquidity pool after buyback.

    Policy function.
    
    Returns:
        A dict which provides amount of native protocol tokens in LP, 
        amount of USDC in LP, value of the constant product invariant,
        token price, and transaction flag.

    Attributes:
        token_lp_weight (float): Weight of the token in the liquidity pool.
        usdc_lp_weight (float): Weight of USDC in the liquidity pool. 

    Raises:
        AssertionError: Constant product has changed after the adoption buys.

    """

    # parameters
    token_lp_weight = 0.5
    usdc_lp_weight = 0.5

    # state variables
    liquidity_pool = prev_state['liquidity_pool'].copy()
    business_assumptions = prev_state['business_assumptions'].copy()

    # policy variables
    lp_tokens_init = liquidity_pool['lp_tokens']
    lp_usdc_init = liquidity_pool['lp_usdc']
    constant_product_init = liquidity_pool['lp_constant_product']
    buybacks_usd = business_assumptions['ba_buybacks_usd']
    business_buybacks_usd = business_assumptions['ba_business_buybacks_usd']

    # policy logic
    # calculate the business buyback separately from the general buybacks if it is negative, which implies a token sale by the business
    if business_buybacks_usd < 0:
        lp_tokens = lp_tokens_init - lp_tokens_init * (1 - (lp_usdc_init / (lp_usdc_init + business_buybacks_usd))**(usdc_lp_weight/token_lp_weight))
        lp_usdc = lp_usdc_init + business_buybacks_usd
        token_price = lp_usdc / lp_tokens
        sold_business_tokens = lp_tokens - lp_tokens_init
    else:
        sold_business_tokens = 0
        lp_tokens = lp_tokens_init
        lp_usdc = lp_usdc_init

    # calculate the liquidity pool after buyback
    lp_tokens = lp_tokens - lp_tokens * (1 - (lp_usdc / (lp_usdc + buybacks_usd))**(usdc_lp_weight/token_lp_weight))
    lp_usdc = lp_usdc + buybacks_usd

    token_price = lp_usdc / lp_tokens
    
    error_message = (
    f'The constant product is not allowed to change after adoption buys! '
    f'Old constant product: {constant_product_init} New constant product: {lp_usdc * lp_tokens}')
    
    np.testing.assert_allclose(constant_product_init, lp_usdc * lp_tokens, rtol=0.001, err_msg=error_message)
    
    return {'lp_tokens': lp_tokens, 'lp_usdc': lp_usdc, 'lp_constant_product': constant_product_init, 'lp_token_price': token_price, 'tx': 4, 'sold_business_tokens': sold_business_tokens}


# STATE UPDATE FUNCTIONS
def update_agents_tx1_after_adoption(params, substep, state_history, prev_state, policy_input, **kwargs):
    """
    Function to update the agents after the adoption buys. 

    State update function.

    Tokens bought are distributed to the agents of 'market_investors' type.

    Returns:
        Tuple ('agents', updated_agents), where updated_agents provide the information
        on how the token amount changed for the agents of the 'market_investors' type.

    Raises:
        ValueError: No market investors found; Request to add at least one.

    """
    # state variables
    liquidity_pool = prev_state['liquidity_pool'].copy()
    updated_agents = prev_state['agents'].copy()


    # get policy inputs
    new_lp_tokens = policy_input['lp_tokens']

    # update variables
    old_lp_tokens = liquidity_pool['lp_tokens']

    # update logic
    bought_tokens = old_lp_tokens - new_lp_tokens

    if bought_tokens > 0:
        # distribute the bought tokens to the market_investors agents
        market_investors = sum([1 for agent in updated_agents if (updated_agents[agent]['a_type'] == 'market_investors')])
        if market_investors == 0:
            raise ValueError("No market investors found. Please add at least one market investor in the stakeholder agents if you plan to buy tokens from the open market dex liquidity with agents.")
        
        for agent in updated_agents:
            if updated_agents[agent]['a_type'] == 'market_investors':
                
                bought_tokens_per_market_investor = bought_tokens / market_investors

                updated_agents[agent]['a_tokens'] += bought_tokens_per_market_investor

    return ('agents', updated_agents)

def update_liquidity_pool_after_transaction(params, substep, state_history, prev_state, policy_input, **kwargs):
    """
    Update the liquidity pool after adoption buys, vesting sell, liquidity addition
    or buyback.

    State update function.

    Note: The type of transaction that brings the need for an update to the 
    liquidity pool is determined by the transaction flag 'tx'.

    Returns:
        Tuple ('liquidity_pool', updated_liquidity_pool) with updated_liquidity_pool
            being a dict that provides information on changed attributes of the
            liquidity pool.


    """
    # parameters
    initial_token_price = params['initial_token_price']

    # state variables
    updated_liquidity_pool = prev_state['liquidity_pool']
    current_month = prev_state['timestep']

    # get policy inputs
    lp_tokens = policy_input['lp_tokens']
    lp_usdc = policy_input['lp_usdc']
    constant_product = policy_input['lp_constant_product']
    token_price = policy_input['lp_token_price']
    tx = policy_input['tx']
    sold_business_tokens = policy_input['sold_business_tokens'] if tx == 4 else 0
    
    # prepare volatility calculation
    if policy_input['tx'] == 1:
        updated_liquidity_pool['lp_token_price_max'] = token_price
        updated_liquidity_pool['lp_token_price_min'] = token_price
    elif policy_input['tx'] in [2, 3, 4]:
        updated_liquidity_pool['lp_token_price_max'] = np.max([updated_liquidity_pool['lp_token_price_max'], token_price, [initial_token_price if current_month == 1 else 0][0]])
        updated_liquidity_pool['lp_token_price_min'] = np.min([updated_liquidity_pool['lp_token_price_min'], token_price, [initial_token_price if current_month == 1 else 1e20][0]])

    # update logic
    updated_liquidity_pool['lp_tokens'] = lp_tokens
    updated_liquidity_pool['lp_usdc'] = lp_usdc
    updated_liquidity_pool['lp_constant_product'] = constant_product
    updated_liquidity_pool['lp_token_price'] = token_price
    updated_liquidity_pool['lp_valuation'] = lp_usdc + lp_tokens * token_price
    updated_liquidity_pool['lp_volatility'] = ((updated_liquidity_pool['lp_token_price_max'] - updated_liquidity_pool['lp_token_price_min'])
                                            / updated_liquidity_pool['lp_token_price_max'] * 100)

    #Special 2 variables
    if tx == 1:
        updated_liquidity_pool['lp_tokens_after_adoption'] = lp_tokens
    elif tx == 3:
        updated_liquidity_pool['lp_tokens_after_liquidity_addition'] = lp_tokens
    elif tx == 4:
        updated_liquidity_pool['lp_tokens_after_buyback'] = lp_tokens
        updated_liquidity_pool['lp_sold_business_tokens'] = sold_business_tokens
    
    return ('liquidity_pool', updated_liquidity_pool)
