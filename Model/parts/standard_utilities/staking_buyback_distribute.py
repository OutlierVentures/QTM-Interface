



##---staking_buyback_distribute---###

# POLICY FUNCTIONS
def staking_buyback_distribute(params, substep, state_history, prev_state, **kwargs):



   
    staking_base_apr_cum = 0    #prev_staking_base_apr_cum + staking_base_apr+removal_token_staking_base_apr
    return ('staking_base_apr_cum',staking_base_apr_cum)


# STATE UPDATE FUNCTIONS
def update_staking_buyback_distribute(params, substep, state_history, prev_state, policy_input, **kwargs):
    return
