import streamlit as st

def consistencyChecksInfo(token_launch, token_launch_date, tav_return_dict, ab_return_dict, ut_return_dict, ba_return_dict, ua_return_dict, timi_return_dict, fr_return_dict):
    # Consistency check for simulation duration
    #if simulation_duration > (ua_return_dict['sim_end'] - ua_return_dict['sim_start']) and ua_return_dict['market'] == 1: 
        
        #st.error("Error: Simulation duration exceeds the selected market simulation period. Please adjust your selection.")
    #    st.session_state['execute_inputs'] = False
    #else:
    #    st.session_state['execute_inputs'] = True   
    
    # Consistency Checks
    if (tav_return_dict['lp_allocation'] < 0 or 
        (ab_return_dict["meta_bucket_alloc_sum"] != 100 and ab_return_dict["agent_behavior"] == 'static') or 
        (tav_return_dict["dex_capital"] > fr_return_dict["raised_funds"] and token_launch) or 
        ut_return_dict["utility_sum"] != 100 or
        (min(tav_return_dict['airdrop_date1'], tav_return_dict['airdrop_date2'], tav_return_dict['airdrop_date3']) < token_launch_date and tav_return_dict['airdrop_toggle']) or
        (ba_return_dict["buyback_start"] < token_launch_date and ba_return_dict["enable_protocol_buybacks"]) or 
        (ba_return_dict["burn_start"] < token_launch_date and ba_return_dict["enable_protocol_burning"]) or
        ba_return_dict["rev_share_sum"] != 100.0 or 
        ("Stake" not in ut_return_dict["utility_to_add"] and ba_return_dict["staker_rev_share"] > 0)):
        st.session_state['execute_inputs'] = False
    else:
        st.session_state['execute_inputs'] = True
    
    if not token_launch:
        if (timi_return_dict["stakeholder_allocations"] + timi_return_dict["lp_allocation_tokens"])/timi_return_dict["required_circulating_supply"]*100 > 100.005:
            st.error(f"Initialized / Required Circulating Supply: {(timi_return_dict['stakeholder_allocations'] + timi_return_dict['lp_allocation_tokens'])*1e6:,.0f} / {timi_return_dict['required_circulating_supply']*1e6:,.0f}  |  {(timi_return_dict['stakeholder_allocations'] + timi_return_dict['lp_allocation_tokens'])/timi_return_dict['required_circulating_supply']*100:,.4f}%. Double check if this allocation matches your intention!", icon="⚠️")
        elif (timi_return_dict["stakeholder_allocations"] + timi_return_dict["lp_allocation_tokens"])/timi_return_dict["required_circulating_supply"]*100 < 99.995:
            st.error(f"Initialized / Required Circulating Supply: {(timi_return_dict['stakeholder_allocations'] + timi_return_dict['lp_allocation_tokens'])*1e6:,.0f} / {timi_return_dict['required_circulating_supply']*1e6:,.0f}  |  {(timi_return_dict['stakeholder_allocations'] + timi_return_dict['lp_allocation_tokens'])/timi_return_dict['required_circulating_supply']*100:,.4f}%. Double check if this allocation matches your intention!", icon="⚠️")
    
    if 'execute_inputs' in st.session_state:
        status_msg = ["✅" if st.session_state['execute_inputs'] else "❌"][0]
    else:
        status_msg = ""
    
    with st.expander("**Consistency Checks**"+ status_msg):
        st.markdown("### Consistency Checks ")
        if 'execute_inputs' in st.session_state:
            if st.session_state['execute_inputs']:
                st.success("All inputs are valid.", icon="✅")
        
        if tav_return_dict["dex_capital"] > fr_return_dict["raised_funds"] and token_launch:
            st.error(f"The required capital ({round(tav_return_dict['dex_capital'],2)}m) to seed the liquidity is higher than the raised funds (${round(fr_return_dict['raised_funds'],2)}m). Please reduce the LP Token Allocation or the Launch Valuation!", icon="⚠️")
        
        if tav_return_dict['lp_allocation'] < 0:
            st.error(f"The LP token allocation ({round(tav_return_dict['lp_allocation'],2)}%) is negative. Reduce the stakeholder allocations!", icon="⚠️")
        
        if tav_return_dict['airdrop_toggle']:
            if tav_return_dict['airdrop_date1'] < token_launch_date:
                st.error(f"The first airdrop date ({tav_return_dict['airdrop_date1'].strftime('%d.%m.%Y')}) is before the launch date ({token_launch_date}). Please adjust the airdrop date!", icon="⚠️")
            if tav_return_dict['airdrop_date2'] < token_launch_date:
                st.error(f"The second airdrop date ({tav_return_dict['airdrop_date2'].strftime('%d.%m.%Y')}) is before the launch date ({token_launch_date}). Please adjust the airdrop date!", icon="⚠️")
            if tav_return_dict['airdrop_date3'] < token_launch_date:
                st.error(f"The third airdrop date ({tav_return_dict['airdrop_date3'].strftime('%d.%m.%Y')}) is before the launch date ({token_launch_date}). Please adjust the airdrop date!", icon="⚠️")

        if ba_return_dict["enable_protocol_buybacks"]:
            if ba_return_dict["buyback_start"] < token_launch_date:
                st.error(f"The buyback starting date ({ba_return_dict['buyback_start'].strftime('%d.%m.%Y')}) is before the launch date ({token_launch_date}). Please adjust the buyback starting date!", icon="⚠️")
        if ba_return_dict["enable_protocol_burning"]:
            if ba_return_dict["burn_start"] < token_launch_date:
                st.error(f"The burn starting date ({ba_return_dict['burn_start'].strftime('%d.%m.%Y')}) is before the launch date ({token_launch_date}). Please adjust the burn starting date!", icon="⚠️")

        if ab_return_dict["meta_bucket_alloc_sum"] != 100 and ab_return_dict["agent_behavior"] == 'static':
            st.error(f"The sum of the average token allocations for utility, selling and holding ({ab_return_dict['avg_token_utility_allocation'] + ab_return_dict['avg_token_selling_allocation'] + ab_return_dict['avg_token_holding_allocation']}%) is not equal to 100%. Please adjust the values!", icon="⚠️")
        
        if ut_return_dict["utility_sum"] != 100:
            st.error(f"The sum of the utility allocations ({ut_return_dict['utility_sum']}%) is not equal to 100%. Please adjust the values!", icon="⚠️")
        
        if ba_return_dict["rev_share_sum"] != 100.0:
            st.error(f"The sum of the revenue share allocations ({ba_return_dict['rev_share_sum']}%) is not equal to 100%. Please adjust the values!", icon="⚠️")

        if "Stake" not in ut_return_dict["utility_to_add"] and ba_return_dict["staker_rev_share"] > 0:
            st.error("You have enabled revenue share for stakers but have not added the staking utility. Please add the staking utility to enable revenue share for stakers.", icon="⚠️")