# POLICIY FUNCTIONS
def vest_tokens(params, substep, state_history, prev_state, **kwargs):
    """
    Policy function to vest tokens for each stakeholder.
    """
    
    agents = prev_state['agents']
    token_economy = prev_state['token_economy']
    total_token_supply = params['initial_total_supply']
    current_month = prev_state['timestep']
    
    agent_token_vesting_dict = {}
    for key, agent in agents.items():
        # Get all invesotor info
        agent_type = agent['a_name']
        agent_tokens_vested = agent['a_tokens_vested']
        agent_token_allocation = [params[agent_type+"_token_allocation"] if agent_type+"_token_allocation" in params else 0][0]
        agent_initial_vesting_perc = [params[agent_type+"_initial_vesting"] if agent_type+"_initial_vesting" in params else 0][0]
        agent_cliff_months = [params[agent_type+"_cliff"] if agent_type+"_cliff" in params else 0][0]
        agent_vesting_duration = [params[agent_type+"_vesting_duration"] if agent_type+"_vesting_duration" in params else 0][0]

        # initial vesting
        if current_month == 1:
            initial_agent_tokens_vested = (agent_initial_vesting_perc / 100) * (agent_token_allocation * total_token_supply)
            agent_token_vesting_dict[key] = initial_agent_tokens_vested

        # Parameter integrity checks
        if agent_vesting_duration <= 0 and agent_initial_vesting_perc <= 0:
            vesting_period_token_amount = 0
        elif agent_vesting_duration <= 0 and agent_initial_vesting_perc != 100:
            print("ERROR: agent "+str(agent_type)+" vesting duration is 0 but initial vesting percentage is not 100%! It is "+str(agent_initial_vesting_perc)+"%. Setting vesting amount to 0.")
            vesting_period_token_amount = 0
        elif agent_vesting_duration <= 0:
            agent_vesting_duration = 0
        else:
            vesting_period_token_amount = (agent_token_allocation * total_token_supply - (agent_initial_vesting_perc / 100 * agent_token_allocation* total_token_supply)) / agent_vesting_duration
        
        if (current_month > agent_cliff_months + agent_vesting_duration) or current_month <= agent_cliff_months:
            vesting_period_token_amount = 0

        agent_token_vesting_dict[key] = [vesting_period_token_amount + agent_token_vesting_dict[key] if key in agent_token_vesting_dict else vesting_period_token_amount][0]

    return {'agent_token_vesting_dict': agent_token_vesting_dict}

# STATE UPDATE FUNCTIONS
def update_agent_vested_tokens(params, substep, state_history, prev_state, policy_input, **kwargs):
    """
    Function to update the vested tokens for each investor based on some criteria
    """
    updated_agents = prev_state['agents']
    agent_token_vesting_dict = policy_input['agent_token_vesting_dict']

    for key, value in agent_token_vesting_dict.items():
        updated_agents[key]['a_tokens'] += value
        updated_agents[key]['a_tokens_vested'] = value
        updated_agents[key]['a_tokens_vested_cum'] += value

    return ('agents', updated_agents)