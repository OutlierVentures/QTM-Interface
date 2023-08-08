import numpy as np

from parts.utils import *

# POLICY FUNCTIONS
def initialize_liquidity_pool(params, substep, state_history, prev_state, **kwargs):
    """
    Function to initialize the liquidity pool in the first timestep
    """

    # parameters
    required_usdc = params['initial_required_usdc']
    required_tokens = params['initial_lp_token_allocation']

    # state variables
    current_month = prev_state['timestep']
    liquidity_pool = prev_state['liquidity_pool']

    if current_month == 1:
        print('Initializing the liquidity pool...')
        constant_product = required_usdc * required_tokens
        token_price = required_usdc / required_tokens

        # initialize the liquidity pool from the system parameters
        liquidity_pool['tokens'] = required_tokens
        liquidity_pool['usdc'] = required_usdc
        liquidity_pool['constant_product'] = constant_product
        liquidity_pool['token_price'] = token_price

        # check if required funds are available from funds raised
        sum_of_raised_capital = calculate_raised_capital(params)

        if required_usdc > sum_of_raised_capital:
            raise ValueError('The required funds to seed the DEX liquidity are '+str(required_usdc)+' and higher than the sum of raised capital '+str(sum_of_raised_capital)+'!')
        
        return {'liquidity_pool': liquidity_pool}
    else:
        return {'liquidity_pool': prev_state['liquidity_pool']}

def liquidity_pool_tx1_after_adoption(params, substep, state_history, prev_state, **kwargs):
    """
    Function to calculate the liquidity pool after the adoption buys
    """

    # parameters
    token_lp_weight = 0.5
    usdc_lp_weight = 0.5

    # state variables
    current_month = prev_state['timestep']
    liquidity_pool = prev_state['liquidity_pool'].copy()
    user_adoption = prev_state['user_adoption'].copy()
    token_buys = user_adoption['token_buys']

    # policy variables
    lp_tokens = liquidity_pool['tokens']
    lp_usdc = liquidity_pool['usdc']
    constant_product = liquidity_pool['constant_product']
    token_price = liquidity_pool['token_price']

    # policy logic
    if current_month == 1:
        # calculate the liquidity pool after the adoption buys
        lp_tokens = lp_tokens - lp_tokens * (1 - (lp_usdc / (lp_usdc + token_buys))**(usdc_lp_weight/token_lp_weight))
        lp_usdc = lp_usdc + token_buys

        token_price = lp_usdc / lp_tokens

        error_message = 'The constant product is not allowed to change after adoption buys! Old constant product: '+str(constant_product)+' New constant product: '+str(lp_usdc * lp_tokens)
        np.testing.assert_allclose(constant_product, lp_usdc * lp_tokens, rtol=0.001, err_msg=error_message)
    
    else:
        pass
        
    return {'lp_tokens': lp_tokens, 'lp_usdc': lp_usdc, 'constant_product': constant_product, 'token_price': token_price, 'tx': 1}

def liquidity_pool_tx2_after_vesting_sell(params, substep, state_history, prev_state, **kwargs):
    """
    Function to calculate the liquidity pool after the vesting sell
    """

    # parameters
    token_lp_weight = 0.5
    usdc_lp_weight = 0.5

    # state variables
    current_month = prev_state['timestep']
    liquidity_pool = prev_state['liquidity_pool'].copy()
    agents = prev_state['agents'].copy()
    token_economy = prev_state['token_economy'].copy()

    # policy variables
    lp_tokens = liquidity_pool['tokens']
    lp_usdc = liquidity_pool['usdc']
    constant_product = liquidity_pool['constant_product']
    token_price = liquidity_pool['token_price']
    selling_allocation = token_economy['selling_allocation']

    # policy logic
    if current_month == 1:
        # get amount of tokens to be sold by agents from vesting + airdrops + incentivisation
        tokens_to_sell = 0
        for agent in agents:
            tokens_to_sell += agents[agent]['selling_tokens']
        
        # consistency check for the amount of tokens to be sold being equivalent to meta bucket selling allocation
        error_message = 'The amount of tokens to be sold '+str(tokens_to_sell)+' is not equal to the meta bucket selling allocation '+str(selling_allocation)+'!'
        np.testing.assert_allclose(tokens_to_sell, selling_allocation, rtol=0.001, err_msg=error_message)

        # calculate the liquidity pool after the vesting sells
        lp_usdc = lp_usdc - lp_usdc * (1 - (lp_tokens / (lp_tokens + tokens_to_sell))**(token_lp_weight/usdc_lp_weight))
        lp_tokens = lp_tokens + tokens_to_sell


        token_price = lp_usdc / lp_tokens

        error_message = 'The constant product is not allowed to change after adoption buys! Old constant product: '+str(constant_product)+' New constant product: '+str(lp_usdc * lp_tokens)
        np.testing.assert_allclose(constant_product, lp_usdc * lp_tokens, rtol=0.001, err_msg=error_message)
    
    else:
        pass
        
    return {'lp_tokens': lp_tokens, 'lp_usdc': lp_usdc, 'constant_product': constant_product, 'token_price': token_price, 'tx': 2}

