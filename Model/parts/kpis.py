import pandas as pd

# POLICY FUNCTIONS
def generate_date(params, substep, state_history, prev_state, **kwargs):
    """
    Generate the current date from timestep
    """

    old_date = prev_state['date']
    new_date = pd.to_datetime(old_date)+pd.DateOffset(months=1)
    return {'new_date': new_date}


# STATE UPDATE FUNCTIONS
def update_date(params, substep, state_history, prev_state, policy_input, **kwargs):
    """
    Function to update the current date of the timestep
    """
    updated_date = policy_input['new_date']
    return ('date', updated_date)