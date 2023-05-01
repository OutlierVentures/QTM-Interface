




def initial_investor_allocation(initial_investors,initial_token_supply):
    

    for i, investor in initial_investors.items():
        
        percentage_allocation = investor['percentage_allocation']

        total_token_amount = percentage_allocation * initial_token_supply

        
        initial_vesting = investor['initial_vesting']

        investor['current_allocation'] = initial_vesting * total_token_amount



    initial_circulating_supply = sum([investor['current_allocation'] for i, investor in initial_investors.items()])


    return initial_investors, initial_circulating_supply
