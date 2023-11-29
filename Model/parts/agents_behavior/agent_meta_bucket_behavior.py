"""Agent and meta bucket related state update and policy functions.

Contains policy functions (PF) and state update functions (SUF) 
relevant for behaviour of each type of agent and for meta bucket allocations.


Functions:
    generate_agent_meta_bucket_behavior: (PF) Define the agent behavior.
    
    agent_meta_bucket_allocations: (PF) Define the meta bucket token allocations 
        of all agents.

    update_agent_meta_bucket_behavior: (SUF) Function to update the agent behaviors.

    update_agent_meta_bucket_allocations: (SUF) Function to update the agent meta 
        bucket token allocations.

    update_token_economy_meta_bucket_allocations: (SUF) Update the meta bucket 
            allocations for the token economy.

"""

# POLICY FUNCTIONS
def generate_agent_meta_bucket_behavior(params, substep, state_history, prev_state, **kwargs):
    """
    Define the agent behavior for each agent type.

    Policy function.

    First, checks if the agent behaviour is set up to be stochastic. 
    If stochastic, agent actions are based on a weighted random choices.
    If static, define the agent behavior for each agent type based on previous state.
    If neither, raise an error.

    Returns: 
        A dict with key 'agent_behavior_dict' and value being a dict, mapping agent
        types to agent behaviour. 

    Raises:    
        ValueError: params['agent_behavior'] must be either 'stochastic' or 'static'.
        KeyError: Missing required parameter.

    """

    try:
        if params['agent_behavior'] == 'stochastic':
            """
            Define the agent behavior for each agent type for the stochastic agent behavior
            Agent actions are based on a weighted random choices.
            """
            agent_behavior_dict = {
                'angel': {
                    'trade': params['avg_token_selling_allocation']-params['avg_token_utility_removal']/3,
                    'hold': params['avg_token_holding_allocation']-params['avg_token_utility_removal']/3,
                    'utility': params['avg_token_utility_allocation']-params['avg_token_utility_removal']/3,
                    'remove_locked_tokens': params['avg_token_utility_removal'],
                },
                'seed': {
                    'trade': params['avg_token_selling_allocation']-params['avg_token_utility_removal']/3,
                    'hold': params['avg_token_holding_allocation']-params['avg_token_utility_removal']/3,
                    'utility': params['avg_token_utility_allocation']-params['avg_token_utility_removal']/3,
                    'remove_locked_tokens': params['avg_token_utility_removal'],
                },
                'presale_1': {
                    'trade': params['avg_token_selling_allocation']-params['avg_token_utility_removal']/3,
                    'hold': params['avg_token_holding_allocation']-params['avg_token_utility_removal']/3,
                    'utility': params['avg_token_utility_allocation']-params['avg_token_utility_removal']/3,
                    'remove_locked_tokens': params['avg_token_utility_removal'],
                },
                'presale_2': {
                    'trade': params['avg_token_selling_allocation']-params['avg_token_utility_removal']/3,
                    'hold': params['avg_token_holding_allocation']-params['avg_token_utility_removal']/3,
                    'utility': params['avg_token_utility_allocation']-params['avg_token_utility_removal']/3,
                    'remove_locked_tokens': params['avg_token_utility_removal'],
                },
                'public_sale': {
                    'trade': params['avg_token_selling_allocation']-params['avg_token_utility_removal']/3,
                    'hold': params['avg_token_holding_allocation']-params['avg_token_utility_removal']/3,
                    'utility': params['avg_token_utility_allocation']-params['avg_token_utility_removal']/3,
                    'remove_locked_tokens': params['avg_token_utility_removal'],
                },
                'team': {
                    'trade': params['avg_token_selling_allocation']-params['avg_token_utility_removal']/3,
                    'hold': params['avg_token_holding_allocation']-params['avg_token_utility_removal']/3,
                    'utility': params['avg_token_utility_allocation']-params['avg_token_utility_removal']/3,
                    'remove_locked_tokens': params['avg_token_utility_removal'],
                },
                'reserve': {
                    'trade': 0,
                    'hold': 50,
                    'utility': 0,
                    'remove_locked_tokens': 0,
                    'incentivise': 50
                },
                'community': {
                    'trade': 0,
                    'hold': 100,
                    'utility': 0,
                    'remove_locked_tokens': 0,
                    'incentivise': 0
                },
                'foundation': {
                    'trade': 0,
                    'hold': 100,
                    'utility': 0,
                    'remove_locked_tokens': 0,
                    'incentivise': 0
                },
                'incentivisation': {
                    'trade': 0,
                    'hold': 100,
                    'utility': 0,
                    'remove_locked_tokens': 0,
                    'incentivise': 0
                },
                'staking_vesting': {
                    'trade': 0,
                    'hold': 100,
                    'utility': 0,
                    'remove_locked_tokens': 0,
                    'incentivise': 0
                },
                'market_investors': {
                    'trade': 60,
                    'hold': 10,
                    'utility': 25,
                    'remove_locked_tokens': 5,
                    'incentivise': 0
                },
                'airdrop_receivers': {
                    'trade': 60,
                    'hold': 10,
                    'utility': 25,
                    'remove_locked_tokens': 5,
                    'incentivise': 0
                },
                'incentivisation_receivers': {
                    'trade': 60,
                    'hold': 10,
                    'utility': 25,
                    'remove_locked_tokens': 5,
                    'incentivise': 0
                }
            }
        
        elif params['agent_behavior'] == 'static':
            """
            Define the agent behavior for each agent type for the static 1:1 QTM behavior
            """
            agents = prev_state['agents'].copy()
            
            # initialize agent behavior dictionary
            agent_behavior_dict = {}

            # populate agent behavior dictionary
            for agent in agents:
                agent_behavior_dict[agent] = {
                    'sell': params['avg_token_selling_allocation'],
                    'hold': params['avg_token_holding_allocation'],
                    'utility': params['avg_token_utility_allocation'],
                    'remove_tokens': params['avg_token_utility_removal'],
                }

                # consistency check for agent metabucket behavior
                if agent_behavior_dict[agent]['sell'] + agent_behavior_dict[agent]['hold'] + agent_behavior_dict[agent]['utility'] != 1.0:
                    raise ValueError(f"Agent meta bucket behavior for agent {agent} does not sum up to 100% ({(agent_behavior_dict[agent]['sell'] + agent_behavior_dict[agent]['hold'] + agent_behavior_dict[agent]['utility'])*100.0}).")
                
        else:
            raise ValueError("params['agent_behavior'] must be either 'stochastic' or 'static'.")
    
    except KeyError as e:
        raise KeyError(f"Missing required parameter: {e}")

    return {'agent_behavior_dict': agent_behavior_dict}

