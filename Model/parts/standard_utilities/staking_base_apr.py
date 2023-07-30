




### NEED BUCKET ALLOCATIONS

##---staking_base_apr---###

# POLICY FUNCTIONS
def staking_base_apr(params, substep, state_history, prev_state, **kwargs):
    lock_share = params['lock_share']
    lock_apr = params['lock_apr']
    lock_payout_source = params['lock_payout_source'] #Does this actually do anything?

    payout_apy = (1 + lock_apr / 100 / 12) ** 12 * 100 - 100


    if prev_state['timestep']==1:
        print('-----------------------------------')
        print(prev_state['token_economy']['utility_allocation'])
        print('-----------------------------------')


       

    #staking_base_apr_allocation = utility_token_allocation_sum *lock_share/100
    #staking_base_apr_allocation_cum = past_cum + current - removal

    #removal = cum* removal %



    #staking_base_apr_removal

    #rewards_tokens
    #rewards_dollars

    staking_base_apr_cum = 0    
    return {'staking_base_apr_cum': staking_base_apr_cum}


# STATE UPDATE FUNCTIONS
def update_staking_base_apr(params, substep, state_history, prev_state, policy_input, **kwargs):

    update_standard_utilities = prev_state['standard_utilities']
    update_standard_utilities['staking_base_apr_cum'] = policy_input['staking_base_apr_cum']

    return ('standard_utilities',update_standard_utilities)








