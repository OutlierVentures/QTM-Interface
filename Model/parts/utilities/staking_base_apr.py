from ..utils import import_dummy_data



# POLICIY FUNCTIONS
def apr(params, substep, state_history, prev_state, **kwargs):
    """
    Policy function to incentivise the ecosystem
    """
    # get parameters
    lock_apr = params['lock_apr']/100
    lock_share = params['lock_share']/100
    
    # fake data 
    dummy_locked_apr_tokens = import_dummy_data(109, prev_state['timestep']-1)


    #Calculating the agent utility sum -> Row 87
    agent_utility_sum = 0
    agents = prev_state['agents'].copy()
    for agent in agents:
        
        utility_tokens = agents[agent]['a_utility_tokens']
        agent_utility_sum += utility_tokens

    dummy_airdrop_holding_supply = import_dummy_data(86, prev_state['timestep']-1)
    agent_utility_sum += dummy_airdrop_holding_supply


    
    staking_base_apr = agent_utility_sum * lock_share



    utility_removal_perc = prev_state['token_economy']['remove_perc']/100
     
    if prev_state['timestep'] == 1 :
        removal_token = 0
        prev_staking_base_apr_cum = 0
    else:
        prev_staking_base_apr_cum = prev_state['utilities']['staking_base_apr_cum']
        removal_token = -staking_base_apr * utility_removal_perc

    staking_base_apr_cum = prev_staking_base_apr_cum + staking_base_apr + removal_token



    staking_rewards = staking_base_apr_cum * lock_apr/12
  

    return {'staking_rewards': staking_rewards,'staking_base_apr_cum':staking_base_apr_cum}








# STATE UPDATE FUNCTIONS





def update_utilties_after_apr(params, substep, state_history, prev_state, policy_input, **kwargs):
    """
    Function to update the token economy after apr
    """

    # get state variables
    updated_utilities = prev_state['utilities'].copy()

    # get policy input
    stake_base_apr_allocation_cum = policy_input['staking_base_apr_cum']
    staking_rewards = policy_input['staking_rewards']

    # update logic

    updated_utilities['staking_base_apr_cum'] = stake_base_apr_allocation_cum
    updated_utilities['staking_rewards'] = staking_rewards




    return ('utilities', updated_utilities)



#NEED TO BUILD AGENT ONE
def update_agents_after_apr(params, substep, state_history, prev_state, policy_input, **kwargs):
    """
    Function to update the vested tokens for each investor based on some criteria
    """
    # get parameters
    lock_payout_source = params['lock_payout_source']

    # get state variables
    updated_agents = prev_state['agents']

    # get policy input
    vested_incentivisation_tokens = policy_input['vested_incentivisation_tokens']

    # update logic
    # subtract vested incentivisation tokens from protocol bucket
    for agent in updated_agents:
        if updated_agents[agent]['a_type'] == 'protocol_bucket' and incentivisation_payout_source.lower() in updated_agents[agent]['a_name'].lower():
            updated_agents[agent]['a_tokens'] = updated_agents[agent]['a_tokens'] - vested_incentivisation_tokens

    # add vested incentivisation tokens to market participants
    # count amount of market_investors and early_investors in updated_agents
    investors = sum([1 for agent in updated_agents if (updated_agents[agent]['a_type'] == 'market_investors' or updated_agents[agent]['a_type'] == 'early_investor')])
    for agent in updated_agents:
        if updated_agents[agent]['a_type'] == 'market_investors' or updated_agents[agent]['a_type'] == 'early_investor':
            updated_agents[agent]['a_tokens'] = updated_agents[agent]['a_tokens'] + vested_incentivisation_tokens / investors

    return ('agents', updated_agents)



