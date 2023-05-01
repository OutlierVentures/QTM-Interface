from  policies import *




def update_token_economy(params, substep, state_history, prev_state, policy_input, **kwargs):
    # Function to update the vested tokens for each investor based on some criteria
    updated_economy = policy_input['updated_token_economy']
    return ('token_economy', updated_economy)


def update_investor_tokens(params, substep, state_history, prev_state, policy_input, **kwargs):
    # Function to update the vested tokens for each investor based on some criteria
    # ...
    updated_investors = policy_input['updated_investors']

    return ('investors', updated_investors)




state_update_block = [
    
    
    {
        # agents.py
        'policies': {
            'vest_tokens': vest_tokens
        },
        'variables': { 
            'investors': update_investor_tokens,
            'token_economy': update_token_economy
        }
    }
]
