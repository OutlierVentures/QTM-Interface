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
    agent_behavior = params['agent_behavior']
    if agent_behavior == 'simple':
        random_seed = params['random_seed']
        random.seed(random_seed + current_month)
    
    current_day = (pd.to_datetime(current_date)+pd.DateOffset(months=1) - pd.to_datetime('today')).days # let current day start from the start of the simulation for user adoption (disable this for testing)

    # Enable these for testing against the old QTM data
    #launchDate = get_initial_date(params) # enable this for testing
    #current_day = (pd.to_datetime(current_date)+pd.DateOffset(months=1) - launchDate).days # enable this for testing

    ## Product user adoption
    # parameters
    initial_product_users = params['initial_product_users']
    product_users_after_10y = params['product_users_after_10y']
    product_adoption_velocity = params['product_adoption_velocity']
    one_time_product_revenue_per_user = params['one_time_product_revenue_per_user']
    regular_product_revenue_per_user = params['regular_product_revenue_per_user']
    user_adoption_target = params['user_adoption_target'] if 'user_adoption_target' in params else 0
    avg_product_user_growth_rate = params['avg_product_user_growth_rate'] if 'avg_product_user_growth_rate' in params else 0
    
    # state variables
    prev_product_users = prev_state['user_adoption']['ua_product_users']
    prev_product_users_m1 = state_history[-2][-1]['user_adoption']['ua_product_users'] if len(state_history) > 2 else 0
    te_incentivised_usd_per_product_user = token_economy['te_incentivised_usd_per_product_user']
    te_incentivised_usd_per_product_user_m1 = state_history[-2][-1]['token_economy']['te_incentivised_usd_per_product_user'] if len(state_history) > 2 else 0

    # adjust product users according to incentivisation target
    if user_adoption_target != 0 and agent_behavior == 'simple':
        # PID Controller for user adoption
        # get previous error
        prev_te_incentivised_usd_per_product_user_error = (te_incentivised_usd_per_product_user_m1 / user_adoption_target-1)**2 * np.sign(te_incentivised_usd_per_product_user_m1 / user_adoption_target-1)
        # Calculate the new error
        product_user_error = (te_incentivised_usd_per_product_user / user_adoption_target-1)**2 * np.sign(te_incentivised_usd_per_product_user / user_adoption_target-1)
        Kp_product_user=prev_product_users*10
        Ki_product_user=0.0
        Kd_product_user=prev_product_users*5
        product_user_signal = get_pid_controller_signal(Kp=Kp_product_user, Ki=Ki_product_user, Kd=Kd_product_user, error=product_user_error, integral=0, previous_error=prev_te_incentivised_usd_per_product_user_error, dt=1)
        prev_product_user_increase = prev_product_users - prev_product_users_m1 if (current_month > 1) else 0
        product_user_increase = 0 if (current_month <= 2) else prev_product_user_increase + product_user_signal
        product_user_increase = np.min([product_user_increase,prev_product_users*1.25]) # limit the product user growth to 0 to avoid negative growth and to 25% to prevent unrealistic growth
        product_users = prev_product_users + product_user_increase if prev_product_users >= initial_product_users*0.1 else initial_product_users*0.1
        product_users = np.max([product_users, prev_product_users*0.9, initial_product_users*0.1]) # limit the product user decrease to 10% per month and to overall 10% of the initial product user amount to avoid unrealistic decrease

    else:
        product_users = calculate_user_adoption(initial_product_users,product_users_after_10y,product_adoption_velocity,current_day)

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
    agent_staking_apr_target = params['agent_staking_apr_target'] if 'agent_staking_apr_target' in params else 0
    avg_token_holder_growth_rate = params['avg_token_holder_growth_rate'] if 'avg_token_holder_growth_rate' in params else 0

    # state variables
    prev_token_holders = prev_state['user_adoption']['ua_token_holders']
    prev_token_holders_m1 = state_history[-2][-1]['user_adoption']['ua_token_holders'] if len(state_history) > 2 else 0
    te_staking_apr = token_economy['te_staking_apr']
    te_staking_apr_m1 = state_history[-2][-1]['token_economy']['te_staking_apr'] if len(state_history) > 2 else 0


    # adjust token holders according to staking target
    if agent_behavior == 'simple':
        """         # PID Controller for token holder growth
        # get previous error
        prev_staking_apr_error = (te_staking_apr_m1 / agent_staking_apr_target-1)**2 * np.sign(te_staking_apr_m1 / agent_staking_apr_target-1)
        # Calculate the new error
        staking_apr_error = (te_staking_apr / agent_staking_apr_target-1)**2 * np.sign(te_staking_apr / agent_staking_apr_target-1)
        Kp_staking_apr=prev_token_holders*10
        Ki_staking_apr=0.0
        Kd_staking_apr=prev_token_holders*5
        staking_apr_signal = get_pid_controller_signal(Kp=Kp_staking_apr, Ki=Ki_staking_apr, Kd=Kd_staking_apr, error=staking_apr_error, integral=0, previous_error=prev_staking_apr_error, dt=1)
        prev_token_holder_increase = prev_token_holders - prev_token_holders_m1 if (current_month > 1) else 0
        token_holder_increase = 0 if (current_month <= 2) else prev_token_holder_increase + staking_apr_signal
        token_holder_increase = np.min([token_holder_increase,prev_token_holders*1.25]) # limit the token holder growth to 0 to avoid negative growth and to 25% to prevent unrealistic growth
        token_holders = prev_token_holders + token_holder_increase if prev_token_holders >= initial_token_holders*0.1 else initial_token_holders*0.1
        token_holders = np.max([token_holders, prev_token_holders*0.9, initial_token_holders*0.1]) # limit the token holder decrease to 10% per month and to overall 10% of the initial token holder amount to avoid unrealistic decrease """
        token_holders = calculate_user_adoption(initial_token_holders,token_holders_after_10y,token_adoption_velocity,current_day)

    else:
        token_holders = calculate_user_adoption(initial_token_holders,token_holders_after_10y,token_adoption_velocity,current_day)

    ## Calculating Token Buys
    if ('market' in params and params['market'] == 0) or 'market' not in params:
        if current_month == 1:
            token_buys =(one_time_token_buy_per_user+regular_token_buy_per_user)*token_holders
        else:
            token_buys =((token_holders-prev_token_holders)*one_time_token_buy_per_user)+token_holders*regular_token_buy_per_user 

        return {'ua_product_users': product_users, 'ua_token_holders': token_holders,'ua_product_revenue': product_revenue,'ua_token_buys':token_buys}
    else:
        # Get token to use for simulation from input parameters
        coin = params['token']
        
        # Retrieve market simulation initialized at the beginning of the simulation
        market_simu = prev_state['market']['market']

        # Compute monthly simulated return corresponding to current timestep 
        new_monthly_return = np.exp(market_simu[market_simu['timestep'] == current_month][f'{coin}_ln_return'].iloc[0])
        if current_month == 1:
            token_buys =(one_time_token_buy_per_user+regular_token_buy_per_user)*token_holders
        else:
            token_buys =((token_holders-prev_token_holders)*one_time_token_buy_per_user)+token_holders*regular_token_buy_per_user*(1 + new_monthly_return) # Simple %-wise buy pressure adjustment based on simulated market returns

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









