from .utils import import_dummy_data

# POLICY FUNCTIONS
def MOCKUP_populate_holding_supply(params, substep, state_history, prev_state, **kwargs):
    """
    Policy function to prescribe holding supply from QTM data tables
    """
    # get parameters

    # get state variables
    current_timestep = prev_state['timestep']

    # load dummy data
    holding_supply_i = import_dummy_data(180, current_timestep)

    return {'holding_supply_i': holding_supply_i}



# STATE UPDATE FUNCTIONS
def MOCKUP_update_holding_supply(params, substep, state_history, prev_state, policy_input, **kwargs):
    """
    Function to update holding supply based on the prescribed data from the QTM data tables
    """
    # get parameters

    # get state variables
    updated_token_economy = prev_state['token_economy'].copy()

    # get policy input
    holding_supply_i = policy_input['holding_supply_i']

    # update logic
    updated_token_economy["holding_supply"] = holding_supply_i

    return ('token_economy', updated_token_economy)