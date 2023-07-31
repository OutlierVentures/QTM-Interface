from .utils import import_dummy_data



# POLICIY FUNCTIONS
def apr(params, substep, state_history, prev_state, **kwargs):
    """
    Policy function to incentivise the ecosystem
    """
    # get parameters
    lock_payout_source = params['lock_payout_source']
    lock_apr = params['lock_apr']
    lock_share = params['lock_share']
    
    # fake data 
    dummy_locked_apr_tokens = import_dummy_data(prev_state,109)
    #locked_apr_tokens = prev_state['token_economy']['tokens_apr_locked'] this is not full


    total_reward_tokens = dummy_locked_apr_tokens * lock_apr/100/12


    return {'total_reward_tokens': total_reward_tokens}








# STATE UPDATE FUNCTIONS



#NEED TO BUILD AGENT ONE
def update_agents_after_apr(params, substep, state_history, prev_state, policy_input, **kwargs):
    """
    Function to update the vested tokens for each investor based on some criteria
    """
    # get parameters
    incentivisation_payout_source = params['incentivisation_payout_source']

    # get state variables
    updated_agents = prev_state['agents']

    # get policy input
    vested_incentivisation_tokens = policy_input['vested_incentivisation_tokens']

    # update logic
    # subtract vested incentivisation tokens from protocol bucket
    for agent in updated_agents:
        if updated_agents[agent]['type'] == 'protocol_bucket' and incentivisation_payout_source.lower() in updated_agents[agent]['name'].lower():
            updated_agents[agent]['tokens'] = updated_agents[agent]['tokens'] - vested_incentivisation_tokens

    # add vested incentivisation tokens to market participants
    # count amount of market_investors and early_investors in updated_agents
    investors = sum([1 for agent in updated_agents if (updated_agents[agent]['type'] == 'market_investors' or updated_agents[agent]['type'] == 'early_investor')])
    for agent in updated_agents:
        if updated_agents[agent]['type'] == 'market_investors' or updated_agents[agent]['type'] == 'early_investor':
            updated_agents[agent]['tokens'] = updated_agents[agent]['tokens'] + vested_incentivisation_tokens / investors

    return ('agents', updated_agents)




def update_token_economy_after_apr(params, substep, state_history, prev_state, policy_input, **kwargs):
    """
    Function to update the token economy after incentivisation
    """
    # get parameters


    # get state variables
    updated_token_economy = prev_state['token_economy'].copy()
    liquidity_pool = prev_state['liquidity_pool']

    # get policy input
    total_reward_tokens = policy_input['total_reward_tokens']

    # update logic

    updated_token_economy['apr_tokens'] = total_reward_tokens
    updated_token_economy['apr_tokens_usd'] = total_reward_tokens * liquidity_pool['token_price']

    return ('token_economy', updated_token_economy)