
"""Provide date and token economy metrics.

Contains policy functions (PF) and state update functions (SUF).


Functions:
    generate_date (PF): Generate the current date from timestep.

    token_economy_metrics (PF): Calculate the initial token economy metrics, 
        such as MC, FDV MC, and circ. supply.

    update_date (SUF):Function to update the current date of the timestep.

    update_token_economy (SUF): Function to update token economy attributes 
        and metrics.

"""

import pandas as pd
from ..utils import *

# POLICY FUNCTIONS
def generate_date(params, substep, state_history, prev_state, **kwargs):
    """
    Generate the current date from timestep.

    Policy function.

    Returns: 
        A dict which points to the current date.
    """
    # parameters
    initial_date = get_initial_date(params)
    
    # state variables
    current_month = prev_state['timestep']
    
    # policy logic
    new_date = pd.to_datetime(initial_date)+pd.DateOffset(months=current_month)

    return {'new_date': new_date}

def token_economy_metrics(params, substep, state_history, prev_state, **kwargs):
    """
    Calculate the initial token economy metrics, such as MC, FDV MC, and circ. 
    supply.

    Policy function.

    Calculations take place as the last substep, to reflect changes that
    happened to the token economy in the current timestep. Information 
    provided for: total supply, selling/utility/holding percentages, 
    circulating supply, unvested tokens, holding supply, and the metrics:
    MC and FDV NC.

    Returns: 
        A dict which provides information about the updated token economy
        attributes and metrics.
    """
    # parameters
    initial_total_supply = params['initial_total_supply']
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
    u_staking_allocation_cum = utilities['u_staking_allocation_cum']

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
    circulating_tokens += u_staking_allocation_cum
    

    vested_cum = 0 
    for stakeholder in agents:
        vested_cum += agents[stakeholder]['a_tokens_vested_cum']
    
    unvested_tokens = initial_total_supply-vested_cum-te_airdrop_tokens_cum-initial_lp_tokens

    total_token_supply = circulating_tokens + unvested_tokens

    MC = liquidity_pool['lp_token_price'] * circulating_tokens
    FDV_MC = liquidity_pool['lp_token_price'] * total_token_supply

    return {'total_token_supply': total_token_supply, 'te_selling_perc': selling_perc, 'te_utility_perc': utility_perc, 'te_holding_perc': holding_perc,
            'te_remove_perc': remove_perc, 'te_circulating_supply': circulating_tokens,'te_unvested_supply':unvested_tokens, 'te_MC': MC, 'te_FDV_MC': FDV_MC,
            'te_holding_supply': held_tokens}

# STATE UPDATE FUNCTIONS
def update_date(params, substep, state_history, prev_state, policy_input, **kwargs):
    """
    Function to update the current date of the timestep.

    State update function.

    Returns:
        Tuple ('date', updated_date).
    """
    # policy input / update logic
    updated_date = policy_input['new_date']

    return ('date', updated_date)

def update_token_economy(params, substep, state_history, prev_state, policy_input, **kwargs):
    """
    Function to update token economy attributes and metrics.

    State update function.

    Updates nformation for: total supply, selling/utility/holding percentages, 
    circulating supply, unvested tokens, holding supply, USD values of 
    incentivised tokens and airdrops and the metrics: MC and FDV NC.

    Returns:
        Tuple ('token_economy', updated_token_economy).
    """
    # parameters
    bribing_share = params['bribing_share'] if 'bribing_share' in params else 0.0

    # get state variables
    updated_token_economy = prev_state['token_economy'].copy()
    utilities = prev_state['utilities'].copy()
    business_assumptions = prev_state['business_assumptions'].copy()
    lp = prev_state['liquidity_pool'].copy()
    user_adoption = prev_state['user_adoption'].copy()

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
    updated_token_economy['te_incentivised_tokens_usd'] = updated_token_economy['te_incentivised_tokens'] * lp['lp_token_price']
    updated_token_economy['te_incentivised_tokens_usd_cum'] += updated_token_economy['te_incentivised_tokens'] * lp['lp_token_price']
    updated_token_economy['te_airdrop_tokens_usd'] = updated_token_economy['te_airdrop_tokens'] * lp['lp_token_price']
    updated_token_economy['te_airdrop_tokens_usd_cum'] += updated_token_economy['te_airdrop_tokens'] * lp['lp_token_price']
    updated_token_economy['te_p_r_ratio'] = FDV_MC / ((business_assumptions['ba_fix_business_revenue_usd'] + user_adoption['ua_product_revenue'])*12) if (business_assumptions['ba_fix_business_revenue_usd'] + user_adoption['ua_product_revenue']) > 0 else 0.0
    updated_token_economy['te_p_e_ratio'] = FDV_MC / (business_assumptions['ba_cash_flow']*12) if (business_assumptions['ba_cash_flow']) > 0 else 0.0
    updated_token_economy['te_product_user_per_incentivised_usd'] = user_adoption['ua_product_users'] / (updated_token_economy['te_incentivised_tokens_usd_cum'] + updated_token_economy['te_airdrop_tokens_usd_cum']) if (updated_token_economy['te_incentivised_tokens_usd_cum'] + updated_token_economy['te_airdrop_tokens_usd_cum']) > 0 else 0.0
    updated_token_economy['te_incentivised_usd_per_product_user'] = (updated_token_economy['te_incentivised_tokens_usd_cum'] + updated_token_economy['te_airdrop_tokens_usd_cum']) / user_adoption['ua_product_users'] if user_adoption['ua_product_users'] > 0 else 0.0
    
    cash_staking_rewards = business_assumptions['ba_staker_revenue_usd'] if utilities['u_staking_revenue_share_rewards'] <= 0 else 0.0
    bribing_rewards_usd = updated_token_economy['te_incentivised_tokens_usd'] * bribing_share/100 if bribing_share > 0 else 0.0
    updated_token_economy['te_bribe_rewards_for_stakers_usd'] = bribing_rewards_usd
    updated_token_economy['te_bribe_rewards_for_stakers_usd_cum'] += bribing_rewards_usd
    token_staking_apr = (utilities['u_staking_revenue_share_rewards'] + utilities['u_staking_vesting_rewards'] + utilities['u_staking_minting_rewards'])*12 / utilities['u_staking_allocation_cum'] * 100 if utilities['u_staking_allocation_cum'] > 0 else 0.0
    revenue_staking_apr = (cash_staking_rewards+bribing_rewards_usd)*12 / (utilities['u_staking_allocation_cum'] * lp['lp_token_price']) * 100 if utilities['u_staking_allocation_cum'] > 0 else 0.0
    new_staking_apr = token_staking_apr + revenue_staking_apr
    new_staking_apr = 500 if (utilities['u_staking_allocation_cum'] == 0 and (((utilities['u_staking_revenue_share_rewards'] + utilities['u_staking_vesting_rewards'] + utilities['u_staking_minting_rewards']) > 0) or ((cash_staking_rewards+bribing_rewards_usd)>0))) else new_staking_apr
    updated_token_economy['te_staking_apr'] = new_staking_apr if not np.isnan(new_staking_apr) else 0.0

    return ('token_economy', updated_token_economy)

