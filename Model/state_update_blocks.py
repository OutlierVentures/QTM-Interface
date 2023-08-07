from parts.ecosystem.vesting import *
from parts.ecosystem.incentivisation import *
from parts.ecosystem.airdrops import *
from parts.ecosystem.burn import *
from parts.ecosystem.liquidity_pool import *
from parts.ecosystem.token_economy import *
from parts.business.user_adoption import *
from parts.business.business_assumptions import *
from parts.agents_behavior.agent_meta_bucket_behavior import *
from parts.utilities.staking_base_apr import *
from parts.utilities.staking_revenue_share import *
from parts.utilities.liquidity_mining import *

from parts.mockups import *


state_update_block = [
    ## MOCKUP STATE UPDATE BLOCKS ##
    {
        # substep 1: mockups.py
        'policies': {
            'MOCKUP_populate_holding_supply': MOCKUP_populate_holding_supply
        },
        'variables': {
            'token_economy': MOCKUP_update_holding_supply
        },
    },

    ## MODEL STATE UPDATE BLOCKS ##
    {
        # substep 2: ecosystem/liquidity_pool.py
        'policies': {
            'initialize_liquidity_pool': initialize_liquidity_pool
        },
        'variables': {
            'liquidity_pool': update_lp_after_lp_seeding
        },
    },
    {
        # substep 3: ecosystem/token_economy.py
        'policies': {
            'generate_date': generate_date
        },
        'variables': { 
            'date': update_date
        },
    },
    {
        # substep 4: ecosystem/vesting.py
        'policies': {
            'vest_tokens': vest_tokens
        },
        'variables': { 
            'agents': update_agent_vested_tokens,
        },
    },
    {
        # substep 5: ecosystem/incentivisation.py
        'policies': {
            'incentivisation': incentivisation
        },
        'variables': { 
            'agents': update_agents_after_incentivisation,
            'token_economy': update_token_economy_after_incentivisation,
        },
    },
    {
        # substep 6: ecosystem/airdrops.py
        'policies': {
            'airdrops': airdrops
        },
        'variables': { 
            'agents': update_agents_after_airdrops,
            'token_economy': update_token_economy_after_airdrops,
        },
    },
    {
        # substep 7: ecosystem/burn.py
        'policies': {
            'burn_from_protocol_bucket': burn_from_protocol_bucket
        },
        'variables': { 
            'agents': update_protocol_bucket_agent_after_burn,
            'token_economy': update_token_economy_after_protocol_bucket_burn,
        },
    },
    {
        # substep 8: agents_behavior/agent_meta_bucket_behavior.py
        'policies': {
            'generate_agent_meta_bucket_behavior': generate_agent_meta_bucket_behavior,
        },
        'variables': {
            'agents': update_agent_meta_bucket_behavior
        },
    },
    {
        # substep 9: agents_behavior/agent_meta_bucket_behavior.py
        'policies': {
            'agent_meta_bucket_allocations': agent_meta_bucket_allocations,
        },
        'variables': {
            'agents': update_agent_meta_bucket_allocations,
            'token_economy': update_token_economy_meta_bucket_allocations
        },
    },
    {
        # substep 10: business/user_adoption.py
        'policies': {
            'user_adoption_metrics': user_adoption_metrics,
        },
        'variables': {
            'user_adoption': update_user_adoption,
        },
    },
    {
        # substep 11: utilities/staking_base_apr.py
        'policies': {
            'apr': apr,
        },
        'variables': {
            'utilities': update_utilties_after_apr,
        },
    },
    {
        # substep 12: utilities/staking_revenue_share.py
        'policies': {
            'staking_revenue_share_buyback_amount': staking_revenue_share_buyback_amount,
        },
        'variables': {
            'utilities': update_buyback_amount_from_revenue_share,
        },
    },
    {
        # substep 13: utilities/staking_revenue_share.py
        'policies': {
            'staking_revenue_share_buyback_agent_allocation': staking_revenue_share_buyback_agent_allocation,
        },
        'variables': {
            'agents': update_staking_revenue_share_buyback_agent_allocation,
            'utilities': update_staking_revenue_share_buyback_meta_allocation,
        },
    },
    {
        # substep 14: utilities/liquidity_mining.py
        'policies': {
            'staking_liquidity_mining_agent_allocation': staking_liquidity_mining_agent_allocation,
        },
        'variables': {
            'agents': update_liquidity_mining_agent_allocation,
            'utilities': update_liquidity_mining_meta_allocation,
        },
    },
    {
        # substep 15: business/business_assumptions.py
        'policies': {
            'business_assumption_metrics': business_assumption_metrics,
        },
        'variables': {
            'business_assumptions': update_business_assumptions,
        },
    },
    {
        # substep 16: ecosystem/liquidity_pool.py
        'policies': {
            'liquidity_pool_tx1_after_adoption': liquidity_pool_tx1_after_adoption,
        },
        'variables': {
            'agents': update_agents_tx1_after_adoption,
            'liquidity_pool': update_liquidity_pool_after_transaction,
        },
    },
    {
        # substep 17: ecosystem/liquidity_pool.py
        'policies': {
            'liquidity_pool_tx2_after_vesting_sell': liquidity_pool_tx2_after_vesting_sell,
        },
        'variables': {
            'liquidity_pool': update_liquidity_pool_after_transaction,
        },
    },
    {
        # substep 18: ecosystem/token_economy.py
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