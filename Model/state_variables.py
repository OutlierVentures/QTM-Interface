from sys_params import *
from utils import *


initial_token_supply = sys_param['initial_token_supply']

initial_investors, initial_circulating_supply  = initial_investor_allocation(initial_investors,initial_token_supply)


initial_state = {
    'investors': initial_investors,
    
    'token_economy': {
        'initial_token_supply': initial_token_supply,
        'current_circulating_supply': initial_circulating_supply


    }
}
