from datetime import datetime

from sys_params import *
from parts.utils import *

# initialize the initial stakeholders
initial_stakeholders = generate_agents(stakeholder_name_mapping)

# initialize the initial liquidity pool
initial_liquidity_pool = initialize_dex_liquidity()

# initialize the initial token economy
initial_token_economy = generate_initial_token_economy_metrics()

# initialize the initial user adoption
initial_user_adoption = initialize_user_adoption()

# initialize the initial business assumptions
business_assumptions = initialize_business_assumptions()

meta_bucket_allocations = initalize_meta_bucket_allocations()

# compose the initial state
initial_state = {
    'agents': initial_stakeholders,
    'liquidity_pool': initial_liquidity_pool,
    'token_economy': initial_token_economy,
    'user_adoption': initial_user_adoption,
    'business_assumptions': business_assumptions,
    'date': convert_date(sys_param),
    'meta_bucket_allocations':meta_bucket_allocations
}
