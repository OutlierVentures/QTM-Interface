# POLICIY FUNCTIONS
def vest_tokens(params, substep, state_history, prev_state, **kwargs):
    """
    Policy function to vest tokens for each stakeholder.
    """
    
    agents = prev_state['agents']
    token_economy = prev_state['token_economy']

    tokens_vested_in_timestep = 0
    agent_token_vesting_dict = {}
    for key, agent in agents.items():
        # Get all invesotor info
        agent_type = agent['type']
        agent_tokens_vested = agent['tokens_vested']
        agent_token_allocation = params[agent_type+"_token_allocation"]
        agent_initial_vesting_perc = params[agent_type+"_initial_vesting"]
        agent_cliff_months = params[agent_type+"_cliff"]
        agent_vesting_duration = params[agent_type+"_vesting_duration"]
        
        #Create vesting variables
        current_month = prev_state['timestep']

        # Parameter integrity checks
        if agent_vesting_duration <= 0 and agent_initial_vesting_perc <= 0:
            vesting_period_token_amount = 0
        elif agent_vesting_duration <= 0 and agent_initial_vesting_perc != 100:
            print("ERROR: agent "+str(agent_type)+" vesting duration is 0 but initial vesting percentage is not 100%! It is "+str(agent_initial_vesting_perc)+"%. Setting vesting amount to 0.")
            vesting_period_token_amount = 0
        elif agent_vesting_duration <= 0:
            agent_vesting_duration = 0
        else:
            vesting_period_token_amount = (agent_token_allocation - (agent_initial_vesting_perc / 100 * params['total_token_supply'])) / agent_vesting_duration
        
        if (current_month >= agent_cliff_months + agent_vesting_duration) or current_month < agent_cliff_months:
            vesting_period_token_amount = 0


        tokens_vested_in_timestep += vesting_period_token_amount

        agent_token_vesting_dict[key] = vesting_period_token_amount

    return {'tokens_vested_in_timestep': tokens_vested_in_timestep,'agent_token_vesting_dict': agent_token_vesting_dict}

# STATE UPDATE FUNCTIONS
def update_agent_vested_tokens(params, substep, state_history, prev_state, policy_input, **kwargs):
    """
    Function to update the vested tokens for each investor based on some criteria
    """
    updated_agents = prev_state['agents']
    agent_token_vesting_dict = policy_input['agent_token_vesting_dict']

    for key, value in agent_token_vesting_dict.items():
        updated_agents[key]['tokens'] += value
        updated_agents[key]['tokens_vested'] += value


    return ('agents', updated_agents)

def update_token_economy(params, substep, state_history, prev_state, policy_input, **kwargs):
    """
    Function to update the token economy based on the vested tokens.
    """

    updated_economy = prev_state['token_economy']
    tokens_vested_in_timestep = policy_input['tokens_vested_in_timestep']
    
    updated_economy['circulating_supply'] += tokens_vested_in_timestep
    updated_economy['market_cap'] = updated_economy['circulating_supply'] * updated_economy['token_price']

    return ('token_economy', updated_economy)