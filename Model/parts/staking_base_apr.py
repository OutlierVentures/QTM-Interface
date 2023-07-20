




### NEED BUCKET ALLOCATIONS

##---staking_base_apr---###

# POLICY FUNCTIONS
def staking_base_apr(params, substep, state_history, prev_state, **kwargs):
    lock_share = params['lock_share']
    lock_APR = params['lock_APR']
    lock_payout_source = params['lock_payout_source'] #Does this actually do anything?

    payout_apy =(1+lock_APR/100/12)^12*100-100

    # staking_base_apr = utility_token_allocation_sum *lock_share/100
    staking_base_apr_cum = 0    #prev_staking_base_apr_cum + staking_base_apr+removal_token_staking_base_apr
    return ('staking_base_apr_cum',staking_base_apr_cum)


# STATE UPDATE FUNCTIONS
def update_staking_base_apr(params, substep, state_history, prev_state, policy_input, **kwargs):
    return









##---staking_buyback_distribute---###

# POLICY FUNCTIONS
def staking_buyback_distribute(params, substep, state_history, prev_state, **kwargs):



   
    staking_base_apr_cum = 0    #prev_staking_base_apr_cum + staking_base_apr+removal_token_staking_base_apr
    return ('staking_base_apr_cum',staking_base_apr_cum)


# STATE UPDATE FUNCTIONS
def update_staking_buyback_distribute(params, substep, state_history, prev_state, policy_input, **kwargs):
    return
