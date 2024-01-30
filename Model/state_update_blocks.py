from Model.parts.ecosystem.vesting import *
from Model.parts.ecosystem.incentivisation import *
from Model.parts.ecosystem.airdrops import *
from Model.parts.ecosystem.burn import *
from Model.parts.ecosystem.liquidity_pool import *
from Model.parts.ecosystem.token_economy import *
from Model.parts.business.user_adoption import *
from Model.parts.business.business_assumptions import *
from Model.parts.business.business_buybacks import *
from Model.parts.agents_behavior.agent_meta_bucket_behavior import *
from Model.parts.utilities.staking_mint_burn import *
from Model.parts.utilities.staking_revenue_share import *
from Model.parts.utilities.staking_vesting import *
from Model.parts.utilities.liquidity_mining import *
from Model.parts.utilities.burning import *
from Model.parts.utilities.holding import *
from Model.parts.utilities.transfer import *

# QTM logic order 
state_update_blocks = [
    ## MODEL STATE UPDATE BLOCKS ##
    {
        # substep 1: ecosystem/token_economy.py
        'policies': {
            'generate_date': generate_date
        },
        'variables': { 
            'date': update_date
        },
    },
    {
        # substep 2: ecosystem/vesting.py
        'policies': {
            'vest_tokens': vest_tokens
        },
        'variables': { 
            'agents': update_agent_vested_tokens,
        },
    },
    {
        # substep 3: ecosystem/incentivisation.py
        'policies': {
            'incentivisation': incentivisation
        },
        'variables': { 
            'agents': update_agents_after_incentivisation,
            'token_economy': update_token_economy_after_incentivisation,
        },
    },
    {
        # substep 4: ecosystem/airdrops.py
        'policies': {
            'airdrops': airdrops
        },
        'variables': { 
            'agents': update_agents_after_airdrops,
            'token_economy': update_token_economy_after_airdrops,
        },
    },
    {
        # substep 5: ecosystem/burn.py
        'policies': {
            'burn_from_protocol_bucket': burn_from_protocol_bucket
        },
        'variables': { 
            'agents': update_protocol_bucket_agent_after_burn,
            'token_economy': update_token_economy_after_protocol_bucket_burn,
        },
    },
    {
        # substep 6: agents_behavior/agent_meta_bucket_behavior.py
        'policies': {
            'generate_agent_meta_bucket_behavior': generate_agent_meta_bucket_behavior,
        },
        'variables': {
            'agents': update_agent_meta_bucket_behavior
        },
    },
    {
        # substep 7: agents_behavior/agent_meta_bucket_behavior.py
        'policies': {
            'agent_meta_bucket_allocations': agent_meta_bucket_allocations,
        },
        'variables': {
            'agents': update_agent_meta_bucket_allocations,
            'token_economy': update_token_economy_meta_bucket_allocations
        },
    },
    {
        # substep 8: business/user_adoption.py
        'policies': {
            'user_adoption_metrics': user_adoption_metrics,
        },
        'variables': {
            'user_adoption': update_user_adoption,
        },
    },
    {
        # substep 9: utilities/staking_vesting.py
        'policies': {
            'staking_vesting_allocation': staking_vesting_allocation,
        },
        'variables': {
            'utilities': update_utilties_after_staking_vesting,
            'agents': update_agents_after_staking_vesting
        },
    },
    {
        # substep 10: utilities/burning.py
        'policies': {
            'burning_agent_allocation': burning_agent_allocation,
        },
        'variables': {
            'agents': update_burning_agent_allocation,
            'utilities': update_burning_meta_allocation,
            'token_economy': update_token_economy_after_utility_burn
        },
    },
    {
        # substep 11: utilities/staking_mint_burn.py
        'policies': {
            'staking_mint_burn': staking_mint_burn,
        },
        'variables': {
            'utilities': update_utilties_after_staking_mint_burn,
            'agents': update_agents_after_staking_mint_burn,
            'token_economy': update_token_economy_after_staking_mint_burn,
        },
    },
    {
        # substep 12: utilities/transfer.py
        'policies': {
            'transfer_agent_allocation': transfer_agent_allocation,
        },
        'variables': {
            'agents': update_agents_after_transfer,
            'utilities': update_utilties_after_transfer,
        },
    },
    {
        # substep 13: business/business_assumptions.py
        'policies': {
            'business_assumption_metrics': business_assumption_metrics,
        },
        'variables': {
            'business_assumptions': update_business_assumptions,
            'utilities': update_buyback_amount_from_revenue_share,
        },
    },
    {
        # substep 14: ecosystem/liquidity_pool.py
        'policies': {
            'liquidity_pool_tx1_after_adoption': liquidity_pool_tx1_after_adoption,
        },
        'variables': {
            'agents': update_agents_tx1_after_adoption,
            'liquidity_pool': update_liquidity_pool_after_transaction,
        },
    },
    {
        # substep 15: utilities/holding.py
        'policies': {
            'holding_agent_allocation': holding_agent_allocation,
        },
        'variables': {
            'agents': update_agents_after_holding,
            'utilities': update_utilties_after_holding,
        },
    },
    {
        # substep 16: utilities/liquidity_mining.py
        'policies': {
            'liquidity_mining_agent_allocation': liquidity_mining_agent_allocation,
        },
        'variables': {
            'agents': update_agents_after_liquidity_mining,
            'utilities': update_utilties_after_liquidity_mining,
        },
    },
    {
        # substep 17: ecosystem/liquidity_pool.py
        'policies': {
            'liquidity_pool_tx2_after_vesting_sell': liquidity_pool_tx2_after_vesting_sell,
        },
        'variables': {
            'liquidity_pool': update_liquidity_pool_after_transaction
        },
    },
    {
        # substep 18: ecosystem/liquidity_pool.py
        'policies': {
            'liquidity_pool_tx3_after_liquidity_addition': liquidity_pool_tx3_after_liquidity_addition,
        },
        'variables': {
            'liquidity_pool': update_liquidity_pool_after_transaction,
        },
    },
    {
        # substep 19: ecosystem/liquidity_pool.py
        'policies': {
            'liquidity_pool_tx4_after_buyback': liquidity_pool_tx4_after_buyback,
        },
        'variables': {
            'liquidity_pool': update_liquidity_pool_after_transaction,
        },
    },
    {
        # substep 20: utilities/staking_revenue_share.py
        'policies': {
            'staking_revenue_share_buyback': staking_revenue_share_buyback,
        },
        'variables': {
            'agents': update_agents_after_staking_revenue_share_buyback,
            'utilities': update_utilities_after_staking_revenue_share_buyback,
        },
    },
    {
        # substep 21: business/business_buybacks.py
        'policies': {
            'business_buyback': business_buyback,
        },
        'variables': {
            'agents': update_agents_after_business_buyback
        },
    },
    {
        # substep 22: ecosystem/incentivisation.py
        'policies': {
            'incentivisation_revenue_share_buyback': incentivisation_revenue_share_buyback,
        },
        'variables': {
            'agents': update_agents_after_incentivisation_revenue_share_buyback,
            'business_assumptions': update_business_assumptions_after_incentivisation_revenue_share_buyback,
            'token_economy': update_token_economy_after_incentivisation_revenue_share
        },
    },
    {
        # substep 23: ecosystem/token_economy.py
        'policies': {
            'token_economy_metrics': token_economy_metrics,
        },
        'variables': {
            'token_economy': update_token_economy,
        },
    }
]
