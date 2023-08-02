from .utils import *

# POLICY FUNCTIONS
def initialize_liquidity_pool(params, substep, state_history, prev_state, **kwargs):
    """
    Function to initialize the liquidity pool in the first timestep
    """

    # parameters
    required_usdc = params['initial_required_usdc']
    required_tokens = params['initial_lp_token_allocation']
    business_fund_holder = params['business_fund_holder']

    # state variables
    current_month = prev_state['timestep']
    liquidity_pool = prev_state['liquidity_pool']

    if current_month == 0:
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


# STATE UPDATE FUNCTIONS
def update_lp_after_lp_seeding(params, substep, state_history, prev_state, policy_input, **kwargs):
    """
    Function to update the agents based on the changes in business funds to seed the liquidity pool.
    """
    # get policy inputs
    updated_liquidity_pool = policy_input['liquidity_pool']

    return ('liquidity_pool', updated_liquidity_pool)