def liquidity_pool_tx3_after_liquidity_addition(params, substep, state_history, prev_state, **kwargs):
    """
    Function to calculate the liquidity pool after liquidity addition
    """

    # parameters

    # state variables
    current_month = prev_state['timestep']
    liquidity_pool = prev_state['liquidity_pool'].copy()
    agents = prev_state['agents'].copy()

    # policy variables
    lp_tokens = liquidity_pool['tokens']
    lp_usdc = liquidity_pool['usdc']
    constant_product = liquidity_pool['constant_product']
    token_price = liquidity_pool['token_price']

    # policy logic
    if current_month == 1:
        # get amount of tokens to be used for liquidity mining
        tokens_for_liquidity = 0
        for agent in agents:
            tokens_for_liquidity += agents[agent]['tokens_liquidity_mining']

        # calculate the liquidity pool after the vesting sells
        lp_usdc = lp_usdc + tokens_for_liquidity * token_price
        lp_tokens = lp_tokens + tokens_for_liquidity


        token_price = lp_usdc / lp_tokens
        constant_product = lp_usdc * lp_tokens
    
    else:
        pass
        
    return {'lp_tokens': lp_tokens, 'lp_usdc': lp_usdc, 'constant_product': constant_product, 'token_price': token_price, 'tx': 3}

def liquidity_pool_tx4_after_buyback(params, substep, state_history, prev_state, **kwargs):
    """
    Function to calculate the liquidity pool after buyback
    """

    # parameters
    token_lp_weight = 0.5
    usdc_lp_weight = 0.5

    # state variables
    current_month = prev_state['timestep']
    liquidity_pool = prev_state['liquidity_pool'].copy()
    business_assumptions = prev_state['business_assumptions'].copy()
    utilities = prev_state['utilities'].copy()

    # policy variables
    lp_tokens = liquidity_pool['tokens']
    lp_usdc = liquidity_pool['usdc']
    constant_product = liquidity_pool['constant_product']
    token_price = liquidity_pool['token_price']
    buybacks_usd = business_assumptions['buybacks_usd']

    # policy logic
    if current_month == 1:
        # calculate the liquidity pool after buyback
        lp_tokens = lp_tokens - lp_tokens * (1 - (lp_usdc / (lp_usdc + buybacks_usd))**(usdc_lp_weight/token_lp_weight))
        lp_usdc = lp_usdc + buybacks_usd

        token_price = lp_usdc / lp_tokens
        
        error_message = 'The constant product is not allowed to change after adoption buys! Old constant product: '+str(constant_product)+' New constant product: '+str(lp_usdc * lp_tokens)
        np.testing.assert_allclose(constant_product, lp_usdc * lp_tokens, rtol=0.001, err_msg=error_message)
    
    else:
        pass
        
    return {'lp_tokens': lp_tokens, 'lp_usdc': lp_usdc, 'constant_product': constant_product, 'token_price': token_price, 'tx': 4}


# STATE UPDATE FUNCTIONS
def update_lp_after_lp_seeding(params, substep, state_history, prev_state, policy_input, **kwargs):
    """
    Function to update the agents based on the changes in business funds to seed the liquidity pool.
    """
    # get policy inputs
    updated_liquidity_pool = policy_input['liquidity_pool']

    return ('liquidity_pool', updated_liquidity_pool)

def update_agents_tx1_after_adoption(params, substep, state_history, prev_state, policy_input, **kwargs):
    """
    Function to update the agents after the adoption buys
    """
    # state variables
    liquidity_pool = prev_state['liquidity_pool'].copy()
    updated_agents = prev_state['agents'].copy()


    # get policy inputs
    new_lp_tokens = policy_input['lp_tokens']

    # update variables
    old_lp_tokens = liquidity_pool['tokens']

    # update logic
    bought_tokens = new_lp_tokens - old_lp_tokens
    # distribute the bought tokens to the market_investors agents
    market_investors = sum([1 for agent in updated_agents if (updated_agents[agent]['type'] == 'market_investors')])
    for agent in updated_agents:
        if updated_agents[agent]['type'] == 'market_investors':
            
            bought_tokens_per_market_investor = bought_tokens / market_investors

            updated_agents[agent]['tokens'] += bought_tokens_per_market_investor

    return ('agents', updated_agents)

def update_liquidity_pool_after_transaction(params, substep, state_history, prev_state, policy_input, **kwargs):
    """
    Function to update the liquidity pool after the adoption buys
    """
    # parameters
    initial_token_price = params['initial_token_price']

    # state variables
    updated_liquidity_pool = prev_state['liquidity_pool']

    # get policy inputs
    lp_tokens = policy_input['lp_tokens']
    lp_usdc = policy_input['lp_usdc']
    constant_product = policy_input['constant_product']
    token_price = policy_input['token_price']
    
    # prepare volatility calculation
    if policy_input['tx'] == 1:
        updated_liquidity_pool['token_price_max'] = token_price
        updated_liquidity_pool['token_price_min'] = token_price
    elif policy_input['tx'] in [2, 3, 4]:
        updated_liquidity_pool['token_price_max'] = np.max([updated_liquidity_pool['token_price_max'], token_price, initial_token_price])
        updated_liquidity_pool['token_price_min'] = np.min([updated_liquidity_pool['token_price_min'], token_price, initial_token_price])

    # update logic
    updated_liquidity_pool['tokens'] = lp_tokens
    updated_liquidity_pool['usdc'] = lp_usdc
    updated_liquidity_pool['constant_product'] = constant_product
    updated_liquidity_pool['token_price'] = token_price
    updated_liquidity_pool['LP_valuation'] = lp_usdc + lp_tokens * token_price
    updated_liquidity_pool['volatility'] = ((updated_liquidity_pool['token_price_max'] - updated_liquidity_pool['token_price_min'])
                                            / updated_liquidity_pool['token_price_max'] * 100)

    return ('liquidity_pool', updated_liquidity_pool)
