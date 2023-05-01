






def vest_tokens(params, substep, state_history, prev_state, **kwargs):
    
    investors = prev_state['investors']
    token_economy = prev_state['token_economy']

    
    #Try 1
    '''
    for i, investor in investors.items():
        


        # Calculate the number of months since the investor's initial allocation
        months_since_allocation = prev_state['timestep']  # Subtract 1 since the initial state is step 0
        # Calculate the number of tokens the investor is eligible to receive
        
        if months_since_allocation < investor['cliff_in_months']:
            # Investor gets their initial amount vested
            tokens_to_vest = (investor['percentage_allocation']*investor['initial_vesting']) * token_economy['initial_token_supply']


        elif months_since_allocation < investor['total_months']:
            # Investor is eligible to receive a portion of their vested tokens based on the vesting schedule
            vesting_period = months_since_allocation - investor['cliff_in_months']

            tokens_to_vest = investor['initial_vesting'] * token_economy['initial_token_supply'] * months_vested / vesting_period

        else:
            # Investor is fully vested
            tokens_to_vest = investor['percentage_allocation'] * token_economy['initial_token_supply']

        # Update the investor's current allocation
        investor['current_allocation'] = tokens_to_vest
        '''



    #Try 2

    for i, investor in investors.items():
        
        # Get all invesotor info
        percentage_allocation = investor['percentage_allocation']
        initial_vesting = investor['initial_vesting']
        cliff_in_months = investor['cliff_in_months']
        total_months = investor['total_months']
        current_allocation = investor['current_allocation']


        #Create vesting variables
        current_month = prev_state['timestep']
        total_token_amount = percentage_allocation * token_economy['initial_token_supply']
        initial_vesting_tokens = initial_vesting * total_token_amount
        vesting_period_token_amount = total_token_amount - initial_vesting_tokens
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




