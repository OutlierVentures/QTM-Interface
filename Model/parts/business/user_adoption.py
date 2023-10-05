import math
from Model.parts.utils import *



def calculate_user_adoption(initial_users,final_users,velocity,timestamp,total_days):
    """
    Definition:
        Function to take in user adoption data and calculate the amount of adoption, can be used for token adoption and product users
    
    Parameters:
        initial_users: starting amount of users
        final_users: ending amount of users
        velocity: speed of adoption on those users
        timstep: current timestep in days
        total_days: length of full simulation
    
    """

    term1 = (1 / (1 + math.exp(-velocity * 0.002 * (timestamp - 1825) / velocity))) * final_users + initial_users
    term2 = (1 / (1 + math.exp(-velocity * 0.002 * (0 - 1825) / velocity))) * final_users
    term3 = initial_users * (timestamp / total_days)
    term4 = final_users - (term1 - term2 - term3)
    result = term1 - term2 - term3 + (term4 * (timestamp / total_days))
    
    return result


# POLICY FUNCTIONS
def user_adoption_metrics(params, substep, state_history, prev_state, **kwargs):
    """
    Calculate the initial token economy metrics, such as MC, FDV MC, circ. supply, and tokens locked.
    """

    current_month = prev_state['timestep']
    current_date = prev_state['date']
    launchDate = pd.to_datetime(params['launch_date'], format='%d.%m.%y')

    current_day = (pd.to_datetime(current_date)+pd.DateOffset(months=1) - launchDate).days

    # This is what is shown in the model as a constant as the user adoption numbers refer to 10 years (product_users_after_10y & token_holers_after_10y)
    total_days = 3653                        

    ## Product user adoption
    initial_product_users = params['initial_product_users']
    product_users_after_10y = params['product_users_after_10y']
    product_adoption_velocity = params['product_adoption_velocity']
    one_time_product_revenue_per_user = params['one_time_product_revenue_per_user']
    regular_product_revenue_per_user = params['regular_product_revenue_per_user']

    product_users = calculate_user_adoption(initial_product_users,product_users_after_10y,product_adoption_velocity,current_day,total_days)

    ## Product Revenue
    
    prev_product_users = prev_state['user_adoption']['ua_product_users']
    if current_month == 1:
        product_revenue = product_users*(one_time_product_revenue_per_user+regular_product_revenue_per_user)
    else:
        product_revenue = (product_users-prev_product_users)*one_time_product_revenue_per_user+product_users*regular_product_revenue_per_user

    ## Token holder adoption
    initial_token_holders = params['initial_token_holders']
    token_holders_after_10y = params['token_holders_after_10y']
    token_adoption_velocity = params['token_adoption_velocity']
    one_time_token_buy_per_user = params['one_time_token_buy_per_user']
    regular_token_buy_per_user = params['regular_token_buy_per_user']

    token_holders = calculate_user_adoption(initial_token_holders,token_holders_after_10y,token_adoption_velocity,current_day,total_days)

    ## Calculating Token Buys
    prev_token_holders = prev_state['user_adoption']['ua_token_holders']
    if current_month == 1:
        token_buys =(one_time_token_buy_per_user+regular_token_buy_per_user)*token_holders
    else:
        token_buys =((token_holders-prev_token_holders)*one_time_token_buy_per_user)+token_holders*regular_token_buy_per_user

    #token2_in_lp = token_buys/ lp2 price
    # This is going to be the same as token buys because we are assuing USD is the pair

    return {'ua_product_users': product_users, 'ua_token_holders': token_holders,'ua_product_revenue': product_revenue,'ua_token_buys':token_buys}



# STATE UPDATE FUNCTIONS
def update_user_adoption(params, substep, state_history, prev_state, policy_input, **kwargs):
    """
    Function to update the user adoption metrics
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









