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
    cash flow, and revenue splits

    Returns:
        cash flow, fixed and variable revenue streams,
        fixed and variable expenditures, buybacks, and revenue splits.

    """
    # state variables 1
    current_month = prev_state['timestep']
    agents = prev_state['agents'].copy()
    liquidity_pool = prev_state['liquidity_pool'].copy()

    # parameters
    token_launch = params['token_launch'] if 'token_launch' in params else True
    royalty_income_per_month = params['royalty_income_per_month']
    other_income_per_month = params['other_income_per_month']
    treasury_income_per_month = params['treasury_income_per_month']
    one_time_payments_1 = params['one_time_payments_1'] if (token_launch and current_month == 1) else 0
    one_time_payments_2 = params['one_time_payments_2'] if (token_launch and current_month == 1) else 0
    salaries_per_month = params['salaries_per_month']
    license_costs_per_month = params['license_costs_per_month']
    other_monthly_costs = params['other_monthly_costs']
    buyback_type = params['buyback_type']
    buyback_perc_per_month = params['buyback_perc_per_month']
    buyback_fixed_per_month = params['buyback_fixed_per_month']
    buyback_start = pd.to_datetime(params['buyback_start'], format='%d.%m.%Y')
    buyback_end = pd.to_datetime(params['buyback_end'], format='%d.%m.%Y')
    buyback_bucket = params['buyback_bucket']

    initial_lp_token_allocation = params['initial_lp_token_allocation']
    initial_token_price = params['initial_token_price']
    initial_total_supply = params['initial_total_supply']
    initial_incentivisation_allocation = params['incentivisation_token_allocation'] * initial_total_supply
    initial_staking_vesting_allocation = params['staking_vesting_token_allocation'] * initial_total_supply

    # check if revenue share is used for buying back tokens
    if 'staker_rev_share_buyback' in params:
        staker_rev_share_buyback = params['staker_rev_share_buyback'] # boolean if revenue share to be used for buying back the token to distribute tokens instead of revenue in diverse assets to stakers
    else:
        staker_rev_share_buyback = True
    if 'incentivisation_rev_share_buyback' in params:
        incentivisation_rev_share_buyback = params['incentivisation_rev_share_buyback'] # boolean if revenue share to be used for buying back the token to distribute tokens instead of revenue in diverse assets to stakers
    else:
        incentivisation_rev_share_buyback = False


    # revenue share splits
    staker_rev_share = params['staker_rev_share']
    if 'business_rev_share' in params:
        business_rev_share = params['business_rev_share']
    else:
        business_rev_share = 100 - staker_rev_share
    if 'service_provider_rev_share' in params:
        service_provider_rev_share = params['service_provider_rev_share']
    else:
        service_provider_rev_share = 0
    if 'incentivisation_rev_share' in params:
        incentivisation_rev_share = params['incentivisation_rev_share']
    else:
        incentivisation_rev_share = 0

    # state variables
    date = prev_state['date']
    prev_cash_balance = prev_state['business_assumptions']['ba_cash_balance']
    product_revenue = prev_state['user_adoption']['ua_product_revenue']
    agents = prev_state['agents'].copy()
    staking_vesting_agent = agents[[agent for agent in agents if agents[agent]['a_name'].lower() == 'staking_vesting'][0]]
    staking_vesting_bucket_tokens = initial_staking_vesting_allocation - staking_vesting_agent['a_tokens_vested_cum'] + staking_vesting_agent['a_tokens_vested'] # calculate the amount of tokens in the staking vesting bucket
    incentivisation_agent = agents[[agent for agent in agents if agents[agent]['a_name'].lower() == 'incentivisation'][0]]
    incentivisation_vesting_bucket_tokens = initial_incentivisation_allocation - incentivisation_agent['a_tokens_vested_cum'] + incentivisation_agent['a_tokens_vested'] # calculate the amount of tokens in the incentivisation vesting bucket
 
    # policy logic
    # fixed expenditures
    ## liquidity capital requirement
    required_liquidity_pool_fund_allocation = initial_lp_token_allocation * initial_token_price if (token_launch and current_month == 1) else 0

    fixed_business_expenditures = (salaries_per_month + license_costs_per_month
                                   + other_monthly_costs + required_liquidity_pool_fund_allocation
                                   + one_time_payments_1 + one_time_payments_2 )
    
    # fixed revenue streams - Ensure that revenue from royalties etc, is never negative
    fixed_business_revenue = max(royalty_income_per_month + other_income_per_month + treasury_income_per_month, 0)
    
    # variable revenues
    ## split of variable revenue streams from product revenue
    var_business_revenue = product_revenue * business_rev_share / 100
    var_staker_revenue = product_revenue * staker_rev_share / 100 if staking_vesting_bucket_tokens <= 0 else 0.0
    var_service_provider_revenue = product_revenue * service_provider_rev_share / 100
    var_incentivisation_revenue = product_revenue * incentivisation_rev_share / 100 if incentivisation_vesting_bucket_tokens <= 0 else 0.0
    var_business_revenue += product_revenue * staker_rev_share / 100 if staking_vesting_bucket_tokens > 0 else 0.0
    var_business_revenue += product_revenue * incentivisation_rev_share / 100 if incentivisation_vesting_bucket_tokens > 0 else 0.0

    np.testing.assert_allclose(var_business_revenue + var_staker_revenue + var_service_provider_revenue + var_incentivisation_revenue, product_revenue, rtol=0.0001, err_msg=f'Revenue split is not correct: business_revenue({var_business_revenue}) + staker_revenue({var_staker_revenue}) + service_provider_revenue({var_service_provider_revenue}) + incentivisation_revenue({var_incentivisation_revenue}) != product_revenue({product_revenue})')

    # buybacks for staking vesting
    staker_rev_share_buyback_amount = var_staker_revenue if staker_rev_share_buyback else 0.0 # revenue share to be used for buybacks to distribute tokens instead of revenue in diverse assets to stakers

    # buybacks for ecosystem incentivisation from revenue
    incentivisation_rev_share_buyback_amount = var_incentivisation_revenue if incentivisation_rev_share_buyback else 0.0 # revenue share to be used for buybacks to distribute tokens instead of revenue in diverse assets as incentivisation into the economy
    
    # business buybacks
    business_buybacks = 0 # business buybacks are not included in the buyback_from_revenue_share variable as they are performed on top of the revenue share buybacks by the protocol/business

    if buyback_start <= date and buyback_end > date:
        if buyback_type == "Fixed":
            business_buybacks += buyback_fixed_per_month

        elif buyback_type == "Percentage":
            business_buybacks += prev_cash_balance * buyback_perc_per_month / 100
            
        else:
            raise ValueError('The buyback type is not defined!')
        
        # check if the business has enough cash to perform the buyback
        business_buybacks = min(business_buybacks, prev_cash_balance)

        # check if the business has enough tokens to sell in case of a negative business buyback
        if business_buybacks < 0:
            buyback_bucket_agent_tokens = [agents[agent]['a_tokens'] for agent in agents if agents[agent]['a_name'].lower() in buyback_bucket.lower()][0]
            buyback_bucket_agent_tokens = buyback_bucket_agent_tokens if buyback_bucket_agent_tokens > 0 else 0
            if buyback_bucket_agent_tokens * liquidity_pool['lp_token_price'] < np.abs(business_buybacks) and buyback_bucket_agent_tokens > 1:
                business_buybacks = -buyback_bucket_agent_tokens * liquidity_pool['lp_token_price']
            elif buyback_bucket_agent_tokens * liquidity_pool['lp_token_price'] < np.abs(business_buybacks) and buyback_bucket_agent_tokens <= 1:
                business_buybacks = 0
            var_business_revenue += -business_buybacks

    business_revenue = fixed_business_revenue + var_business_revenue - business_buybacks if business_buybacks < 0 else fixed_business_revenue + var_business_revenue
    business_expenditures = fixed_business_expenditures + business_buybacks if business_buybacks > 0 else fixed_business_expenditures

    # calculate the cash flow for the month
    cash_flow = business_revenue - business_expenditures

    # calculate buyback sum
    buybacks = business_buybacks + staker_rev_share_buyback_amount + incentivisation_rev_share_buyback_amount if business_buybacks > 0 else staker_rev_share_buyback_amount + incentivisation_rev_share_buyback_amount

    var_business_expenditures = business_buybacks if business_buybacks >0 else 0

    return {'cash_flow': cash_flow, 'fixed_business_revenue': fixed_business_revenue, 'var_business_revenue': var_business_revenue,
            'fixed_business_expenditures': fixed_business_expenditures, 'var_business_expenditures': var_business_expenditures, 'business_buybacks_usd': business_buybacks,
            'buybacks': buybacks, 'var_staker_revenue': var_staker_revenue,
            'var_service_provider_revenue': var_service_provider_revenue, 'var_incentivisation_revenue': var_incentivisation_revenue,
            'u_buyback_from_revenue_share_staking_usd': staker_rev_share_buyback_amount, 'ba_buyback_from_revenue_share_incentivisation_usd': incentivisation_rev_share_buyback_amount}


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
    updated_business_assumptions = prev_state['business_assumptions'].copy()

    # policy variables
    cash_flow = policy_input['cash_flow']
    fixed_business_revenue = policy_input['fixed_business_revenue']
    var_business_revenue = policy_input['var_business_revenue']
    fixed_business_expenditures = policy_input['fixed_business_expenditures']
    var_business_expenditures = policy_input['var_business_expenditures']
    var_staker_revenue = policy_input['var_staker_revenue']
    var_service_provider_revenue = policy_input['var_service_provider_revenue']
    var_incentivisation_revenue = policy_input['var_incentivisation_revenue']
    buybacks = policy_input['buybacks']
    business_buybacks_usd = policy_input['business_buybacks_usd']
    buyback_from_revenue_share_incentivisation_usd = policy_input['ba_buyback_from_revenue_share_incentivisation_usd']

    # update logic
    updated_business_assumptions['ba_cash_flow'] = cash_flow
    updated_business_assumptions['ba_cash_balance'] += cash_flow

    updated_business_assumptions['ba_buybacks_usd'] = buybacks
    updated_business_assumptions['ba_buybacks_cum_usd'] += buybacks

    updated_business_assumptions['ba_fix_expenditures_usd'] = fixed_business_expenditures
    updated_business_assumptions['ba_fix_expenditures_cum_usd'] += fixed_business_expenditures
    updated_business_assumptions['ba_var_expenditures_usd'] = var_business_expenditures
    updated_business_assumptions['ba_var_expenditures_cum_usd'] += var_business_expenditures

    updated_business_assumptions['ba_fix_business_revenue_usd'] = fixed_business_revenue
    updated_business_assumptions['ba_fix_business_revenue_cum_usd'] += fixed_business_revenue
    updated_business_assumptions['ba_var_business_revenue_usd'] = var_business_revenue
    updated_business_assumptions['ba_var_business_revenue_cum_usd'] += var_business_revenue

    updated_business_assumptions['ba_staker_revenue_usd'] = var_staker_revenue
    updated_business_assumptions['ba_staker_revenue_cum_usd'] += var_staker_revenue

    updated_business_assumptions['ba_service_provider_revenue_usd'] = var_service_provider_revenue
    updated_business_assumptions['ba_service_provider_revenue_cum_usd'] += var_service_provider_revenue

    updated_business_assumptions['ba_incentivisation_revenue_usd'] = var_incentivisation_revenue
    updated_business_assumptions['ba_incentivisation_revenue_cum_usd'] += var_incentivisation_revenue

    updated_business_assumptions['ba_business_buybacks_usd'] = business_buybacks_usd

    updated_business_assumptions['ba_buyback_from_revenue_share_incentivisation_usd'] = buyback_from_revenue_share_incentivisation_usd

    return ('business_assumptions', updated_business_assumptions)



def update_buyback_amount_from_revenue_share(params, substep, state_history, prev_state, policy_input, **kwargs):
    """
    Function to update capital amount for token buybacks from the revenue share
    """
    # get parameters

    # get state variables
    updated_utilities = prev_state['utilities'].copy()

    # get policy input
    buyback_from_revenue_share_usd = policy_input['u_buyback_from_revenue_share_staking_usd']

    # update logic
    updated_utilities['u_buyback_from_revenue_share_staking_usd'] = buyback_from_revenue_share_usd

    return ('utilities', updated_utilities)