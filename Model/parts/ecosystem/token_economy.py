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
    # parameters
    total_token_supply = params['initial_total_supply']
    selling_perc = params['avg_token_selling_allocation']
    utility_perc = params['avg_token_utility_allocation']
    holding_perc = params['avg_token_holding_allocation']
    remove_perc = params['avg_token_utility_removal']
    initial_lp_tokens = params['initial_lp_token_allocation']

    # state variables
    liquidity_pool = prev_state['liquidity_pool']
    agents = prev_state['agents']
    token_economy = prev_state['token_economy']
    utilities = prev_state['utilities']

    # circulating supply variable
    circulating_tokens = 0
    lp_tokens = liquidity_pool['lp_tokens']
    u_staking_base_apr_cum = utilities['u_staking_base_apr_cum']
    u_staking_revenue_share_allocation_cum = utilities['u_staking_revenue_share_allocation_cum']

    # unvested supply variable
    te_airdrop_tokens_cum = token_economy['te_airdrop_tokens_cum']

    protocol_bucket_tokens = 0
    held_tokens = 0
    for stakeholder in agents:
        # calculate protocol bucket tokens
        if agents[stakeholder]['a_type'] == 'protocol_bucket':
            protocol_bucket_tokens += agents[stakeholder]['a_tokens']
        # calculate protocol bucket tokens
        if agents[stakeholder]['a_type'] != 'protocol_bucket':
            held_tokens += agents[stakeholder]['a_tokens']

    circulating_tokens += protocol_bucket_tokens + held_tokens + lp_tokens
    circulating_tokens += u_staking_base_apr_cum + u_staking_revenue_share_allocation_cum
    

    vested_cum = 0 
    for stakeholder in agents:
        vested_cum += agents[stakeholder]['a_tokens_vested_cum']
    
    unvested_tokens = total_token_supply-vested_cum-te_airdrop_tokens_cum-initial_lp_tokens


    MC = liquidity_pool['lp_token_price'] * circulating_tokens
    FDV_MC = liquidity_pool['lp_token_price'] * total_token_supply


    return {'total_token_supply': total_token_supply, 'te_selling_perc': selling_perc, 'te_utility_perc': utility_perc, 'te_holding_perc': holding_perc,
            'te_remove_perc': remove_perc, 'te_circulating_supply': circulating_tokens,'te_unvested_supply':unvested_tokens, 'te_MC': MC, 'te_FDV_MC': FDV_MC,
            'te_holding_supply': held_tokens}

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
    selling_perc = policy_input['te_selling_perc']
    utility_perc = policy_input['te_utility_perc']
    holding_perc = policy_input['te_holding_perc']
    remove_perc = policy_input['te_remove_perc']
    circulating_supply = policy_input['te_circulating_supply']
    unvested_tokens = policy_input['te_unvested_supply']
    MC = policy_input['te_MC']
    FDV_MC = policy_input['te_FDV_MC']
    held_supply = policy_input['te_holding_supply']


    # update logic
    updated_token_economy['te_total_supply'] = total_token_supply
    updated_token_economy['te_circulating_supply'] = circulating_supply
    updated_token_economy['te_unvested_supply'] = unvested_tokens
    updated_token_economy['te_MC'] = MC
    updated_token_economy['te_FDV_MC'] = FDV_MC
    updated_token_economy['te_selling_perc'] = selling_perc
    updated_token_economy['te_utility_perc'] = utility_perc
    updated_token_economy['te_holding_perc'] = holding_perc
    updated_token_economy['te_remove_perc'] = remove_perc
    updated_token_economy['te_holding_supply'] = held_supply

    return ('token_economy', updated_token_economy)

