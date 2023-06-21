from  parts.vesting import *
from parts.agent_behavior import *

state_update_block = [
    {
        # vesting.py
        'policies': {
            'vest_tokens': vest_tokens
        },
        'variables': { 
            'agents': update_agent_vested_tokens,
            'token_economy': update_token_economy
        },
    },
    {
        # agent_behavior.py
        'policies': {
            'agent_behaviour': generate_agent_behavior,
        },
        'variables': {
            'agents': update_agent_behavior,
        },
    }
]
