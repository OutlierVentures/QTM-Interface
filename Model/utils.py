




def initial_investor_allocation(initial_investors,token_economy):
    initial_token_supply = token_economy['initial_token_supply']
    external_equity = token_economy['external_equity']

    initial_investors = fund_raising(initial_investors,initial_token_supply,external_equity)

    for i, investor in initial_investors.items():

        if investor['percentage_allocation'] == 0 and investor['effective_token_price'] != 0:
            investor['percentage_allocation'] = (investor['capital_raise']/investor['effective_token_price'])/initial_token_supply
        #Need to figure this out


        percentage_allocation = investor['percentage_allocation']
    
        total_token_amount = percentage_allocation * initial_token_supply
        initial_vesting = investor['initial_vesting']
        investor['current_allocation'] = initial_vesting * total_token_amount


    initial_investors = create_liquidity_pool(initial_investors,initial_token_supply)

    token_economy['current_circulating_supply'] = sum([investor['current_allocation'] for i, investor in initial_investors.items()])

    token_economy['sum_of_raised_capital'] = sum([investor['capital_raise'] for i, investor in initial_investors.items()])

    return initial_investors, token_economy







def fund_raising(initial_investors,initial_token_supply,external_equity):


    #need a public sale investor to be intiialized no matter what
    initial_investors['Public Sale']['effective_token_price'] =  initial_investors['Public Sale']['valuation_cap']/initial_token_supply
    initial_investors['Public Sale']['token_discount_perc'] = 0
    public_token_price = initial_investors['Public Sale']['effective_token_price']



    #Go through the rest of the investors that are not public sale
    for i, investor in initial_investors.items():
        

        #Check if its an investor with a fundraise
        investor_type = investor['type']
        investor_subtype = investor['subtype']


        if investor_type == "Investor" and investor_subtype != "Public Sale":


            #deal with angels

            if investor['subtype'] == "Angel":
                investor['percentage_allocation'] = external_equity*(initial_investors['Founders']['percentage_allocation']/(1-external_equity))
                percentage_allocation = investor['percentage_allocation']
                                
                investor['valuation_cap'] = (investor['capital_raise'] / (percentage_allocation*initial_token_supply)) * initial_token_supply
                valuation_cap = investor['valuation_cap']
                
                investor['bonus_amount'] = investor['valuation_cap']/initial_token_supply

                investor['effective_token_price'] = min(public_token_price / investor['bonus_amount'], investor['valuation_cap'] / initial_token_supply)
            else:
                valuation_cap = investor['valuation_cap']
                bonus_amount = investor['bonus_amount']
                #Change other variables
                if bonus_amount !=0:
                    investor['effective_token_price'] = min(public_token_price / bonus_amount, valuation_cap / initial_token_supply)
                else:
                    investor['effective_token_price'] = valuation_cap / initial_token_supply
                
                
            investor['token_discount_perc'] = investor['effective_token_price']/public_token_price



    return initial_investors



def create_liquidity_pool(initial_investors,initial_token_supply):
    percentage_allocation = 0
    percentage_allocation = 1-sum([investor['percentage_allocation'] for i, investor in initial_investors.items()])
    


    initial_investors['Liquidity Pool']['percentage_allocation'] = percentage_allocation
    total_token_amount = percentage_allocation * initial_token_supply
    
    initial_vesting = initial_investors['Liquidity Pool']['initial_vesting']
    initial_investors['Liquidity Pool']['current_allocation']= initial_vesting * total_token_amount
    initial_investors['Liquidity Pool']['total_token_amount']= total_token_amount

    return initial_investors



def liquidity_pool_module(initial_investors,token_economy,liquidity_pool):


    public_sale_valuation = token_economy['public_sale_valuation']
    initial_token_supply = token_economy['initial_token_supply']
    sum_of_raised_capital = token_economy['sum_of_raised_capital']
    current_circulating_supply = token_economy['current_circulating_supply']
    lp_paring_token_price = liquidity_pool['lp_paring_token_price']
    token_lp_weighting = liquidity_pool['token_lp_weighting']




    token_launch_price = public_sale_valuation / initial_token_supply

    liquidity_pool_fund_allocation = token_launch_price*initial_investors['Liquidity Pool']['total_token_amount']*100

    allocation_by_raised_amount = liquidity_pool_fund_allocation/sum_of_raised_capital

    initial_token_MC_price = token_launch_price*current_circulating_supply

    initial_token_FDV_price = initial_token_supply*token_launch_price

    initial_pairing_amount = liquidity_pool_fund_allocation/lp_paring_token_price

    token_pair_weighting = 1-token_lp_weighting


    liquidity_pool_module_data = {
        'token_launch_price': token_launch_price,
        'liquidity_pool_fund_allocation': liquidity_pool_fund_allocation,
        'allocation_by_raised_amount': allocation_by_raised_amount,
        'initial_token_MC_price': initial_token_MC_price,
        'initial_token_FDV_price': initial_token_FDV_price,
        'initial_pairing_amount': initial_pairing_amount,
        'token_pair_weighting': token_pair_weighting
    }



    return liquidity_pool_module_data
