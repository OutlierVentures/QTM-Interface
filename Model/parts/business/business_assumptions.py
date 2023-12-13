"""Set business assumption metrics or update business assumptions.

Contains policy functions (PF) and state update functions (SUF) 
relevant for behaviour of each type of agent and for meta bucket allocations.


Functions:
    business_assumption_metrics: (PF): Set up the business assumption metrics.

    update_business_assumptions: (SUF): Update the business assumptions.

"""


from ..utils import *



# POLICY FUNCTIONS
def business_assumption_metrics(params, substep, state_history, prev_state, **kwargs):
    """
    Set up the business assumption metrics.

    Policy function.

    Reads a range of parameters (originally from QTM input tab 'cadCAD_inputs'), and
    the state of: cash balance, revenue streams. 
    Then calculates: expenditures, buyback, liquidity requirements, sum of raised capital,
    and cash flow.

    Returns:
        Returns dict that maps 'cash_flow' to 'buybacks' to their respective values for
        the current time step.

    """

    # parameters
    royalty_income_per_month = params['royalty_income_per_month']
    other_income_per_month = params['other_income_per_month']
    treasury_income_per_month = params['treasury_income_per_month']
    one_time_payments_1 = params['one_time_payments_1']
    one_time_payments_2 = params['one_time_payments_2']
    salaries_per_month = params['salaries_per_month']
    license_costs_per_month = params['license_costs_per_month']
    other_monthly_costs = params['other_monthly_costs']
    buyback_type = params['buyback_type']
    buyback_perc_per_month = params['buyback_perc_per_month']
    buyback_fixed_per_month = params['buyback_fixed_per_month']
    buyback_start = pd.to_datetime(params['buyback_start'], format='%d.%m.%Y')
    buyback_end = pd.to_datetime(params['buyback_end'], format='%d.%m.%Y')
    token_launch = params['token_launch'] if 'token_launch' in params else True

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
    
    # Ensure that revenue from royalties etc, is never negative
    Revenue_Streams = max(royalty_income_per_month + other_income_per_month + treasury_income_per_month, 0)

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
    required_liquidity_pool_fund_allocation = initial_lp_token_allocation * initial_token_price if token_launch else 0

    # calculate the cash flow for the month
    if current_month == 1:
        cash_flow = (- required_liquidity_pool_fund_allocation + Revenue_Streams +
                      product_revenue - (Expenditures + one_time_payments_1 + one_time_payments_2 + buybacks))

    elif current_month > 1:
        cash_flow = Revenue_Streams + product_revenue - (Expenditures + buybacks)

    return {'cash_flow': cash_flow, 'buybacks': buybacks}


# STATE UPDATE FUNCTIONS
def update_business_assumptions(params, substep, state_history, prev_state, policy_input, **kwargs):
    """
    Function to update the business assumptions.

    State update function.

    Uses cash flow and buyback variables to update business assumptions.

    Returns:
        Returns a tuple ('business_assumptions', updated_business_assumptions),
        where updated_business_assumptions gives latest buybacks and updated cash flow.

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
