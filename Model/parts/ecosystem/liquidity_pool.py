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
        
    return {'lp_tokens': lp_tokens, 'lp_usdc': lp_usdc, 'constant_product': constant_product, 'token_price': token_price}


# STATE UPDATE FUNCTIONS
def update_lp_after_lp_seeding(params, substep, state_history, prev_state, policy_input, **kwargs):
    """
    Function to update the agents based on the changes in business funds to seed the liquidity pool.
    """
    # get policy inputs
    updated_liquidity_pool = policy_input['liquidity_pool']

    return ('liquidity_pool', updated_liquidity_pool)

def update_liquidity_pool_tx1_after_adoption(params, substep, state_history, prev_state, policy_input, **kwargs):
    """
    Function to update the liquidity pool after the adoption buys
    """
    # state variables
    updated_liquidity_pool = prev_state['liquidity_pool']

    # get policy inputs
    lp_tokens = policy_input['lp_tokens']
    lp_usdc = policy_input['lp_usdc']
    constant_product = policy_input['constant_product']
    token_price = policy_input['token_price']

    # update logic
    updated_liquidity_pool['tokens'] = lp_tokens
    updated_liquidity_pool['usdc'] = lp_usdc
    updated_liquidity_pool['constant_product'] = constant_product
    updated_liquidity_pool['token_price'] = token_price

    return ('liquidity_pool', updated_liquidity_pool)