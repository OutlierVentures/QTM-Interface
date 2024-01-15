import streamlit as st
from UserInterface.plots import *

def utilitiesInput(sys_param, tav_return_dict, ab_return_dict):
    """
    This function creates the utilities section of the UI.
    """
    with st.expander("**Utilities**"):
        st.markdown("### Utilities")
        # Sample nested dictionary for utility values
        utility_values = {
            'Stake': {
                'description': "Stake tokens for fixed APR token rewards.",
                'staking_share': {
                    'value': sys_param['staking_share'][0],
                    'display_name': 'Staking Alloc. / %',
                    'description': 'The percentage of the meta utility bucket allocated supply per timestep that is staked.'
                    },
                'staking_buyback_from_revenue_share': {
                    'value': sys_param['staking_buyback_from_revenue_share'][0],
                    'display_name': 'Revenue Share Buyback / %',
                    'description': 'The percentage of the revenue that is used for buying back and distribute tokens to stakers once the staking vesting bucket runs out of tokens.'
                    },
                'mint_burn_ratio': {
                    'value': sys_param['mint_burn_ratio'][0],
                    'display_name': 'Mint / Burn Ratio',
                    'description': 'The ratio of minted tokens to burned tokens for staking rewards. The remaining tokens are distributed from the staking vesting bucket if an allocation exists.'
                    }
            },
            'Liquidity Mining': {
                'description': 'Provide liquidity to the DEX liquidity pool to receive tokens as incentives at a fixed APR.',
                'liquidity_mining_share': {
                    'value': sys_param['liquidity_mining_share'][0],
                    'display_name': 'Liquidity Mining Alloc. / %',
                    'description': 'The percentage of the meta utility bucket allocated supply per timestep that is used for liquidity mining.'
                    },
                'liquidity_mining_apr': {
                    'value': sys_param['liquidity_mining_apr'][0],
                    'display_name': 'APR / %',
                    'description': 'The liquidity mining incentive fixed APR.'
                    },
                'liquidity_mining_payout_source': {
                    'value': sys_param['liquidity_mining_payout_source'][0],
                    'display_name': 'Payout Source',
                    'description': 'The payout source protocol bucket for the liquidity mining incentives.',
                    'options': ['Reserve', 'Community', 'Foundation']
                    },
            },
            'Burning': {
                'description': 'Burn tokens from the meta utility bucket allocations per timestep.',
                'burning_share': {
                    'value': sys_param['burning_share'][0],
                    'display_name': 'Burning Alloc. / %',
                    'description': 'The percentage of the meta utility bucket allocated supply per timestep that is burned.'
                    },
            },
            'Holding': {
                'description': 'Hold tokens and receive passive token rewards.',
                'holding_share': {
                    'value': sys_param['holding_share'][0],
                    'display_name': 'Holding Alloc. / %',
                    'description': 'The percentage of the meta utility bucket allocated supply per timestep that is added to the overall unallocated (holding) supply.'
                    },
                'holding_apr': {
                    'value': sys_param['holding_apr'][0],
                    'display_name': 'APR / %',
                    'description': 'The token rewards APR for holding the token.'
                    },
                'holding_payout_source': {
                    'value': sys_param['holding_payout_source'][0],
                    'display_name': 'Payout Source',
                    'description': 'The payout source protocol bucket for the holding incentives.',
                    'options': ['Reserve', 'Community', 'Foundation']
                    },
                },
            'Transfer': {
                'description': 'Transfer tokens from the meta utility bucket allocations to a protocol bucket. This can be used to simulate any form of purchases in the ecosystem using the token.',
                'transfer_share': {
                    'value': sys_param['transfer_share'][0],
                    'display_name': 'Transfer Alloc. / %',
                    'description': 'The percentage of the meta utility bucket allocated supply per timestep that is transferred to a protocol bucket.'
                    },
                'transfer_destination': {
                    'value': sys_param['transfer_destination'][0],
                    'display_name': 'Transfer Destination',
                    'description': 'The protocol bucket destination of the transfer.',
                    'options': ['Reserve', 'Community', 'Foundation']
                    },
            }
        }
        
        # add staking target to utility values
        if ab_return_dict["agent_behavior"] == 'random':
            utility_values['Stake'].update({'agent_staking_apr_target':{
                    'value': sys_param['agent_staking_apr_target'][0] if 'agent_staking_apr_target' in sys_param else 10.0,
                    'display_name': 'APR Target / %',
                    'description': 'The agents target APR for staking rewards. Agents with random behavior will prioritize utility allocations over selling on average as long as the staking APR is above the APR target. Only applicable for random agent behavior!'
                    }})
        
        # remove utilities when not activated in the token allocation section
        if not tav_return_dict["incentivisation_toggle"]:
            try:
                utility_values.pop('Incentivisation')
            except:
                pass
        if not tav_return_dict["staking_vesting_toggle"]:
            try:
                utility_values.pop('Stake for Vesting Rewards')
            except:
                pass

        # get initial and default values
        default_utilities = []
        for utility in utility_values:
            for key, val in utility_values[utility].items():
                if '_share' in key and key != 'staking_buyback_from_revenue_share':
                    if val['value'] > 0:
                        default_utilities.append(utility)

        # Let user add a utility from the dropdown
        utility_to_add = st.multiselect("Add a utility:", list(utility_values.keys()), default=default_utilities)
        
        # Display the input fields for the added utilities
        utility_sum = 0
        utility_shares = {}
        for utility in utility_to_add:
            st.markdown("---")
            st.markdown("***" + utility + "***")
            for key, val in utility_values[utility].items():
                if key == 'description':
                    st.write(val)
                else:
                    init_value = val['value']
                    display_name = val['display_name']
                    description = val['description']
                    if 'options' in val:
                        options = val['options']
                        new_val = st.selectbox(display_name, options=options, index=options.index(init_value), help=description)
                    else:
                        new_val = st.number_input(display_name, value=init_value, help=description)
                    
                    utility_values[utility][key]['value'] = new_val

        # check utility sums
        count_staking_utilities = 0
        for utility in utility_to_add:
            for key, val in utility_values[utility].items():    
                if '_share' in key and key != 'staking_buyback_from_revenue_share':
                    utility_sum += val['value']
                    utility_shares[utility] = [val['value']]
            if 'Stake' in utility:
                count_staking_utilities += 1
        
        if utility_sum != 100:
            if utility_sum < 100:
                utility_shares['Undefined'] = [100 - utility_sum]
            st.error(f"The sum of the utility allocations ({round(utility_sum,2)}%) is not equal to 100%. Please adjust the utility shares!", icon="⚠️")
        if count_staking_utilities > 1:
            st.warning(f"Multiple staking utilities are defined. Please make sure if you really want to activate multiple different staking mechanisms at once.", icon="⚠️")
        
        # Display the utility pie chart
        st.markdown("---")
        st.write(f'**Utility shares: {round(utility_sum,2)}%**')
        st.markdown("---")
        utility_pie_plot(utility_shares, utility_values)

        # compose new dictionary with parameter values for utilities
        utility_parameter_choice = {}
        for utility in utility_values:
            for key, val in utility_values[utility].items():
                if key == 'description':
                    pass
                else:
                    if utility not in utility_to_add and key != 'staking_buyback_from_revenue_share' and '_share' in key:
                        utility_parameter_choice[key] = 0
                    else:
                        utility_parameter_choice[key] = val['value']

    ut_return_dict = {
        "utility_values" : utility_values,
        "utility_parameter_choice" : utility_parameter_choice,
        "utility_shares" : utility_shares,
        "utility_sum" : utility_sum,
        "count_staking_utilities" : count_staking_utilities
    }

    return ut_return_dict