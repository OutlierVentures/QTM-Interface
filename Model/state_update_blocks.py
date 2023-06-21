from  parts.mechanisms import *

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
