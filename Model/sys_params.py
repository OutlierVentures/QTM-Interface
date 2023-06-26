import uuid
from parts.utils import *
import pandas as pd
import sys
sys.path.append('../')
from data.not_iterable_variables import *


QTM_inputs = pd.read_csv('../data/Quantitative_Token_Model_V1.87 - cadCAD_inputs.csv')

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
    'market_investors_token_allocation' : [0]
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
initial_stakeholder_values = initialize_agent_parameters(stakeholder_names)