def agent_meta_bucket_allocations(params, substep, state_history, prev_state, **kwargs):
    """
    Define the meta bucket token allocations of all agents with respect to 'sell',
    'hold' and 'utility'.    

    Policy function.

    Updates agent token allocations and updates the meta bucket allocations w.r.t. each agents contribution.
    Note that protocol buckets are not used for meta bucket allocations

    Returns: 
        A dict which allows to group the agents according to the following keys: 
        'meta_bucket_allocations','agent_allocations', 'agent_from_holding_allocations'. 
        Each agent from any of these groups reports the allocations for 'sell',
        'hold' and 'utility'.    


    """

    # get state variables
    agents = prev_state['agents']

    # initialize meta bucket token allocations
    meta_bucket_allocations= {
        'selling': 0,
        'holding': 0,
        'utility': 0
    }

    # update agent token allocations and update the meta bucket allocations w.r.t. each agents contribution
    # note that protocol buckets are not used for meta bucket allocations
    agent_allocations = {}
    agent_from_holding_allocations = {}
    sell_from_holding_sum = 0
    utility_from_holding_sum = 0
    hold_from_holding_sum = 0
    for agent in agents:
        # get agent static behavior percentages
        selling_perc = agents[agent]['a_actions']['sell']
        utility_perc = agents[agent]['a_actions']['utility']
        hold_perc = agents[agent]['a_actions']['hold']

        if agents[agent]['a_type'] == 'early_investor' or agents[agent]['a_type'] == 'team':
            # calculate corresponding absolute token amounts for meta buckets
            # agent meta bucket allocations are based on the agents vested tokens
            sell_tokens = agents[agent]['a_tokens_vested'] * selling_perc
            utility_tokens = agents[agent]['a_tokens_vested'] * utility_perc
            holding_tokens = agents[agent]['a_tokens_vested'] * hold_perc
        
        else:
            # calculate corresponding absolute token amounts for meta buckets
            sell_tokens = 0
            utility_tokens = 0
            holding_tokens = 0
        
        # update agent token allocations
        agent_allocations[agent] = {
            'selling': sell_tokens,
            'holding': holding_tokens,
            'utility': utility_tokens,
        }

        # get token meta bucket allocations from agent holding balances of previous timestep
        # get token holding amount from previous timestep (t - 1)
        if agents[agent]['a_type'] != 'protocol_bucket':
            a_token_holdings_tm1 = agents[agent]['a_tokens'] - agents[agent]['a_tokens_vested']
            agent_from_holding_allocations[agent] = {
                'selling': a_token_holdings_tm1 * selling_perc,
                'holding': a_token_holdings_tm1 * hold_perc,
                'utility': a_token_holdings_tm1 * utility_perc,
            }
            sell_from_holding_sum += agent_from_holding_allocations[agent]['selling']
            utility_from_holding_sum += agent_from_holding_allocations[agent]['utility']
            hold_from_holding_sum += agent_from_holding_allocations[agent]['holding']
        
        # populate meta bucket allocations
        meta_bucket_allocations['selling'] += sell_tokens + [agent_from_holding_allocations[agent]['selling'] if agent in agent_from_holding_allocations else 0][0]
        meta_bucket_allocations['holding'] += holding_tokens + [agent_from_holding_allocations[agent]['holding'] if agent in agent_from_holding_allocations else 0][0]
        meta_bucket_allocations['utility'] += utility_tokens + [agent_from_holding_allocations[agent]['utility'] if agent in agent_from_holding_allocations else 0][0]
    
    return {'meta_bucket_allocations': meta_bucket_allocations, 'agent_allocations': agent_allocations, 'agent_from_holding_allocations': agent_from_holding_allocations}



