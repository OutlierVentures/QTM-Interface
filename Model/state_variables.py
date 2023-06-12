from sys_params import *
from utils import *



initial_investors, token_economy  = initial_investor_allocation(sys_param['initial_investors'],sys_param['token_economy'])

liquidity_pool = liquidity_pool_module(initial_investors,token_economy,sys_param['liquidity_pool'])

print(liquidity_pool)

initial_state = {
    'investors': initial_investors,
    'token_economy': token_economy,
    'liquidity_pool': liquidity_pool

}
