import numpy as np
import pandas as pd
from datetime import datetime
from Model.parts.utils import months_difference

"""Vesting tokens and updating the amount of vested tokens held.

Contains policy functions (PF) and state update functions (SUF).


Functions:
    vest_tokens (PF): Policy function to vest tokens for each stakeholder.

    update_agent_vested_tokens (SUF): Function to update the vested tokens 
        for each investor based on some criteria.
"""

# POLICIY FUNCTIONS
def vest_tokens(params, substep, state_history, prev_state, **kwargs):
    """
    Policy function to vest tokens for each stakeholder.

    Policy function.

    Returns: 
        A dict which mapping agents to their vested token amounts.
    """
    token_launch_date = pd.to_datetime(params['launch_date'], format='%d.%m.%Y')
    token_launch = params['token_launch'] if 'token_launch' in params else True

    agents = prev_state['agents'].copy()
    total_token_supply = params['initial_total_supply']
    current_month = prev_state['timestep']

    if not token_launch:
        passed_months = np.abs(int(months_difference(token_launch_date, datetime.today())))
        current_month = passed_months + current_month

    agent_token_vesting_dict = {}
    for key, agent in agents.items():
        # Get all invesotor info
        agent_type = agent['a_name']
        agent_token_allocation = [params[agent_type+"_token_allocation"] if agent_type+"_token_allocation" in params else 0][0]
        agent_initial_vesting_perc = [params[agent_type+"_initial_vesting"] if agent_type+"_initial_vesting" in params else 0][0]
        agent_cliff_months = [params[agent_type+"_cliff"] if agent_type+"_cliff" in params else 0][0]
        agent_vesting_duration = [params[agent_type+"_vesting_duration"] if agent_type+"_vesting_duration" in params else 0][0]

        # Parameter integrity checks
        if agent_vesting_duration <= 0 and agent_initial_vesting_perc <= 0:
            vesting_period_token_amount = 0
        elif agent_vesting_duration <= 0 and agent_initial_vesting_perc != 100:
            print("Warning: agent "+str(agent_type)+" vesting duration is 0 but initial vesting percentage is not 100%! It is "+str(agent_initial_vesting_perc)+"%. Setting vesting amount to 0.")
            vesting_period_token_amount = 0
        elif agent_vesting_duration <= 0:
            agent_vesting_duration = 0
        else:
            vesting_period_token_amount = (agent_token_allocation * total_token_supply - (agent_initial_vesting_perc / 100 * agent_token_allocation* total_token_supply)) / agent_vesting_duration
        
        if (current_month > agent_cliff_months + agent_vesting_duration) or current_month <= agent_cliff_months:
            vesting_period_token_amount = 0

        agent_token_vesting_dict[key] = [vesting_period_token_amount + agent_token_vesting_dict[key] if key in agent_token_vesting_dict else vesting_period_token_amount][0]

    return {'agent_token_vesting_dict': agent_token_vesting_dict}

# STATE UPDATE FUNCTIONS
def update_agent_vested_tokens(params, substep, state_history, prev_state, policy_input, **kwargs):
    """
    Function to update the vested tokens for each investor based on some criteria.

    State update function.

    Returns:
        Tuple ('agents', updated_agents), where updated_agents provide information
        for all agents on updated token holding, amount of vested tokens in current 
        period and cumulatively.
    """
    token_launch = params['token_launch'] if 'token_launch' in params else True
    updated_agents = prev_state['agents']
    current_month = prev_state['timestep']
    agent_token_vesting_dict = policy_input['agent_token_vesting_dict']

    for key, value in agent_token_vesting_dict.items():
        updated_agents[key]['a_tokens'] += value
        updated_agents[key]['a_tokens_vested'] = value + updated_agents[key]['a_tokens_vested_cum'] if current_month == 1 and token_launch else value
        updated_agents[key]['a_tokens_vested_cum'] += value

    return ('agents', updated_agents)