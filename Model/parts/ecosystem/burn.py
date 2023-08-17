import pandas as pd

# POLICY FUNCTIONS
def burn_from_protocol_bucket(params, substep, state_history, prev_state, **kwargs):
    """
    Policy function to incentivise the ecosystem
    """
    # get parameters
    total_token_supply = params['initial_total_supply']
    burn_start = pd.to_datetime(params['burn_start'], format='%d.%m.%y')
    burn_end = pd.to_datetime(params['burn_end'], format='%d.%m.%y')
    burn_per_month = params['burn_per_month']

    # get state variables
    current_date = pd.to_datetime(prev_state['date'])

    # policy logic
    # calculate burn amount
    if burn_start <= current_date and burn_end > current_date:
        burn_token_amount = total_token_supply * burn_per_month/100
    else:
        burn_token_amount = 0

    return {'burn_token_amount': burn_token_amount}

# STATE UPDATE FUNCTIONS
def update_protocol_bucket_agent_after_burn(params, substep, state_history, prev_state, policy_input, **kwargs):
    """
    Function to update the vested tokens for each investor based on some criteria
    """
    # get parameters
    burn_project_bucket = params['burn_project_bucket']

    # get state variables
    updated_agents = prev_state['agents']

    # get policy input
    burn_token_amount = policy_input['burn_token_amount']

    # update logic
    # subtract burn tokens from protocol bucket
    for agent in updated_agents:
        if updated_agents[agent]['a_type'] == 'protocol_bucket' and burn_project_bucket.lower() in updated_agents[agent]['a_name'].lower():
            updated_agents[agent]['a_tokens'] -= [burn_token_amount if burn_token_amount < updated_agents[agent]['a_tokens'] else updated_agents[agent]['a_tokens']][0]
            updated_agents[agent]['a_tokens_burned'] = burn_token_amount
            updated_agents[agent]['a_tokens_burned_cum'] += burn_token_amount

    return ('agents', updated_agents)

def update_token_economy_after_protocol_bucket_burn(params, substep, state_history, prev_state, policy_input, **kwargs):
    """
    Function to update the token economy after incentivisation
    """
    # get parameters

    # get state variables
    updated_token_economy = prev_state['token_economy'].copy()
    liquidity_pool = prev_state['liquidity_pool'].copy()

    # get policy input
    burn_token_amount = policy_input['burn_token_amount']

    # update logic
    updated_token_economy['te_tokens_burned'] = burn_token_amount
    updated_token_economy['te_tokens_burned_cum'] += burn_token_amount
    updated_token_economy['te_tokens_burned_usd'] = burn_token_amount * liquidity_pool['lp_token_price']

    return ('token_economy', updated_token_economy)