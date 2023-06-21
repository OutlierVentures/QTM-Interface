# POLICIY FUNCTIONS

def vest_tokens(params, substep, state_history, prev_state, **kwargs):
    
    agents = prev_state['agents']
    token_economy = prev_state['token_economy']

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

        vesting_period_token_amount = agent_token_allocation - (agent_initial_vesting_perc / 100 * params['total_token_supply'])
        
        if total_months != 0:
            current_vesting_percent = (current_month-cliff_in_months)/total_months

        # (4-3)/10 = 1/10 then vest 10%
        # (4 - 10) / 9 = then - num, cant vest yet
        # (10-6) / 3 = % greater than 1, vest the whole thing



            
        if current_vesting_percent <= 0:
            # Investor gets their initial amount vested
            tokens_to_vest = initial_vesting_tokens


        elif current_vesting_percent < 1:
            # Investor is eligible to receive a portion of their vested tokens based on the vesting schedule
            tokens_to_vest = (current_vesting_percent* vesting_period_token_amount) + initial_vesting_tokens

        else:
            # Investor is fully vested
            tokens_to_vest = total_token_amount

        # Update the investor's current allocation
        investor['current_allocation'] = tokens_to_vest




    token_economy['current_circulating_supply'] = sum([investor['current_allocation'] for i, investor in investors.items()])


    # Update the state variables
    updated_investors = investors
    updated_token_economy = token_economy

    return {'updated_investors': updated_investors,'updated_token_economy': updated_token_economy}

# STATE UPDATE FUNCTIONS
def update_investor_tokens(params, substep, state_history, prev_state, policy_input, **kwargs):
    # Function to update the vested tokens for each investor based on some criteria
    # ...
    updated_investors = policy_input['updated_investors']

    return ('investors', updated_investors)

def update_token_economy(params, substep, state_history, prev_state, policy_input, **kwargs):
    # Function to update the vested tokens for each investor based on some criteria
    updated_economy = policy_input['updated_token_economy']
    return ('token_economy', updated_economy)