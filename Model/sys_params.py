import uuid
from parts.utils import *
import pandas as pd

import sys
import os

# Get the current directory
current_dir = os.path.dirname(os.path.abspath(__file__))

# Go up one folder
parent_dir = os.path.abspath(os.path.join(current_dir, os.pardir))

# Append the parent directory to sys.path
sys.path.append(parent_dir)

# Now you can import modules from the desired path
from data.not_iterable_variables import *

QTM_inputs = pd.read_csv(parent_dir+'/data/Quantitative_Token_Model_V1.87 - cadCAD_inputs.csv')

# System parameters
sys_param = compose_initial_parameters(QTM_inputs, parameter_list)

# calculating the token allocations for different agents
agent_token_allocation = {
    'angle_token_allocation': [x/100 * (y/100 / (1-x/100)) for x in sys_param['equity_external_shareholders_perc'] for y in sys_param['team_allocation']],
    'seed_token_allocation' : calculate_investor_allocation(sys_param, "seed"),
    'presale_1_token_allocation' : calculate_investor_allocation(sys_param, "presale_1"),
    'presale_2_token_allocation' : calculate_investor_allocation(sys_param, "presale_2"),
    'public_sale_token_allocation' : [(x/100)for x in sys_param['public_sale_supply_perc']],
    'team_token_allocation' : [x / 100 for x in sys_param['team_allocation']],
    'ov_token_allocation' : [x / 100 for x in sys_param['ov_allocation']],
    'advisor_token_allocation' : [x / 100 for x in sys_param['advisor_allocation']],
    'strategic_partners_token_allocation' : [x / 100 for x in sys_param['strategic_partners_allocation']],
    'reserve_token_allocation' : [x / 100 for x in sys_param['reserve_allocation']],
    'community_token_allocation' : [x / 100 for x in sys_param['community_allocation']],
    'foundation_token_allocation' : [x / 100 for x in sys_param['foundation_allocation']],
    'placeholder_1_token_allocation' : [x / 100 for x in sys_param['placeholder_1_allocation']],
    'placeholder_2_token_allocation' : [x / 100 for x in sys_param['placeholder_2_allocation']],
    'market_token_allocation' : [0]
}

sys_param.update(agent_token_allocation)

# calculating the initial values for the liquidity pool
liquidity_pool_initial_values = {
    'initial_token_price': [x / y for x in sys_param['public_sale_valuation'] for y in sys_param['initial_total_supply']],
    'initial_lp_token_allocation': calc_initial_lp_tokens(agent_token_allocation, sys_param),
    'initial_required_usdc': [x * y for x in calc_initial_lp_tokens(agent_token_allocation, sys_param) for y in [x / y for x in sys_param['public_sale_valuation'] for y in sys_param['initial_total_supply']]]
}
sys_param.update(liquidity_pool_initial_values)


# calculating the initial values for the different agents
stakeholder_names = [
    'angle',
    'seed',
    'presale_1',
    'presale_2',
    'public_sale',
    'team',
    'reserve',
    'community',
    'foundation',
    'placeholder_1',
    'placeholder_2',
    'market_investors'
]
#initial_stakeholder_values = generate_agents(stakeholder_names)

# defining the mapping between the stakeholder names and their type categories
stakeholder_name_mapping = {
    'angle': 'early_investor',
    'seed': 'early_investor',
    'presale_1': 'early_investor',
    'presale_2': 'early_investor',
    'public_sale': 'early_investor',
    'team': 'team',
    'reserve': 'reserve',
    'community': 'protocol_bucket',
    'foundation': 'protocol_bucket',
    'placeholder_1': 'protocol_bucket',
    'placeholder_2': 'protocol_bucket',
    'market': 'market_investors',
}

initial_stakeholder_values = generate_agents(stakeholder_name_mapping)



user_adoption_initial_values = {
    'initial_product_users' : [x for x in sys_param['initial_product_users']],
    'product_users_after_10y' : [x for x in sys_param['product_users_after_10y']],
    'product_adoption_velocity' : [x for x in sys_param['product_adoption_velocity']],
    'one_time_product_revenue_per_user' : [x for x in sys_param['one_time_product_revenue_per_user']],
    'regular_product_revenue_per_user' : [x for x in sys_param['regular_product_revenue_per_user']],
    'initial_token_holders' : [x for x in sys_param['initial_token_holders']],
    'token_holders_after_10y' : [x for x in sys_param['token_holders_after_10y']],
    'token_adoption_velocity' : [x for x in sys_param['token_adoption_velocity']],
    'one_time_token_buy_per_user' : [x for x in sys_param['one_time_token_buy_per_user']],
    'regular_token_buy_per_user' : [x for x in sys_param['regular_token_buy_per_user']],
    'avg_token_utility_allocation' : [x / 100 for x in sys_param['avg_token_utility_allocation']],
    'avg_token_holding_allocation' : [x / 100 for x in sys_param['avg_token_holding_allocation']],
    'avg_token_selling_allocation' : [x / 100 for x in sys_param['avg_token_selling_allocation']],
    'avg_token_utility_removal' : [x / 100 for x in sys_param['avg_token_utility_removal']]

}

sys_param.update(user_adoption_initial_values)





business_assumptions_initial_values = {
    'product_income_per_month': [x for x in sys_param['product_income_per_month']],
    'royalty_income_per_month': [x for x in sys_param['royalty_income_per_month']],
    'other_income_per_month': [x for x in sys_param['other_income_per_month']],
    'treasury_income_per_month': [x for x in sys_param['treasury_income_per_month']],
    'regular_income_sum': [x for x in sys_param['regular_income_sum']],
    'one_time_payments_1': [x for x in sys_param['one_time_payments_1']],
    'one_time_payments_2': [x for x in sys_param['one_time_payments_2']],
    'salaries_per_month': [x for x in sys_param['salaries_per_month']],
    'license_costs_per_month': [x for x in sys_param['license_costs_per_month']],
    'other_monthly_costs': [x for x in sys_param['other_monthly_costs']],
    'buyback_type': [x for x in sys_param['buyback_type']],
    'buyback_perc_per_month': [x for x in sys_param['buyback_perc_per_month']],
    'buyback_fixed_per_month': [x for x in sys_param['buyback_fixed_per_month']],
    'buyback_bucket': [x for x in sys_param['buyback_bucket']],
    'buyback_start': [x for x in sys_param['buyback_start']],
    'buyback_end': [x for x in sys_param['buyback_end']],
    'burn_per_month': [x for x in sys_param['burn_per_month']],
    'burn_start': [x for x in sys_param['burn_start']],
    'burn_end': [x for x in sys_param['burn_end']],
    'burn_project_bucket': [x for x in sys_param['burn_project_bucket']]
}



sys_param.update(business_assumptions_initial_values)
