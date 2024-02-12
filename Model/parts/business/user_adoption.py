"""Calculate and update user adoption metrics.

Contains policy functions (PF) and state update functions (SUF).


Functions:
    calculate_user_adoption: Take in user adoption data and calculate the amount of adoption.

    user_adoption_metrics (PF): Calculate the metrics relevant for monitoring user adoption.

    update_user_adoption (SUF): Function to update the user adoption metrics.

"""

import math
from Model.parts.utils import *
import random

# POLICY FUNCTIONS
def user_adoption_metrics(params, substep, state_history, prev_state, **kwargs):
    """
    Calculate the metrics relevant for monitoring user adoption.

    Policy function.

    Token adoption and product users are calculated according to the logic provided in the
    calculate_user_adoption function.

    Returns:
        A dict which provides information on product users, token holders, product
        revenue and token buys.
    
    """
    # state variables for all
    current_month = prev_state['timestep']
    current_date = prev_state['date']
    token_economy = prev_state['token_economy'].copy()
    launchDate = pd.to_datetime(params['launch_date'], format='%d.%m.%Y')
    if params['agent_behavior'] == 'simple':
        random_seed = params['random_seed']
        random.seed(random_seed + current_month)

    # current_day = (pd.to_datetime(current_date)+pd.DateOffset(months=1) - launchDate).days
    current_day = (pd.to_datetime(current_date)+pd.DateOffset(months=1) - pd.to_datetime('today')).days # let current day start from the start of the simulation for user adoption

    ## Product user adoption
    # parameters
    initial_product_users = params['initial_product_users']
    product_users_after_10y = params['product_users_after_10y']
    product_adoption_velocity = params['product_adoption_velocity']
    one_time_product_revenue_per_user = params['one_time_product_revenue_per_user']
    regular_product_revenue_per_user = params['regular_product_revenue_per_user']
    user_adoption_target = params['user_adoption_target'] if 'user_adoption_target' in params else 0
    
    # state variables
    prev_product_users = prev_state['user_adoption']['ua_product_users']
    product_users = calculate_user_adoption(initial_product_users,product_users_after_10y,product_adoption_velocity,current_day)

    # adjust product users according to incentivisation target
    if user_adoption_target != 0:
        # calculate new product users based on incentivisation target
        last_month_day = (pd.to_datetime(current_date) - pd.to_datetime('today')).days
        product_users_last_month_regular = calculate_user_adoption(initial_product_users,product_users_after_10y,product_adoption_velocity,last_month_day)
        product_users = (product_users - product_users_last_month_regular) + prev_product_users
        incentive_adoption_ratio = token_economy['te_incentivised_usd_per_product_user'] / user_adoption_target

        product_users = product_users + (product_users-prev_product_users) * (incentive_adoption_ratio - 1) if incentive_adoption_ratio > 0 else product_users

    ## Product Revenue
    if current_month == 1:
        product_revenue = product_users*(one_time_product_revenue_per_user+regular_product_revenue_per_user)
    else:
        product_revenue = (product_users-prev_product_users)*one_time_product_revenue_per_user + product_users*regular_product_revenue_per_user

    
    ## Token holder adoption
    # parameters
    initial_token_holders = params['initial_token_holders']
    token_holders_after_10y = params['token_holders_after_10y']
    token_adoption_velocity = params['token_adoption_velocity']
    one_time_token_buy_per_user = params['one_time_token_buy_per_user']
    regular_token_buy_per_user = params['regular_token_buy_per_user']
    agent_behavior = params['agent_behavior']
    agent_staking_apr_target = params['agent_staking_apr_target'] if 'agent_staking_apr_target' in params else 0

    # state variables
    prev_token_holders = prev_state['user_adoption']['ua_token_holders']

    token_holders = calculate_user_adoption(initial_token_holders,token_holders_after_10y,token_adoption_velocity,current_day)

    # adjust token holders according to staking target
    if agent_behavior == 'simple':
        last_month_day = (pd.to_datetime(current_date) - pd.to_datetime('today')).days
        token_holders_last_month_regular = calculate_user_adoption(initial_token_holders,token_holders_after_10y,token_adoption_velocity,last_month_day)
        token_holders = (token_holders - token_holders_last_month_regular) + prev_token_holders
        staking_apr_ratio = (token_economy['te_staking_apr'] / agent_staking_apr_target)**2

        token_holders = token_holders + (token_holders-prev_token_holders) * (staking_apr_ratio - 1) if staking_apr_ratio > 0 else token_holders

    ## Calculating Token Buys
    if current_month == 1:
        token_buys =(one_time_token_buy_per_user+regular_token_buy_per_user)*token_holders
    else:
        token_buys =((token_holders-prev_token_holders)*one_time_token_buy_per_user)+token_holders*regular_token_buy_per_user

    return {'ua_product_users': product_users, 'ua_token_holders': token_holders,'ua_product_revenue': product_revenue,'ua_token_buys':token_buys}



# STATE UPDATE FUNCTIONS
def update_user_adoption(params, substep, state_history, prev_state, policy_input, **kwargs):
    """
    Function to update the user adoption metrics.

    State update function.

    Returns:
        A tuple ('user_adoption', updated_user_adoption), where updated_user_adoption
        provides updated information on product users, token holders, product revenue
        and token buys.
    
    """

    product_users = policy_input['ua_product_users']
    token_holders  = policy_input['ua_token_holders']
    product_revenue = policy_input['ua_product_revenue']
    token_buys = policy_input['ua_token_buys']

    updated_user_adoption = {
        'ua_product_users': product_users,
        'ua_token_holders': token_holders,
        'ua_product_revenue': product_revenue,
        'ua_token_buys': token_buys
    }

    return ('user_adoption', updated_user_adoption)









