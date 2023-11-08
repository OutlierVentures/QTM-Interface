"""Calculation and processing of liquidity mining at agent level.

Contains policy functions (PF) and state update functions (SUF).


Functions:
    liquidity_mining_agent_allocation (PF): Policy function to calculate the agent liquidity mining

    update_agents_after_liquidity_mining (SUF): Function to update agent liquidity mining allocations

    update_utilties_after_liquidity_mining (SUF): Function to update meta liquidity mining allocations.

"""


# POLICY FUNCTIONS
def liquidity_mining_agent_allocation(params, substep, state_history, prev_state, **kwargs):
    """
    Policy function to calculate the agent liquidity mining
    """
    # get parameters
    liquidity_mining_apr = params['liquidity_mining_apr']/100
    liquidity_mining_share = params['liquidity_mining_share']/100
    
    # get state variables
    agents = prev_state['agents'].copy()
    lp = prev_state['liquidity_pool'].copy()
    token_economy = prev_state['token_economy'].copy()

    # get impermanent loss adjustment related variables
    selling_allocation = token_economy['te_selling_allocation']
    lp_tokens_after_liquidity_addition = lp['lp_tokens_after_liquidity_addition']
    lp_tokens = lp['lp_tokens']
    IL_adjustment_factor = [(lp_tokens + selling_allocation) / lp_tokens_after_liquidity_addition if lp_tokens_after_liquidity_addition > 0 else 1][0]

    # policy logic
    # initialize policy logic variables
    agent_utility_sum = 0
    agent_utility_removal_sum = 0
    agent_utility_rewards_sum = 0
    agents_liquidity_mining_allocations = {}
    agents_liquidity_mining_removal = {}
    agents_liquidity_mining_rewards = {}

    # calculate the liquidity mining apr token allocations and removals for each agent
    if liquidity_mining_share > 0:
        for agent in agents:
            utility_removal_perc = agents[agent]['a_actions']['remove_tokens']
            utility_tokens = agents[agent]['a_utility_tokens'] + agents[agent]['a_utility_from_holding_tokens'] # get the new agent utility token allocations from vesting, airdrops, incentivisation, and holdings of previous timestep
            tokens_liquidity_mining_cum = agents[agent]['a_tokens_liquidity_mining_cum'] # get amount of liq. mining allocated tokens from last timestep
            
            agents_liquidity_mining_allocations[agent] = utility_tokens * liquidity_mining_share # calculate the amount of tokens that shall be allocated to the liquidity mining apr utility from this timestep
            agents_liquidity_mining_removal[agent] = tokens_liquidity_mining_cum * utility_removal_perc # calculate the amount of tokens that shall be removed from the liquidity mining apr utility for this timestep based on the tokens allocated in the previous timestep
            agents_liquidity_mining_rewards[agent] = (tokens_liquidity_mining_cum * (1+(IL_adjustment_factor - 1)) + agents_liquidity_mining_allocations[agent] - agents_liquidity_mining_removal[agent]) * liquidity_mining_apr/12 # calculate the amount of tokens that shall be rewarded to the agent for liquidity mining 
            
            agent_utility_sum += agents_liquidity_mining_allocations[agent] # sum up the total amount of tokens allocated to the liquidity mining apr utility for this timestep
            agent_utility_removal_sum += agents_liquidity_mining_removal[agent] # sum up the total amount of tokens removed from the liquidity mining apr utility for this timestep
            agent_utility_rewards_sum += agents_liquidity_mining_rewards[agent] # sum up the total amount of tokens rewarded to the agent for liquidity mining for this timestep

    return {'agents_liquidity_mining_allocations': agents_liquidity_mining_allocations,'agents_liquidity_mining_removal':agents_liquidity_mining_removal,
            'agents_liquidity_mining_rewards': agents_liquidity_mining_rewards, 'agent_utility_sum': agent_utility_sum,
            'agent_utility_removal_sum': agent_utility_removal_sum, 'agent_utility_rewards_sum': agent_utility_rewards_sum, 'IL_adjustment_factor': IL_adjustment_factor}



# STATE UPDATE FUNCTIONS
def update_agents_after_liquidity_mining(params, substep, state_history, prev_state, policy_input, **kwargs):
    """
    Function to update agent liquidity mining allocations
    """
    # get parameters
    liquidity_mining_payout_source = params['liquidity_mining_payout_source']

    # get state variables
    updated_agents = prev_state['agents'].copy()

    # get policy input
    agents_liquidity_mining_allocations = policy_input['agents_liquidity_mining_allocations']
    agents_liquidity_mining_removal = policy_input['agents_liquidity_mining_removal']
    agents_liquidity_mining_rewards = policy_input['agents_liquidity_mining_rewards']
    agent_utility_rewards_sum = policy_input['agent_utility_rewards_sum']
    IL_adjustment_factor = policy_input['IL_adjustment_factor']

    # update logic
    if agents_liquidity_mining_allocations != {}:
        for agent in updated_agents:
            updated_agents[agent]['a_tokens_liquidity_mining'] = agents_liquidity_mining_allocations[agent]
            updated_agents[agent]['a_tokens_liquidity_mining_cum'] = updated_agents[agent]['a_tokens_liquidity_mining_cum'] * (1 + (IL_adjustment_factor - 1)) + agents_liquidity_mining_allocations[agent] - agents_liquidity_mining_removal[agent]
            updated_agents[agent]['a_tokens_liquidity_mining_remove'] = agents_liquidity_mining_removal[agent]
            updated_agents[agent]['a_tokens_liquidity_mining_rewards'] = agents_liquidity_mining_rewards[agent]
            updated_agents[agent]['a_tokens'] += (agents_liquidity_mining_rewards[agent] + agents_liquidity_mining_removal[agent])

            # subtract tokens from payout source agent
            if updated_agents[agent]['a_name'].lower() in liquidity_mining_payout_source.lower():
                updated_agents[agent]['a_tokens'] -= agent_utility_rewards_sum

    return ('agents', updated_agents)



def update_utilties_after_liquidity_mining(params, substep, state_history, prev_state, policy_input, **kwargs):
    """
    Function to update meta liquidity mining allocations
    """
    # get state variables
    updated_utilities = prev_state['utilities'].copy()

    # get policy input
    agent_utility_sum = policy_input['agent_utility_sum']
    agent_utility_removal_sum = policy_input['agent_utility_removal_sum']
    agent_utility_rewards_sum = policy_input['agent_utility_rewards_sum']
    IL_adjustment_factor = policy_input['IL_adjustment_factor']

    # update logic
    updated_utilities['u_liquidity_mining_rewards'] = agent_utility_rewards_sum
    updated_utilities['u_liquidity_mining_allocation'] = (agent_utility_sum)
    updated_utilities['u_liquidity_mining_allocation_cum'] = updated_utilities['u_liquidity_mining_allocation_cum'] * (1 + (IL_adjustment_factor - 1)) + agent_utility_sum - agent_utility_removal_sum
    updated_utilities['u_liquidity_mining_allocation_remove'] = agent_utility_removal_sum

    return ('utilities', updated_utilities)
