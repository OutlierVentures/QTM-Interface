

#This is not currently being used








##-------STAKING_BASE_APR-------###
#Locking tokens for staking to receive rewards in the same token. Staked tokens give owner voting power in the DAO.

# POLICY FUNCTIONS
def staking_base_apr(params, substep, state_history, prev_state, **kwargs):
    lock_share = params['lock_share']
    lock_apr = params['lock_apr']
    lock_payout_source = params['lock_payout_source'] #Does this actually do anything?

    payout_apy = (1 + lock_apr / 100 / 12) ** 12 * 100 - 100


    if prev_state['timestep']==1:
        print('-----------------------------------')
        print(prev_state['token_economy']['utility_allocation']) # THIS MIGHT NEED TO CHANGE
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






















##-------STAKING_BUYBACK_DISTRIBUTE-------###
#Locking tokens for staking to receive rewards in the same token. Staked tokens give owner voting power in the DAO.

# POLICY FUNCTIONS
def staking_buyback_distribute(params, substep, state_history, prev_state, **kwargs):
   
    staking_base_apr_cum = 0    #prev_staking_base_apr_cum + staking_base_apr+removal_token_staking_base_apr

    return ('staking_base_apr_cum',staking_base_apr_cum)


# STATE UPDATE FUNCTIONS
def update_staking_buyback_distribute(params, substep, state_history, prev_state, policy_input, **kwargs):
    return









##-------LIQUIDITY_MINING-------###
#Provide liquidity and receive tokens based on amount




##-------BURNING-------###
#Burn tokens (e.g. for some benefit)


##-------HOLDING-------###
#Just hold the tokens in your wallet and receive rewards based on the amount


##-------Transfer-------###
#Transfer tokens to receive some benefit (e.g. for purchasing a NFT, another product, or to earn reputation etc.). Transferred tokens will go to the "Transfer Destination" bucket.




