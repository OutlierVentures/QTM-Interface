from parts.vesting import *
from parts.agent_behavior import *
from parts.liquidity_pool import *
from parts.token_economy import *
from parts.user_adoption import *
from parts.business_assumptions import *
from parts.kpis import *
from parts.incentivisation import *


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
        # kpis.py
        'policies': {
            'generate_date': generate_date
        },
        'variables': { 
            'date': update_date
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
        # incentivisation.py
        'policies': {
            'incentivisation': incentivisation
        },
        'variables': { 
            'agents': update_agents_after_incentivisation,
            'token_economy': update_token_economy_after_incentivisation,
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
        # agent_behavior.py
        'policies': {
            'agent_token_allocations': agent_token_allocations,
        },
        'variables': {
            'agents': update_agent_token_allocations,
            'meta_bucket_allocations':update_meta_bucket_allocations,
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
    },
     {
        # user_adoption.py
        'policies': {
            'user_adoption_metrics': user_adoption_metrics,
        },
        'variables': {
            'user_adoption': update_user_adoption,
        },
    },
    {
        # business_assumptions.py
        'policies': {
            'business_assumption_metrics': business_assumption_metrics,
        },
        'variables': {
            'business_assumptions': update_business_assumptions,
        },
    }
]
