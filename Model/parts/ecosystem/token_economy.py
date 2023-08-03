import pandas as pd

# POLICY FUNCTIONS
def generate_date(params, substep, state_history, prev_state, **kwargs):
    """
    Generate the current date from timestep
    """
    # parameters
    initial_date = pd.to_datetime(params['launch_date'], format='%d.%m.%y')
    
    # state variables
    old_timestep = prev_state['timestep']
    
    # policy logic
    new_date = pd.to_datetime(initial_date)+pd.DateOffset(months=old_timestep-1)

    return {'new_date': new_date}

def token_economy_metrics(params, substep, state_history, prev_state, **kwargs):
    """
    Calculate the initial token economy metrics, such as MC, FDV MC, circ. supply, and tokens locked.
    """

    liquidity_pool = prev_state['liquidity_pool']
    agents = prev_state['agents']
    total_token_supply = params['initial_total_supply']
    selling_perc = params['avg_token_selling_allocation']
    utility_perc = params['avg_token_utility_allocation']
    holding_perc = params['avg_token_holding_allocation']
    remove_perc = params['avg_token_utility_removal']

    circulating_tokens = 0
    locked_apr_tokens = 0
    locked_buyback_tokens = 0

    for stakeholder in agents:
        circulating_tokens += agents[stakeholder]['tokens']
        locked_apr_tokens += agents[stakeholder]['tokens_apr_locked']
        locked_buyback_tokens += agents[stakeholder]['tokens_buyback_locked']
    
    MC = liquidity_pool['token_price'] * circulating_tokens
    FDV_MC = liquidity_pool['token_price'] * total_token_supply

    return {'total_token_supply': total_token_supply, 'selling_perc': selling_perc, 'utility_perc': utility_perc, 'holding_perc': holding_perc,
            'remove_perc': remove_perc, 'circulating_supply': circulating_tokens, 'MC': MC, 'FDV_MC': FDV_MC, 'tokens_apr_locked': locked_apr_tokens,
            'tokens_buyback_locked': locked_buyback_tokens}

# STATE UPDATE FUNCTIONS
def update_date(params, substep, state_history, prev_state, policy_input, **kwargs):
    """
    Function to update the current date of the timestep
    """
    # policy input / update logic
    updated_date = policy_input['new_date']

    return ('date', updated_date)

def update_token_economy(params, substep, state_history, prev_state, policy_input, **kwargs):
    """
    Function to update the agents based on the changes in business funds to seed the liquidity pool.
    """
    # get state variables
    updated_token_economy = prev_state['token_economy'].copy()

    # policy inputs
    total_token_supply = policy_input['total_token_supply']
    selling_perc = policy_input['selling_perc']
    utility_perc = policy_input['utility_perc']
    holding_perc = policy_input['holding_perc']
    remove_perc = policy_input['remove_perc']
    circulating_supply = policy_input['circulating_supply']
    MC = policy_input['MC']
    FDV_MC = policy_input['FDV_MC']
    tokens_apr_locked = policy_input['tokens_apr_locked']
    tokens_buyback_locked = policy_input['tokens_buyback_locked']

    updated_token_economy['total_supply'] = total_token_supply
    updated_token_economy['circulating_supply'] = circulating_supply
    updated_token_economy['MC'] = MC
    updated_token_economy['FDV_MC'] = FDV_MC
    updated_token_economy['tokens_apr_locked'] = tokens_apr_locked
    updated_token_economy['tokens_buyback_locked'] = tokens_buyback_locked
    updated_token_economy['selling_perc'] = selling_perc
    updated_token_economy['utility_perc'] = utility_perc
    updated_token_economy['holding_perc'] = holding_perc
    updated_token_economy['remove_perc'] = remove_perc

    return ('token_economy', updated_token_economy)