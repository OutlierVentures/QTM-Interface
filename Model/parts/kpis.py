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


# STATE UPDATE FUNCTIONS
def update_date(params, substep, state_history, prev_state, policy_input, **kwargs):
    """
    Function to update the current date of the timestep
    """
    # policy input / update logic
    updated_date = policy_input['new_date']

    return ('date', updated_date)



