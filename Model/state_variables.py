from sys_params import *
from parts.utils import *

initial_stakeholders = generate_agents(initial_values)

initial_liquidity_pool = seed_dex_liquidity(agent_token_allocation, initial_stakeholders, 'reserve', sys_param)

initial_token_economy = generate_initial_token_economy_metrics(initial_stakeholders, initial_liquidity_pool, sys_param)

initial_state = {
    'agents': initial_stakeholders,
    'liquidity_pool': initial_liquidity_pool,
    'token_economy': initial_token_economy
}
