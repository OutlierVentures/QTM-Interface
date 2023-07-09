import math



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

    current_day = current_month*30 #need to adjust it to being months
    total_days = 3653 # THis is what is shown in the model as a constant
                        

    ## Product user adoption
    initial_product_users = params['initial_product_users']
    product_users_after_10y = params['product_users_after_10y']
    product_adoption_velocity = params['product_adoption_velocity']
    one_time_product_revenue_per_user = params['one_time_product_revenue_per_user']
    regular_product_revenue_per_user = params['regular_product_revenue_per_user']

    product_users = calculate_user_adoption(initial_product_users,product_users_after_10y,product_adoption_velocity,current_day,total_days)

    ## Token holder adoption
    initial_token_holders = params['initial_token_holders']
    token_holders_after_10y = params['token_holders_after_10y']
    token_adoption_velocity = params['token_adoption_velocity']
    one_time_token_buy_per_user = params['one_time_token_buy_per_user']
    regular_token_buy_per_user = params['regular_token_buy_per_user']

    token_holders = calculate_user_adoption(initial_token_holders,token_holders_after_10y,token_adoption_velocity,current_day,total_days)


    ## Product Revenue
    prev_product_users = prev_state['user_adoption']['product_users']
    product_revenue = (product_users-prev_product_users)*one_time_product_revenue_per_user+product_users*regular_product_revenue_per_user


    ## Calculating Token Buys
    prev_token_holders = prev_state['user_adoption']['token_holders']
    token_buys =((token_holders-prev_token_holders)*one_time_token_buy_per_user)+token_holders*regular_token_buy_per_user

    # Calculate token_2_in_lp *WAITING FOR PAIRING TOKEN DATA*
    #token_2_in_lp = token_buys/prev_state['']
    

    avg_token_utility_allocation = params['avg_token_utility_allocation']
    avg_token_holding_allocation = params['avg_token_holding_allocation']
    avg_token_selling_allocation = params['avg_token_selling_allocation']
    avg_token_utility_removal = params['avg_token_utility_removal']


    return {'product_users': product_users, 'token_holders': token_holders,'product_revenue': product_revenue,'token_buys':token_buys}



# STATE UPDATE FUNCTIONS
def update_user_adoption(params, substep, state_history, prev_state, policy_input, **kwargs):
    """
    Function to update the user adoption metrics
    """

    product_users = policy_input['product_users']
    token_holders  = policy_input['token_holders']
    product_revenue = policy_input['product_revenue']
    token_buys = policy_input['token_buys']

    
    updated_user_adoption = {
        'product_users': product_users,
        'token_holders': token_holders,
        'product_revenue': product_revenue,
        'token_buys': token_buys
    }

    return ('user_adoption', updated_user_adoption)









