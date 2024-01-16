import streamlit as st
from . import helpers
from Model.sys_params import *

def tokenInMarketInitializationInput(token_launch_date, token_launch, bti_return_dict, ut_return_dict, ab_return_dict, tav_return_dict, sys_param):

    stakeholder_allocations_fixed = 0
    stakeholder_allocations = 0
    lp_allocation_tokens = tav_return_dict["lp_allocation"] / 100 * bti_return_dict["initial_supply"]
    required_circulating_supply = 0
    if not token_launch:
        with st.expander("**Token In-Market Initialization (for already launched tokens)**"):
            st.markdown("### Token In-Market Initialization")
            st.markdown("Use the following input parameters to initialize the model for a token that already launched in the market. Note that all the above settings will still be valid and important for the simulation.")

            current_holdings = {}
            current_staked = {}
            vested_dict, vested_supply_sum = helpers.calc_vested_tokens_for_stakeholder(token_launch_date, bti_return_dict["initial_supply"], tav_return_dict["vesting_dict"])
            airdropped_supply_sum, remaining_airdrop_supply = helpers.calc_airdropped_tokens(token_launch_date, bti_return_dict["initial_supply"], tav_return_dict["airdrop_allocation"], tav_return_dict["airdrop_dict"])

            col101, col102 = st.columns(2)
            with col101:
                current_initial_supply = st.number_input('Total Supply / m', label_visibility="visible", min_value=vested_supply_sum + airdropped_supply_sum + tav_return_dict["lp_allocation"] / 100 * bti_return_dict["initial_supply"], value=bti_return_dict["initial_supply"], disabled=False, key="initial_supply", help="The total token supply. This can be different from the initial total supply if tokens got minted or burned since token launch.")
                if bti_return_dict["initial_supply"] < current_initial_supply:
                    st.info(f"The current total supply ({current_initial_supply}m) is higher than the initial total supply ({bti_return_dict['initial_supply']}m). This means that new tokens got **minted** since token launch.", icon="ℹ️")
                if bti_return_dict["initial_supply"] > current_initial_supply:
                    st.info(f"The current total supply ({current_initial_supply}m) is lower than the initial total supply ({bti_return_dict['initial_supply']}m). This means that tokens got **burned** since token launch.", icon="ℹ️")
                
                burned_supply = bti_return_dict["initial_supply"] - current_initial_supply if current_initial_supply < bti_return_dict["initial_supply"] else 0
                minted_supply = current_initial_supply - bti_return_dict["initial_supply"] if current_initial_supply > bti_return_dict["initial_supply"] else 0
                
                token_fdv = st.number_input('Current Token FDV / $m', label_visibility="visible", min_value=0.1, value=bti_return_dict["launch_valuation"] if 'token_fdv' not in sys_param else sys_param['token_fdv'][0]/1e6, disabled=False, key="token_fdv", help="The token fully diluted valuation.")

            with col102:
                total_in_market_vested_tokens = st.text_input('Total Emitted Tokens / m', value=f"{round(vested_supply_sum + airdropped_supply_sum + tav_return_dict['lp_allocation'] / 100 * bti_return_dict['initial_supply'],2)}m", disabled=True, key=f"vested_supply_sum", help="Total amount of vested tokens according to the vesting schedule and token launch date.")
                st.text_input('Total Emitted Tokens / % init. total supply', value=f"{round((vested_supply_sum + airdropped_supply_sum + tav_return_dict['lp_allocation'] / 100 * bti_return_dict['initial_supply'])/bti_return_dict['initial_supply']*100,2)}%", disabled=True, key=f"vested_supply_sum_perc", help="Total amount of vested tokens as percentage share of the total supply according to the vesting schedule and token launch date.")

            staking_vesting_vested = vested_dict['staking_vesting']
            stakeholder_names, stakeholder_name_mapping = get_stakeholders()

            col101a, col102a, col103a = st.columns(3)
            with col101a:
                col101b, col102b = st.columns(2)
                with col101b:
                    st.text_input('Blank', value="", label_visibility="hidden", disabled=True, key=f"blank_1")
                with col102b:
                    st.text_input('Blank', value="", label_visibility="hidden", disabled=True, key=f"blank_2")
                st.write("**Stakeholder**")
                for stakeholder in vested_dict:
                    if tav_return_dict['vesting_dict'][stakeholder]['allocation'] > 0:
                        st.text_input('Stakeholder', value=[stakeholder if stakeholder is not 'incentivisation' else 'incentivisation_receivers'][0].replace("_"," ").title(), label_visibility="collapsed", disabled=True, key=f"stakeholder_{stakeholder}")
                if tav_return_dict['airdrop_toggle']:
                    st.text_input('Airdrop Receivers', value='Airdrop Receivers', label_visibility="collapsed", disabled=True, key=f"stakeholder_airdrop_receivers")
                st.text_input('Market Investors', value='Market Investors', label_visibility="collapsed", disabled=True, key=f"stakeholder_market_investors")
                st.text_input('DEX Liquidity Pool', value='DEX Liquidity Pool', label_visibility="hidden", disabled=True, key=f"dex_liquidity_pool_in_market")
            
            with col102a:
                if 'Stake' not in ut_return_dict["utility_shares"]:
                    token_holding_ratio_share = st.number_input("Token Holding Ratio Share / %", value=100, disabled=True, key="avg_token_holding_allocation1", help="The currently held token supply share by the stakeholders")
                else:
                    token_holding_ratio_share = st.number_input("Token Holding Ratio Share / %", value=ab_return_dict["avg_token_holding_allocation"] if 'token_holding_ratio_share' not in sys_param else sys_param['token_holding_ratio_share'][0], disabled=False, key="avg_token_holding_allocation2", help="The currently held token supply share by the stakeholders")
                st.write("**Token Holdings / m**")
                for stakeholder in vested_dict:
                    if tav_return_dict['vesting_dict'][stakeholder]['allocation'] > 0:
                        current_holdings[stakeholder if stakeholder is not 'incentivisation' else 'incentivisation_receivers'] = st.number_input(f'Token Holdings ({stakeholder if stakeholder is not "incentivisation" else "incentivisation_receivers"}) / m', label_visibility="collapsed", format="%.4f", min_value=0.0, value=vested_dict[stakeholder]*token_holding_ratio_share/100 if stakeholder != 'staking_vesting' else 0.0, disabled=False if stakeholder != 'staking_vesting' else True, key=f"current_holdings_{stakeholder if stakeholder is not 'incentivisation' else 'incentivisation_receivers'}", help=f"The current holdings of {stakeholder if stakeholder is not 'incentivisation' else 'incentivisation_receivers'}.")
                if tav_return_dict['airdrop_toggle']:
                    current_holdings['airdrop_receivers'] = st.number_input(f'Token Holdings (Airdrop Receivers) / m', label_visibility="collapsed", format="%.4f", min_value=0.0, value=float(airdropped_supply_sum)*token_holding_ratio_share/100, disabled=False, key=f"current_holdings_airdrop_receivers", help=f"The current holdings of the airdrop receivers.")
                current_holdings['market_investors'] = st.number_input(f'Token Holdings (Market Investors) / m', label_visibility="collapsed", format="%.4f", min_value=0.0, value=float(sys_param['market_investors_current_holdings'][0]/1e6) if 'market_investors_current_holdings' in sys_param else (staking_vesting_vested + minted_supply - burned_supply) * token_holding_ratio_share/100 if (staking_vesting_vested + minted_supply - burned_supply) >= 0 else 0.0, disabled=False, key=f"current_holdings_market_investors", help=f"The current holdings of the market investors.")
            
            with col103a:
                if 'Stake' in ut_return_dict["utility_shares"]:
                    st.number_input("Token Staking Ratio Share / %", min_value=0.0, value=100.0-token_holding_ratio_share, disabled=True, key="avg_token_utility_allocation1", help="The currently staked token supply share by the stakeholders as ")
                    st.write("**Tokens Staked / m**")
                    for stakeholder in vested_dict:
                        if tav_return_dict['vesting_dict'][stakeholder]['allocation'] > 0:
                            current_staked[stakeholder if stakeholder is not 'incentivisation' else 'incentivisation_receivers'] = st.number_input(f'Tokens Staked ({stakeholder if stakeholder is not "incentivisation" else "incentivisation_receivers"}) / m', label_visibility="collapsed", format="%.4f", min_value=0.0, value=vested_dict[stakeholder]*(1-token_holding_ratio_share/100) if stakeholder != 'staking_vesting' else 0.0, disabled=False if stakeholder != 'staking_vesting' else True, key=f"current_staked_{stakeholder if stakeholder is not 'incentivisation' else 'incentivisation_receivers'}", help=f"The current staked tokens of {stakeholder if stakeholder is not 'incentivisation' else 'incentivisation_receivers'}.")
                    if tav_return_dict['airdrop_toggle']:
                        current_staked['airdrop_receivers'] = st.number_input(f'Tokens Staked (Airdrop Receivers) / m', label_visibility="collapsed", format="%.4f", min_value=0.0, value=float(airdropped_supply_sum)*(1-token_holding_ratio_share/100), disabled=False, key=f"current_staked_airdrop_receivers", help=f"The current staked tokens of the airdrop receivers.")
                    current_staked['market_investors'] = st.number_input(f'Tokens Staked (Market Investors) / m', label_visibility="collapsed", format="%.4f", min_value=0.0, value=float(sys_param['market_investors_current_staked'][0]/1e6) if 'market_investors_current_staked' in sys_param else (staking_vesting_vested + minted_supply - burned_supply) * (1-token_holding_ratio_share/100) if (staking_vesting_vested + minted_supply - burned_supply) >= 0 else 0.0, disabled=False, key=f"current_staked_market_investors", help=f"The current staked tokens of the market investors.")
            
            # calculate stakeholder allocation amounts
            for stakeholder in tav_return_dict['vesting_dict']:
                stakeholder_allocations_fixed += tav_return_dict['vesting_dict'][stakeholder]['allocation']
            stakeholder_allocations_fixed += tav_return_dict['airdrop_allocation'] if tav_return_dict['airdrop_toggle'] else 0
            for stakeholder in current_holdings:
                stakeholder_allocations += current_holdings[stakeholder] + current_staked[stakeholder]
            
            with col102a:
                lp_allocation_tokens = st.number_input('LP Token Allocation / m', label_visibility="visible", value=sys_param['lp_allocation_tokens'][0]/1e6 if 'lp_allocation_tokens' in sys_param else tav_return_dict['lp_allocation'] / 100 * bti_return_dict['initial_supply'], format="%.4f", disabled=False, key="lp_allocation_tokens", help="The percentage of tokens allocated to the liquidity pool. This is the remaining percentage of tokens after all other allocations have been made. It must not be < 0 and determines the required capital to seed the liquidity.")
            with col103a:
                tav_return_dict["dex_capital"] = st.number_input('DEX Capital / $m', value=lp_allocation_tokens * token_fdv / current_initial_supply, disabled=True, key="liquidity_capital_requirements1", help="The required capital to seed the liquidity: left over lp token allocation x total_initial_supply / 100 % * token_launch_price.")

            required_circulating_supply = vested_supply_sum + airdropped_supply_sum + tav_return_dict['lp_allocation'] / 100 * bti_return_dict['initial_supply'] - burned_supply + minted_supply

            col101c, col102c, col103c, col104c = st.columns(4)
            with col101c:
                st.write("**Initial Total Supply**")
                st.write(f"**Current Supply**")
                st.write(f"**Burned Supply**")
                st.write(f"**Minted Supply**")
                st.write(f"**Initialized Circulating Supply**")
                st.write(f"**Required Circulating Supply**")
            with col102c:
                st.write(f"**{bti_return_dict['initial_supply']:,.4f}m**")
                st.write(f"**{current_initial_supply:,.4f}m**")
                st.write(f"**{burned_supply:,.4f}m**")
                st.write(f"**{minted_supply:,.4f}m**")
                st.write(f"**{stakeholder_allocations + lp_allocation_tokens:,.4f}m**")
                st.write(f"**{required_circulating_supply:,.4f}m**")
                
            if (stakeholder_allocations + lp_allocation_tokens)/required_circulating_supply*100 > 100.005:
                st.error(f"Initialized / Required Circulating Supply: {(stakeholder_allocations + lp_allocation_tokens)*1e6:,.0f} / {required_circulating_supply*1e6:,.0f}  |  {(stakeholder_allocations + lp_allocation_tokens)/required_circulating_supply*100:,.4f}%. Double check if this allocation matches your intention!", icon="⚠️")
            elif (stakeholder_allocations + lp_allocation_tokens)/required_circulating_supply*100 < 99.995:
                st.error(f"Initialized / Required Circulating Supply: {(stakeholder_allocations + lp_allocation_tokens)*1e6:,.0f} / {required_circulating_supply*1e6:,.0f}  |  {(stakeholder_allocations + lp_allocation_tokens)/required_circulating_supply*100:,.4f}%. Double check if this allocation matches your intention!", icon="⚠️")
            else:
                st.success(f"Initialized / Required Circulating Supply: {(stakeholder_allocations + lp_allocation_tokens)*1e6:,.0f} / {required_circulating_supply*1e6:,.0f}  |  {(stakeholder_allocations + lp_allocation_tokens)/required_circulating_supply*100:,.4f}%")

            # calculate the amount of tokens held and staked per stakeholder and check if the sum is greater than their initial allocation
            for stakeholder in current_holdings:
                if stakeholder != 'market_investors':
                    if stakeholder == 'airdrop_receivers':
                        if current_holdings[stakeholder] + current_staked[stakeholder] > airdropped_supply_sum + remaining_airdrop_supply:
                            st.warning(f"The current airdrop receiver holdings ({round(current_holdings[stakeholder],2)}m) plus staked supply ({round(current_staked[stakeholder],2)}m) are greater than the overall airdrop allocation ({round(tav_return_dict['airdrop_allocation'],2)}m). Double check if this allocation matches your intention!", icon="⚠️")
                    else:
                        if current_holdings[stakeholder] + current_staked[stakeholder] > tav_return_dict['vesting_dict'][stakeholder if stakeholder is not 'incentivisation_receivers' else 'incentivisation']['allocation']:
                            st.warning(f"The current holdings ({round(current_holdings[stakeholder],2)}m) plus staked supply ({round(current_staked[stakeholder],2)}m) are greater than the initial allocation ({round(tav_return_dict['vesting_dict'][stakeholder if stakeholder is not 'incentivisation_receivers' else 'incentivisation']['allocation'],2)}m) for {stakeholder}. Double check if this allocation matches your intention!", icon="⚠️")

            if lp_allocation_tokens < 0:
                st.error(f"The LP token allocation ({round(tav_return_dict['lp_allocation'],2)}m) is negative. Reduce stakeholder allocations!", icon="⚠️")
    
    else:
        current_initial_supply = bti_return_dict["initial_supply"]
        token_fdv = bti_return_dict["launch_valuation"]
        current_holdings = {}
        current_staked = {}
        vested_dict, vested_supply_sum = helpers.calc_vested_tokens_for_stakeholder(token_launch_date, bti_return_dict["initial_supply"], tav_return_dict["vesting_dict"])
        airdropped_supply_sum, remaining_airdrop_supply = helpers.calc_airdropped_tokens(token_launch_date, bti_return_dict["initial_supply"], tav_return_dict["airdrop_allocation"], tav_return_dict["airdrop_dict"])
        stakeholder_allocations_fixed = 0
        stakeholder_allocations = 0
        lp_allocation_tokens = tav_return_dict["lp_allocation"] / 100 * bti_return_dict["initial_supply"]
        required_circulating_supply = vested_supply_sum + airdropped_supply_sum + tav_return_dict["lp_allocation"] / 100 * bti_return_dict["initial_supply"]
        token_holding_ratio_share = 100
    
    timi_return_dict = {
        "current_initial_supply": current_initial_supply,
        "token_fdv": token_fdv,
        "vested_dict": vested_dict,
        "airdropped_supply_sum": airdropped_supply_sum,
        "remaining_airdrop_supply": remaining_airdrop_supply,
        "current_holdings": current_holdings,
        "current_staked": current_staked,
        "stakeholder_allocations_fixed": stakeholder_allocations_fixed,
        "stakeholder_allocations": stakeholder_allocations,
        "lp_allocation_tokens": lp_allocation_tokens,
        "required_circulating_supply": required_circulating_supply,
        "token_holding_ratio_share": token_holding_ratio_share
    }

    return timi_return_dict
