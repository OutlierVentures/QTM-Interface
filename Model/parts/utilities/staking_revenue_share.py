# POLICY FUNCTIONS
def staking_revenue_share_buyback_amount(params, substep, state_history, prev_state, **kwargs):
    """
    Policy function to calculate the amount of usd to be used for token buyback from the revenue share
    """
    # get parameters
    staking_revenue_utility_share_allocation = params['lock_buyback_distribute_share']
    revenue_share = params['lock_buyback_from_revenue_share'] # revenue share to be used for buyback

    # get state variables
    user_adoption = prev_state['user_adoption'].copy()
    product_revenue = user_adoption['product_revenue']

    # policy logic
    if float(staking_revenue_utility_share_allocation) > 0:
        buyback_amount = product_revenue * float(revenue_share) / 100
    else:
        buyback_amount = 0

    return {'buyback_from_revenue_share_usd': buyback_amount}


# STATE UPDATE FUNCTIONS
def update_buyback_amount_from_revenue_share(params, substep, state_history, prev_state, policy_input, **kwargs):
    """
    Function to update capital amount for token buybacks from the revenue share
    """
    # get parameters

    # get state variables
    updated_utilities = prev_state['utilities'].copy()

    # get policy input
    buyback_from_revenue_share_usd = policy_input['buyback_from_revenue_share_usd']

    # update logic
    updated_utilities['buyback_from_revenue_share_usd'] = buyback_from_revenue_share_usd

    return ('utilities', updated_utilities)