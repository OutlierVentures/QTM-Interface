from sys_params import *
from parts.utils import *

# initialize the initial stakeholders
initial_stakeholders = generate_agents(stakeholder_name_mapping)

# initialize the initial liquidity pool
initial_liquidity_pool = initialize_dex_liquidity()

# initialize the initial token economy
initial_token_economy = generate_initial_token_economy_metrics()

# compose the initial state
initial_state = {
    'agents': initial_stakeholders,
    'liquidity_pool': initial_liquidity_pool,
    'token_economy': initial_token_economy
}
