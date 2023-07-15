from .utils import *



# POLICY FUNCTIONS
def business_assumption_metrics(params, substep, state_history, prev_state, **kwargs):


    product_income_per_month = params['product_income_per_month']
    royalty_income_per_month = params['royalty_income_per_month']
    other_income_per_month = params['other_income_per_month']
    treasury_income_per_month = params['treasury_income_per_month']
    regular_income_sum = params['regular_income_sum']
    one_time_payments_1 = params['one_time_payments_1']
    one_time_payments_2 = params['one_time_payments_2']
    salaries_per_month = params['salaries_per_month']
    license_costs_per_month = params['license_costs_per_month']
    other_monthly_costs = params['other_monthly_costs']
    buyback_type = params['buyback_type']
    buyback_perc_per_month = params['buyback_perc_per_month']
    buyback_fixed_per_month = params['buyback_fixed_per_month']
    buyback_bucket = params['buyback_bucket']
    buyback_start = 0 #params['buyback_start']    #issue that buy back start and end is in a regular dates
    buyback_end = 10*12 #params['buyback_end']
    burn_per_month = params['burn_per_month']
    burn_start = params['burn_start']
    burn_end = params['burn_end']
    burn_project_bucket = params['burn_project_bucket']



    current_month = prev_state['timestep']

    if current_month == 1:

        liquidity_pool_fund_allocation = params['initial_token_price']/params['initial_lp_token_allocation']
        print("pool: ",liquidity_pool_fund_allocation)

        sum_of_raised_capital = calculate_raised_capital(params) #Should this be a state variable? It is beign referenced twice
        print("raised capital: ",sum_of_raised_capital)

        cash_balance = (sum_of_raised_capital - liquidity_pool_fund_allocation - one_time_payments_1
                                - one_time_payments_2 - salaries_per_month - license_costs_per_month
                                - other_monthly_costs + royalty_income_per_month + other_income_per_month
                                + treasury_income_per_month)

    else:
        
        prev_cash_balance = prev_state['business_assumptions']['cash_balance']

        buybacks = 0
        if buyback_start <= current_month and buyback_end > current_month:
            if buyback_type == "Fixed":
                buybacks = buyback_fixed_per_month
            else:
                buybacks = prev_cash_balance * buyback_perc_per_month / 100




        product_revenue = prev_state['user_adoption']['product_revenue']


        cash_balance = (
        prev_cash_balance +
        royalty_income_per_month +
        other_income_per_month +
        treasury_income_per_month -
        salaries_per_month -
        license_costs_per_month -
        other_monthly_costs-
        buybacks +
        product_revenue)

    return {'cash_balance': cash_balance}



# STATE UPDATE FUNCTIONS
def update_business_assumptions(params, substep, state_history, prev_state, policy_input, **kwargs):

    cash_balance = policy_input['cash_balance']

    
    updated_business_assumptions = {
        'cash_balance': cash_balance
    }

    return ('business_assumptions', updated_business_assumptions)
