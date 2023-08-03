from parts.initial_emissions.vesting import *
from parts.initial_emissions.incentivisation import *
from parts.initial_emissions.airdrops import *
from parts.liquidity_pool import *
from parts.token_economy import *
from parts.user_adoption import *
from parts.business_assumptions import *
from parts.kpis import *
from parts.agents_behavior.agent_meta_bucket_behavior import *
from parts.utilities.staking_base_apr import *
from parts.utilities.staking_revenue_share import *


state_update_block = [
    {
        # liquidity_pool.py
        'policies': {
            'initialize_liquidity_pool': initialize_liquidity_pool
        },
        'variables': {
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
        # airdrops.py
        'policies': {
            'airdrops': airdrops
        },
        'variables': { 
            'agents': update_agents_after_airdrops,
            'token_economy': update_token_economy_after_airdrops,
        },
    },
    {
        # agent_meta_bucket_behavior.py
        'policies': {
            'generate_agent_meta_bucket_behavior': generate_agent_meta_bucket_behavior,
        },
        'variables': {
            'agents': update_agent_meta_bucket_behavior
        },
    },
    {
        # agent_meta_bucket_behavior.py
        'policies': {
            'agent_meta_bucket_allocations': agent_meta_bucket_allocations,
        },
        'variables': {
            'agents': update_agent_meta_bucket_allocations,
            'token_economy': update_token_economy_meta_bucket_allocations
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
        # staking_base_apr.py
        'policies': {
            'apr': apr,
        },
        'variables': {
            'utilities': update_utilties_after_apr,
        },
    },
    {
        # utilities/staking_revenue_share.py
        'policies': {
            'staking_revenue_share_buyback_amount': staking_revenue_share_buyback_amount,
        },
        'variables': {
            'utilities': update_buyback_amount_from_revenue_share,
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
]

''' 
 {
    # agent_utility_behavior.py
    'policies': {
        'generate_agent_behavior': generate_agent_behavior,
        'agent_token_allocations':agent_token_allocations,
    },
    'variables': {
        'agents': update_agent_behavior,
        'agents':update_agent_token_allocations,
        'token_economy':update_meta_bucket_allocations

    },
    },'''