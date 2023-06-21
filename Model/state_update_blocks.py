from  parts.mechanisms import *

state_update_block = [
    {
        # mechanisms.py
        'policies': {
            'vest_tokens': vest_tokens
        },
        'variables': { 
            'agents': update_agent_vested_tokens,
            'token_economy': update_token_economy
        }
    }
]
