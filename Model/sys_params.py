
initial_investors = {
         'Public Sale': {
         'percentage_allocation': .035,
         'initial_vesting': .25,
         'cliff_in_months': 0,
         'total_months': 6,
         'current_allocation': 0,
         'type':"Investor",
         'subtype': "Public Sale",
         'total_token_amount':0,
         'capital_raise': 2100000,
         'valuation_cap': 60000000,
         'bonus_amount':0,
         'effective_token_price':0,
         'token_discount_perc':0 },
        
        'Liquidity Pool': {
         'percentage_allocation': 0,
         'initial_vesting': 1,
         'cliff_in_months': 0,
         'total_months': 0,
         'current_allocation': 0,
         'type':"Investor",
         'subtype': "Public Sale",
         'total_token_amount':0,
         'capital_raise': 0,
         'valuation_cap': 0,
         'bonus_amount':0,
         'effective_token_price':0,
         'token_discount_perc':0 },

         'Angels': {
         'percentage_allocation': 0,
         'initial_vesting': 0,
         'cliff_in_months': 1,
         'total_months': 24,
         'current_allocation': 0,
         'type':"Investor",
         'subtype': "Angel",
         'total_token_amount':0,
         'capital_raise': 250000,
         'valuation_cap': 0,
         'bonus_amount':0,
         'effective_token_price':0,
         'token_discount_perc':0 },
        
        'Seed': { 
         'percentage_allocation': 0,
         'initial_vesting': 0,
         'cliff_in_months': 1,
         'total_months': 24,
         'current_allocation': 0,
         'capital_raise': 0,
         'valuation_cap': 0,
         'type':"Investor",
         'subtype': "Fundrasing",
         'total_token_amount':0,
         'capital_raise': 750000,
         'valuation_cap': 30000000,
         'bonus_amount':0.5,
         'effective_token_price':0,
         'token_discount_perc':0 },
        
         'Pre-Sale 1': {
         'percentage_allocation': 0,
         'initial_vesting': 0,
         'cliff_in_months': 1,
         'total_months': 12,
         'current_allocation': 0,
         'capital_raise': 0,
         'valuation_cap': 0,
         'type':"Investor",
         'subtype': "Fundrasing",
         'total_token_amount':0,
         'capital_raise': 1500000,
         'valuation_cap': 40000000,
         'bonus_amount':0.25,
         'effective_token_price':0,
         'token_discount_perc':0 },

         'Pre-Sale 2': {
         'percentage_allocation': 0,
         'initial_vesting': 0,
         'cliff_in_months': 1,
         'total_months': 9,
         'current_allocation': 0,
         'capital_raise': 0,
         'valuation_cap': 0,
         'type':"Investor",
         'subtype': "Fundrasing",
         'total_token_amount':0,
         'capital_raise': 2500000,
         'valuation_cap': 50000000,
         'bonus_amount':0.15,
         'effective_token_price':0,
         'token_discount_perc':0 },

         'Founders': {
         'percentage_allocation': .25,
         'initial_vesting': 0,
         'cliff_in_months': 6,
         'total_months': 36,
         'current_allocation': 0,
         'capital_raise': 0,
         'valuation_cap': 0,
         'type':"Investor",
         'subtype': "None",
         'total_token_amount':0,
         'capital_raise': 0,
         'valuation_cap': 0,
         'bonus_amount':0,
         'effective_token_price':0,
         'token_discount_perc':0 },

         'Advisors': {
         'percentage_allocation': 0.01,
         'initial_vesting': 0,
         'cliff_in_months': 1,
         'total_months': 24,
         'current_allocation': 0,
         'capital_raise': 0,
         'valuation_cap': 0,
         'type':"Investor",
         'subtype': "None",
         'total_token_amount':0,
         'capital_raise': 0,
         'valuation_cap': 0,
         'bonus_amount':0,
         'effective_token_price':0,
         'token_discount_perc':0 },

         'Reserve': {
         'percentage_allocation': 0.4,
         'initial_vesting': 1,
         'cliff_in_months': 0,
         'total_months': 0,
         'current_allocation': 0,
         'capital_raise': 0,
         'valuation_cap': 0,
         'type':"Project Buckets",
         'subtype': "None",
         'total_token_amount':0,
         'capital_raise': 0,
         'valuation_cap': 0,
         'bonus_amount':0,
         'effective_token_price':0,
         'token_discount_perc':0 }

    }
    
token_economy = {
    'initial_token_supply': 100000000, # Total number of tokens initially in the economy
    'public_sale_valuation': 60000000,
    'current_circulating_supply':0,
    'external_equity': .1,
    'inflation': 'Fixed',
    'sum_of_raised_capital':0
}

liquidity_pool ={
    'token_lp_weighting': .5,
    'lp_paring_token_ticker': 'USDC',
    'lp_paring_token_price': 1
}



# System parameters
sys_param = {
    'token_economy': token_economy,
    'initial_investors':initial_investors,
    'liquidity_pool': liquidity_pool  
    
}
