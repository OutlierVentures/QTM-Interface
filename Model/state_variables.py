from sys_params import *
from parts.utils import *



initial_stakeholder_values, token_economy  = initial_investor_allocation(sys_param['initial_stakeholder_values'],sys_param['token_economy'])

liquidity_pool = liquidity_pool_module(initial_stakeholder_values,token_economy,sys_param['liquidity_pool'])


initial_state = {
    'agents': generate_agents(initial_values['initial_team_usd_funds'],initial_values['initial_team_tokens'], 
                            initial_values['initial_foundation_usd_funds'],initial_values['initial_foundation_tokens'], 
                            initial_values['initial_early_investor_usd_funds'], initial_values['initial_early_investor_tokens'],
                            initial_values['initial_market_investor_usd_funds'], initial_values['initial_market_investor_tokens']),
    'investors': initial_stakeholder_values,
    'token_economy': token_economy,
    'liquidity_pool': liquidity_pool

}
