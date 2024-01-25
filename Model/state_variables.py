from Model.sys_params import get_sys_param
from Model.parts.utils import *

# Get the current directory
current_dir = os.path.dirname(os.path.abspath(__file__))

# Go up one folder
parent_dir = os.path.abspath(os.path.join(current_dir, os.pardir))

# Append the parent directory to sys.path
sys.path.append(parent_dir)

def get_initial_state(input_file, adjusted_params):
    sys_param, stakeholder_name_mapping, stakeholder_names, conn, cur, param_id, execute_sim = get_sys_param(input_file, adjusted_params)

    # initialize the initial stakeholders
    initial_stakeholders = generate_agents(stakeholder_name_mapping, sys_param)

    # initialize the initial liquidity pool
    initial_liquidity_pool = initialize_dex_liquidity(sys_param)

    # initialize the initial token economy
    initial_token_economy = generate_initial_token_economy_metrics(initial_stakeholders, initial_liquidity_pool, sys_param)

    # initialize the initial user adoption
    initial_user_adoption = initialize_user_adoption(sys_param)

    # initialize the initial business assumptions
    business_assumptions = initialize_business_assumptions(sys_param, initial_user_adoption)

    # initialize the initial standard utilities
    utilities = initialize_utilities(initial_stakeholders, sys_param)

    # compose the initial state
    initial_state = {
        'date': get_initial_date(sys_param),
        'agents': initial_stakeholders,
        'liquidity_pool': initial_liquidity_pool,
        'token_economy': initial_token_economy,
        'user_adoption': initial_user_adoption,
        'business_assumptions': business_assumptions,
        'utilities': utilities 
    }

    return initial_state, sys_param, stakeholder_name_mapping, stakeholder_names, conn, cur, param_id, execute_sim
