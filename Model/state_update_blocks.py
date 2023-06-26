from  parts.vesting import *
from parts.agent_behavior import *
from parts.liquidity_pool import *
from parts.token_economy import *

state_update_block = [
    {
        # liquidity_pool.py
        'policies': {
            'initialize_liquidity_pool': initialize_liquidity_pool
        },
        'variables': { 
            'agents': update_agents_after_lp_seeding,
            'liquidity_pool': update_lp_after_lp_seeding
        },
    },
    {
        # vesting.py
        'policies': {
            'vest_tokens': vest_tokens
        },
        'variables': { 
            'agents': update_agent_vested_tokens,
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
    },
    {
        # token_economy.py
        'policies': {
            'token_economy_metrics': token_economy_metrics,
        },
        'variables': {
            'token_economy': update_token_economy,
        },
    }
]
