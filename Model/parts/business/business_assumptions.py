from ..utils import *



# POLICY FUNCTIONS
def business_assumption_metrics(params, substep, state_history, prev_state, **kwargs):

    # parameters
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
    buyback_start = pd.to_datetime(params['buyback_start'], format='%d.%m.%y')
    buyback_end = pd.to_datetime(params['buyback_end'], format='%d.%m.%y')
    burn_per_month = params['burn_per_month']
    burn_start = params['burn_start']
    burn_end = params['burn_end']
    burn_project_bucket = params['burn_project_bucket']
    initial_lp_token_allocation = params['initial_lp_token_allocation']
    initial_token_price = params['initial_token_price']

    # state variables
    current_month = prev_state['timestep']
    date = prev_state['date']
    prev_cash_balance = prev_state['business_assumptions']['ba_cash_balance']
    buyback_from_revenue_share = prev_state['utilities']['u_buyback_from_revenue_share_usd']
    product_revenue = prev_state['user_adoption']['ua_product_revenue']

    # policy logic    
    # expenditures
    Expenditures = (salaries_per_month + license_costs_per_month
                            + other_monthly_costs)
    
    # revenues
    Revenue_Streams = (royalty_income_per_month + other_income_per_month
                                + treasury_income_per_month)

    # buybacks
    buybacks = buyback_from_revenue_share
    if buyback_start <= date and buyback_end > date:
        if buyback_type == "Fixed":
            buybacks += buyback_fixed_per_month
        elif buyback_type == "Percentage":
            buybacks += prev_cash_balance * buyback_perc_per_month / 100
        else:
            raise ValueError('The buyback type is not defined!')

    # liquidity capital requirement
    required_liquidity_pool_fund_allocation = initial_lp_token_allocation * initial_token_price

    # amount of raised capital
    sum_of_raised_capital = calculate_raised_capital(params)

    # calculate the cash flow for the month
    if current_month == 1:
        cash_flow = sum_of_raised_capital - required_liquidity_pool_fund_allocation + Revenue_Streams + product_revenue - (Expenditures + one_time_payments_1 + one_time_payments_2 + buybacks)

    elif current_month > 1:
        cash_flow = Revenue_Streams + product_revenue - (Expenditures + buybacks)

    return {'cash_flow': cash_flow, 'buybacks': buybacks}



# STATE UPDATE FUNCTIONS
def update_business_assumptions(params, substep, state_history, prev_state, policy_input, **kwargs):
    """
    Function to update the business assumptions
    """
    # parameters

    # state variables
    updated_business_assumptions = prev_state['business_assumptions']

    # policy variables
    cash_flow = policy_input['cash_flow']
    buybacks = policy_input['buybacks']

    # update logic
    updated_business_assumptions['ba_buybacks_usd'] = buybacks
    updated_business_assumptions['ba_cash_balance'] += cash_flow

    return ('business_assumptions', updated_business_assumptions)