# STATE UPDATE FUNCTIONS
def update_agent_meta_bucket_behavior(params, substep, state_history, prev_state, policy_input, **kwargs):
    """
    Function to update the agent behaviors. 
    
    State update function.

    Returns:
        A tuple ('agents', updated_agents), where updated_agents is a dict mapping
        each agent to their updated behaviour.
    

    """
    updated_agents = prev_state['agents']
    agent_behavior_dict = policy_input['agent_behavior_dict']

    for key in updated_agents:
        updated_agents[key]['a_actions'] = agent_behavior_dict[key]

    return ('agents', updated_agents)

def update_agent_meta_bucket_allocations(params, substep, state_history, prev_state, policy_input, **kwargs):
    """
    Function to update the agent meta bucket token allocations.

    State update function.

    Returns: 
        A tuple ('agents', updated_agents), where updated_agents is a dict mapping
        each agent to their updated meta bucket token allocation.
    """
    
    # get state variables
    updated_agents = prev_state['agents'].copy()
    
    # get policy inputs
    agent_allocations = policy_input['agent_allocations']
    agent_from_holding_allocations = policy_input['agent_from_holding_allocations']

    for key in updated_agents:
        # update agent token allocations
        updated_agents[key]['a_selling_tokens'] = agent_allocations[key]['selling']
        updated_agents[key]['a_utility_tokens'] = agent_allocations[key]['utility']
        updated_agents[key]['a_holding_tokens'] = agent_allocations[key]['holding']
        updated_agents[key]['a_selling_from_holding_tokens'] = [agent_from_holding_allocations[key]['selling'] if key in agent_from_holding_allocations else 0][0]
        updated_agents[key]['a_utility_from_holding_tokens'] = [agent_from_holding_allocations[key]['utility'] if key in agent_from_holding_allocations else 0][0]
        updated_agents[key]['a_holding_from_holding_tokens'] = [agent_from_holding_allocations[key]['holding'] if key in agent_from_holding_allocations else 0][0]
        updated_agents[key]['a_tokens'] -= (agent_allocations[key]['selling'] + agent_allocations[key]['utility']
                                            + [agent_from_holding_allocations[key]['selling'] + agent_from_holding_allocations[key]['utility'] if key in agent_from_holding_allocations else 0][0])

        if prev_state['timestep'] < 5:
            print(f"Agent {updated_agents[key]['a_name']}: updated_agents[key]['a_selling_tokens']: {updated_agents[key]['a_selling_tokens']}, updated_agents[key]['a_utility_tokens']: {updated_agents[key]['a_utility_tokens']}, updated_agents[key]['a_holding_tokens']: {updated_agents[key]['a_holding_tokens']}, updated_agents[key]['a_selling_from_holding_tokens']: {updated_agents[key]['a_selling_from_holding_tokens']}, updated_agents[key]['a_utility_from_holding_tokens']: {updated_agents[key]['a_utility_from_holding_tokens']}, updated_agents[key]['a_holding_from_holding_tokens']: {updated_agents[key]['a_holding_from_holding_tokens']}, updated_agents[key]['a_tokens']: {updated_agents[key]['a_tokens']}")
    return ('agents', updated_agents)


def update_token_economy_meta_bucket_allocations(params, substep, state_history, prev_state, policy_input, **kwargs):
    """
    Function to update the meta bucket allocations for the token economy.

    State update function.

    Returns: 
        A tuple ('token_economy', updated_token_economy), where updated_token_economy is
        a dict providing values of updated meta bucket allocations for, respectively,
        token economy selling/utility/holding allocations and their cumulative values.
    """

    # get state variables
    updated_token_economy = prev_state['token_economy'].copy()

    # get policy inputs
    updated_meta_bucket_allocations = policy_input['meta_bucket_allocations']

    updated_token_economy['te_selling_allocation'] = updated_meta_bucket_allocations['selling']
    updated_token_economy['te_utility_allocation'] = updated_meta_bucket_allocations['utility']
    updated_token_economy['te_holding_allocation'] = updated_meta_bucket_allocations['holding']
    updated_token_economy['te_selling_allocation_cum'] += updated_meta_bucket_allocations['selling']
    updated_token_economy['te_utility_allocation_cum'] += updated_meta_bucket_allocations['utility']
    updated_token_economy['te_holding_allocation_cum'] += updated_meta_bucket_allocations['holding']

    return ('token_economy', updated_token_economy)
