






def vest_tokens(params, substep, state_history, prev_state, **kwargs):
    
    investors = prev_state['investors']
    token_economy = prev_state['token_economy']

    



    for i, investor in investors.items():
        # Get all invesotor info
        percentage_allocation = investor['percentage_allocation']
        initial_vesting = investor['initial_vesting']
        cliff_in_months = investor['cliff_in_months']
        total_months = investor['total_months']
        #current_allocation = investor['current_allocation']

        
        #Create vesting variables
        current_month = prev_state['timestep']
        total_token_amount = percentage_allocation * token_economy['initial_token_supply']
        
        initial_vesting_tokens = initial_vesting * total_token_amount
        vesting_period_token_amount = total_token_amount - initial_vesting_tokens
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




