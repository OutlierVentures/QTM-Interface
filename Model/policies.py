






def vest_tokens(params, substep, state_history, prev_state, **kwargs):
    
    
    

    investors = prev_state['investors']
    token_economy = prev_state['token_economy']

    
    
    
    for i, investor in enumerate(investors):
        # Calculate the number of months since the investor's initial allocation
        months_since_allocation = prev_state['timestep']  # Subtract 1 since the initial state is step 0

        # Calculate the number of tokens the investor is eligible to receive
        if months_since_allocation < investor['cliff_in_months']:
            # Investor is not eligible to receive any tokens during the cliff period
            tokens_to_vest = 0
        elif months_since_allocation < investor['total_months']:
            # Investor is eligible to receive a portion of their tokens based on the vesting schedule
            vesting_period = investor['total_months'] - investor['cliff_in_months']
            months_vested = months_since_allocation - investor['cliff_in_months']
            tokens_to_vest = investor['initial_vesting'] * token_economy['initial_token_supply'] * months_vested / vesting_period
        else:
            # Investor is fully vested
            tokens_to_vest = investor['initial_vesting'] * token_economy['initial_token_supply']

        # Update the investor's current allocation
        investors[i]['current_allocation'] = tokens_to_vest

    # Update the state variables
    token_economy['current_circulating_supply'] = sum([investor['current_allocation'] for investor in investors])

    return {'investors': investors,'token_economy': token_economy}




