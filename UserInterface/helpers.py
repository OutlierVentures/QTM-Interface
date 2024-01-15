import streamlit as st
from UserInterface.plots import *
from Model.parts.utils import *
import pandas as pd
from io import BytesIO
from pyxlsb import open_workbook as open_xlsb
import random
from . import basicTokenInformation as bti
from . import fundraising as fr
from . import tokenAllocationsAndVesting as tav
from . import userAdoption as ua
from . import agentBehavior as ab
from . import businessAssumptions as ba
from . import utilities as ut

fundraising_style_map = {
    'Moderate': 2,
    'Medium': 5,
    'Aggressive': 8
}

param_help = {
    'fundraising_style': f"The more aggressive the fundraising style, the more advantageous it is to be an early investor: **Moderate** / **Medium** / **Aggressive** : **{fundraising_style_map['Moderate']}x** / **{fundraising_style_map['Medium']}x** / **{fundraising_style_map['Aggressive']}x** public sale to seed round valuation ratio.",
    'incentivisation': "Enable token incentives for your ecosystem. These can have several applications, e.g. liquidity incentives or behavior/action incentives. Whenever you want to incentivize something through a fixed vesting rewards approach enable the incentivisation allocation.",
    'staking_vesting': "Enable staking vesting token allocations. These tokens will automatically vest as rewards for stakers. Note that the QTM provides 3 different staking mechanisms: **(1) Staking Vesting (2) Staking fixed APR rewards (3) Staking revenue share buybacks and distribute rewards**. At this input you only switch on/off the staking vesting mechanism (1) as it is relevant for the initial token allocations.",
    'airdrops': "Enable airdrops. Airdrops are a great way to distribute tokens to a large number of people. They can be used to incentivize certain actions or to reward early supporters.",
    'vesting_style': f"The vesting style determines how fast the tokens are released. The faster the higher the initial vesting and the lower the cliff and duration months.",
}

def model_ui_inputs(input_file_path, uploaded_file, parameter_list, col01):
    if 'param_id' in st.session_state:
        parameter_id_choice = st.session_state['param_id']
    else:
        parameter_id_choice = ""

    # Adjusting Parameters
    if parameter_id_choice == "":
        sys_param = compose_initial_parameters(pd.read_csv(input_file_path), parameter_list)
        sys_param['avg_token_utility_allocation'] = [sys_param['avg_token_utility_allocation'][0] / 100]
        sys_param['avg_token_holding_allocation'] = [sys_param['avg_token_holding_allocation'][0] / 100]
        sys_param['avg_token_selling_allocation'] = [sys_param['avg_token_selling_allocation'][0] / 100]
        sys_param['avg_token_utility_removal'] = [sys_param['avg_token_utility_removal'][0] / 100]
    else:
        sys_param_df = get_simulation_data('simulationData.db', 'sys_param')
        if len(sys_param_df[sys_param_df['id'] == parameter_id_choice])<1:
            sys_param = compose_initial_parameters(pd.read_csv(input_file_path), parameter_list)
        else:
            sys_param = {k:[v] for k, v in sys_param_df[sys_param_df['id'] == parameter_id_choice].to_dict('index')[list(sys_param_df[sys_param_df['id'] == parameter_id_choice].to_dict('index').keys())[0]].items()}

    with col01:
        token_launch_date = st.date_input("Token Launch Date", value=datetime.strptime(sys_param['launch_date'][0], "%d.%m.%Y"), help="The token launch date is the time when the token becomes liquid to be traded and at which the vesting conditions start to apply. Defining a date before today's date means that the token has already been launched and therefore requires additional information about the current token distribution and valuations in the parameter definitions below.")
        token_launch_date = datetime(token_launch_date.year, token_launch_date.month, token_launch_date.day)
        if token_launch_date > datetime.today():
            token_launch = True
        else:
            token_launch = False


    ##############################################
    # Basic Token Information
    ##############################################

    bti_return_dict = bti.basicTokenInformationInput(sys_param)


    ##############################################
    # Fundraising
    ##############################################
    
    fr_return_dict = fr.fundraisingInput(sys_param, param_help, bti_return_dict["equity_investments"], bti_return_dict["equity_perc"], bti_return_dict["public_sale_supply"], bti_return_dict["launch_valuation"], bti_return_dict["initial_supply"], uploaded_file, fundraising_style_map)

    ##############################################
    # Token Allocations and Vesting
    ##############################################

    tav_return_dict = tav.tokenAllocationsAndVestingInput(sys_param, param_help, bti_return_dict["equity_perc"], fr_return_dict["seed_raised"], fr_return_dict["presale_1_raised"], fr_return_dict["presale_2_raised"], fr_return_dict["public_sale_raised"], fr_return_dict["raised_funds"], bti_return_dict["launch_valuation"], fr_return_dict["seed_valuation"], fr_return_dict["presale_1_valuation"], fr_return_dict["presale_2_valuation"], bti_return_dict["initial_supply"], token_launch_date, token_launch)


    ##############################################
    # User Adoption
    ##############################################

    ua_return_dict = ua.userAdoptionInput(sys_param)


    ##############################################
    # Agent Behavior
    ##############################################

    ab_return_dict = ab.agentBehaviorInput(sys_param, ua_return_dict["adoption_style"], ua_return_dict["adoption_dict"])


    ##############################################
    # Business Assumptions
    ##############################################

    ba_return_dict = ba.businessAssumptionsInput(sys_param, ua_return_dict["adoption_dict"], token_launch_date, fr_return_dict["raised_funds"], token_launch, tav_return_dict["incentivisation_toggle"], tav_return_dict["staking_vesting_toggle"], ua_return_dict["adoption_style"], ua_return_dict["regular_product_revenue_per_user"], ua_return_dict["initial_product_users"], ua_return_dict["show_full_adoption_table"])


    ##############################################
    # Utilities
    ##############################################

    ut_return_dict = ut.utilitiesInput(sys_param, tav_return_dict, ab_return_dict)

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
            vested_dict, vested_supply_sum = calc_vested_tokens_for_stakeholder(token_launch_date, bti_return_dict["initial_supply"], tav_return_dict["vesting_dict"])
            airdropped_supply_sum, remaining_airdrop_supply = calc_airdropped_tokens(token_launch_date, bti_return_dict["initial_supply"], tav_return_dict["airdrop_allocation"], tav_return_dict["airdrop_dict"])

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
                lp_allocation_tokens = st.number_input('LP Token Allocation / m', label_visibility="visible", value=tav_return_dict['lp_allocation'] / 100 * bti_return_dict['initial_supply'], format="%.4f", disabled=False, key="lp_allocation_tokens", help="The percentage of tokens allocated to the liquidity pool. This is the remaining percentage of tokens after all other allocations have been made. It must not be < 0 and determines the required capital to seed the liquidity.")
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
            
    # Map new parameters to model input parameters
    new_params = {
        'token_launch': token_launch,
        'launch_date': token_launch_date.strftime("%d.%m.%Y").split(" ")[0],
        'equity_external_shareholders_perc': bti_return_dict['equity_perc'],
        'initial_total_supply': bti_return_dict['initial_supply']*1e6,
        'public_sale_supply_perc': bti_return_dict['public_sale_supply'],
        'public_sale_valuation': bti_return_dict['launch_valuation'] * 1e6,
        'angel_raised': bti_return_dict['equity_investments'] * 1e6,
        'fundraising_style': fr_return_dict["fundraising_style"],
        'seed_raised': fr_return_dict["seed_raised"]* 1e6,
        'presale_1_raised': fr_return_dict["presale_1_raised"]* 1e6,
        'presale_2_raised': fr_return_dict["presale_2_raised"]* 1e6,
        'public_sale_raised': fr_return_dict["public_sale_raised"]* 1e6,
        'seed_valuation': fr_return_dict["seed_valuation"]* 1e6,
        'presale_1_valuation': fr_return_dict["presale_1_valuation"]* 1e6,
        'presale_2_valuation': fr_return_dict["presale_2_valuation"]* 1e6,
        'vesting_style': tav_return_dict['vesting_style'],
        'angel_initial_vesting': tav_return_dict['angel_initial_vesting'],
        'angel_cliff': tav_return_dict['angel_cliff'],
        'angel_vesting_duration': tav_return_dict['angel_duration'],
        'seed_initial_vesting': tav_return_dict['seed_initial_vesting'],
        'seed_cliff': tav_return_dict['seed_cliff'],
        'seed_vesting_duration': tav_return_dict['seed_duration'],
        'presale_1_initial_vesting': tav_return_dict['presale_1_initial_vesting'],
        'presale_1_cliff': tav_return_dict['presale_1_cliff'],
        'presale_1_vesting_duration': tav_return_dict['presale_1_duration'],
        'presale_2_initial_vesting': tav_return_dict['presale_2_initial_vesting'],
        'presale_2_cliff': tav_return_dict['presale_2_cliff'],
        'presale_2_vesting_duration': tav_return_dict['presale_2_duration'],
        'public_sale_initial_vesting': tav_return_dict['public_sale_initial_vesting'],
        'public_sale_cliff': tav_return_dict['public_sale_cliff'],
        'public_sale_vesting_duration': tav_return_dict['public_sale_duration'],
        'team_allocation': tav_return_dict['team_allocation'],
        'team_initial_vesting': tav_return_dict['team_initial_vesting'],
        'team_cliff': tav_return_dict['team_cliff'],
        'team_vesting_duration': tav_return_dict['team_duration'],
        'ov_allocation': 0,
        'ov_initial_vesting': 0,
        'ov_cliff': 0,
        'ov_vesting_duration': 0,
        'advisor_allocation': tav_return_dict['ov_advisor_allocation'],
        'advisor_initial_vesting': tav_return_dict['advisor_initial_vesting'],
        'advisor_cliff': tav_return_dict['advisor_cliff'],
        'advisor_vesting_duration': tav_return_dict['advisor_duration'],
        'strategic_partners_allocation': tav_return_dict['strategic_partners_allocation'],
        'strategic_partners_initial_vesting': tav_return_dict['strategic_partners_initial_vesting'],
        'strategic_partners_cliff': tav_return_dict['strategic_partners_cliff'],
        'strategic_partners_vesting_duration': tav_return_dict['strategic_partners_duration'],
        'reserve_allocation': tav_return_dict['reserve_allocation'],
        'reserve_initial_vesting': tav_return_dict['reserve_initial_vesting'],
        'reserve_cliff': tav_return_dict['reserve_cliff'],
        'reserve_vesting_duration': tav_return_dict['reserve_duration'],
        'community_allocation': tav_return_dict['community_allocation'],
        'community_initial_vesting': tav_return_dict['community_initial_vesting'],
        'community_cliff': tav_return_dict['community_cliff'],
        'community_vesting_duration': tav_return_dict['community_duration'],
        'foundation_allocation': tav_return_dict['foundation_allocation'],
        'foundation_initial_vesting': tav_return_dict['foundation_initial_vesting'],
        'foundation_cliff': tav_return_dict['foundation_cliff'],
        'foundation_vesting_duration': tav_return_dict['foundation_duration'],
        'incentivisation_allocation': tav_return_dict['incentivisation_allocation'],
        'incentivisation_initial_vesting': tav_return_dict['incentivisation_initial_vesting'],
        'incentivisation_cliff': tav_return_dict['incentivisation_cliff'],
        'incentivisation_vesting_duration': tav_return_dict['incentivisation_duration'],
        'staking_vesting_allocation': tav_return_dict['staking_vesting_allocation'],
        'staking_vesting_initial_vesting': tav_return_dict['staking_vesting_initial_vesting'],
        'staking_vesting_cliff': tav_return_dict['staking_vesting_cliff'],
        'staking_vesting_vesting_duration': tav_return_dict['staking_vesting_duration'],
        'airdrop_allocation': tav_return_dict['airdrop_allocation'],
        'airdrop_date1': [tav_return_dict['airdrop_date1'].strftime('%d.%m.%Y') if tav_return_dict['airdrop_toggle'] else sys_param['airdrop_date1'][0]][0],
        'airdrop_amount1': [tav_return_dict['airdrop_amount1'] if tav_return_dict['airdrop_toggle'] else sys_param['airdrop_amount1'][0]][0],
        'airdrop_date2': [tav_return_dict['airdrop_date2'].strftime('%d.%m.%Y') if tav_return_dict['airdrop_toggle'] else sys_param['airdrop_date2'][0]][0],
        'airdrop_amount2': [tav_return_dict['airdrop_amount2'] if tav_return_dict['airdrop_toggle'] else sys_param['airdrop_amount2'][0]][0],
        'airdrop_date3': [tav_return_dict['airdrop_date3'].strftime('%d.%m.%Y') if tav_return_dict['airdrop_toggle'] else sys_param['airdrop_date3'][0]][0],
        'airdrop_amount3': [tav_return_dict['airdrop_amount3'] if tav_return_dict['airdrop_toggle'] else sys_param['airdrop_amount3'][0]][0],
        'adoption_style': ua_return_dict["adoption_style"] if not ua_return_dict["show_full_adoption_table"] else 'Custom',
        'initial_product_users': ua_return_dict["initial_product_users"],
        'initial_token_holders': ua_return_dict["initial_token_holders"],
        'product_users_after_10y': ua_return_dict["product_users_after_10y"],
        'token_holders_after_10y': ua_return_dict["token_holders_after_10y"],
        'product_adoption_velocity': ua_return_dict["product_adoption_velocity"],
        'token_adoption_velocity': ua_return_dict["token_adoption_velocity"],
        'regular_product_revenue_per_user': ua_return_dict["regular_product_revenue_per_user"],
        'regular_token_buy_per_user': ua_return_dict["regular_token_buy_per_user"],
        'agent_behavior': ab_return_dict["agent_behavior"],
        'avg_token_utility_allocation': ab_return_dict["avg_token_utility_allocation"],
        'avg_token_selling_allocation': ab_return_dict["avg_token_selling_allocation"],
        'avg_token_holding_allocation': ab_return_dict["avg_token_holding_allocation"],
        'avg_token_utility_removal': ab_return_dict["avg_token_utility_removal"] if (ua_return_dict["adoption_style"] == 'Custom' or ua_return_dict["show_full_adoption_table"]) and ab_return_dict["agent_behavior"] == 'static' else ua_return_dict["adoption_dict"][ua_return_dict["adoption_style"]]['avg_token_utility_removal'] if ab_return_dict["agent_behavior"] == 'static' else 0,
        'royalty_income_per_month': ba_return_dict["royalty_income_per_month"] *1e3,
        'treasury_income_per_month': ba_return_dict["treasury_income_per_month"] *1e3,
        'other_income_per_month': ba_return_dict["other_income_per_month"]*1e3,
        'one_time_payments_1': ba_return_dict["one_time_payments_1"]*1e3,
        'salaries_per_month': ba_return_dict["salaries_per_month"]*1e3,
        'license_costs_per_month': ba_return_dict["license_costs_per_month"]*1e3,
        'other_monthly_costs': ba_return_dict["other_monthly_costs"]*1e3,
        'buyback_perc_per_month': ba_return_dict["buyback_perc_per_month"],
        'buyback_fixed_per_month': ba_return_dict["buyback_fixed_per_month"]*1e3,
        'buyback_bucket': ba_return_dict["buyback_bucket"],
        'buyback_start': ba_return_dict["buyback_start"].strftime('%d.%m.%Y'),
        'buyback_end': ba_return_dict["buyback_end"].strftime('%d.%m.%Y'),
        'burn_per_month': ba_return_dict["burn_per_month"],
        'burn_bucket': ba_return_dict["burn_bucket"],
        'burn_start': ba_return_dict["burn_start"].strftime('%d.%m.%Y'),
        'burn_end': ba_return_dict["burn_end"].strftime('%d.%m.%Y'),
    }

    # add utility parameters to new_params
    new_params.update(ut_return_dict["utility_parameter_choice"])

    # add random seed to new_params
    if ab_return_dict["agent_behavior"] == 'random':
        new_params['random_seed'] = ab_return_dict["random_seed"]

    # add in-market initialization parameters to new_params
    if not token_launch:
        new_params['initial_total_supply'] = current_initial_supply*1e6
        new_params.update({
            'token_fdv': token_fdv*1e6,
            'token_holding_ratio_share': token_holding_ratio_share,
            'lp_allocation_tokens': lp_allocation_tokens*1e6
        })
        # add current_holdings, current_staked, and vested_dict dict entries to new_params
        for stakeholder in vested_dict:
            if tav_return_dict['vesting_dict'][stakeholder]['allocation'] > 0:
                new_params.update({
                    f'{stakeholder if stakeholder is not "incentivisation" else "incentivisation_receivers"}_current_holdings': current_holdings[stakeholder if stakeholder is not 'incentivisation' else 'incentivisation_receivers']*1e6,
                    f'{stakeholder if stakeholder is not "incentivisation" else "incentivisation_receivers"}_current_staked': current_staked[stakeholder if stakeholder is not 'incentivisation' else 'incentivisation_receivers']*1e6,
                    f'{stakeholder}_vested_init': vested_dict[stakeholder]*1e6,
                })
        # add airdrop receivers to new_params
        if tav_return_dict['airdrop_toggle']:
            new_params.update({
                'airdrop_receivers_current_holdings': current_holdings['airdrop_receivers']*1e6,
                'airdrop_receivers_current_staked': current_staked['airdrop_receivers']*1e6,
                'airdrop_receivers_vested_init': 0,
            })

        # add market investors to new_params
        new_params.update({
            'market_investors_current_holdings': current_holdings['market_investors']*1e6,
            'market_investors_current_staked': current_staked['market_investors']*1e6,
            'market_investors_vested_init': 0,
        })
        new_params['initial_cash_balance'] = ba_return_dict["initial_cash_balance"]*1e3

    # Consistency Checks
    if (tav_return_dict['lp_allocation'] < 0 or (ab_return_dict["meta_bucket_alloc_sum"] != 100 and ab_return_dict["agent_behavior"] == 'static') or (tav_return_dict["dex_capital"] > fr_return_dict["raised_funds"] and token_launch) or ut_return_dict["utility_sum"] != 100 or
        (min(tav_return_dict['airdrop_date1'], tav_return_dict['airdrop_date2'], tav_return_dict['airdrop_date3']) < token_launch_date and tav_return_dict['airdrop_toggle']) or
        (ba_return_dict["buyback_start"] < token_launch_date and ba_return_dict["enable_protocol_buybacks"]) or (ba_return_dict["burn_start"] < token_launch_date and ba_return_dict["enable_protocol_burning"]) or
        (ba_return_dict["initial_cash_balance"] == 0 and (ba_return_dict["royalty_income_per_month"] + ba_return_dict["treasury_income_per_month"] + ba_return_dict["other_income_per_month"] + ua_return_dict["initial_product_users"] *
                                        [ua_return_dict["regular_product_revenue_per_user"] if ua_return_dict["adoption_style"] == 'Custom' or ua_return_dict["show_full_adoption_table"] else ua_return_dict["adoption_dict"][ua_return_dict["adoption_style"]]['regular_product_revenue_per_user']][0] -
                                        ba_return_dict["salaries_per_month"] - ba_return_dict["license_costs_per_month"] - ba_return_dict["other_monthly_costs"]) and not token_launch)):
        st.session_state['execute_inputs'] = False
    else:
        st.session_state['execute_inputs'] = True
    
    if not token_launch:
        if (stakeholder_allocations + lp_allocation_tokens)/required_circulating_supply*100 > 100.005 or (stakeholder_allocations + lp_allocation_tokens)/required_circulating_supply*100 < 99.995:
            st.session_state['execute_inputs'] = False
        else:
            st.session_state['execute_inputs'] = True
    
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
        
        if not token_launch:
            if (ba_return_dict["initial_cash_balance"] == 0 and (ba_return_dict["royalty_income_per_month"] + ba_return_dict["treasury_income_per_month"] + ba_return_dict["other_income_per_month"] + ua_return_dict["initial_product_users"] *
                                               [ua_return_dict["regular_product_revenue_per_user"] if ua_return_dict["adoption_style"] == 'Custom' or ua_return_dict["show_full_adoption_table"] else ua_return_dict["adoption_dict"][ua_return_dict["adoption_style"]]['regular_product_revenue_per_user']][0] -
                                               ba_return_dict["salaries_per_month"] - ba_return_dict["license_costs_per_month"] - ba_return_dict["other_monthly_costs"]) and not token_launch):
                st.error(f"The initial cash balance is 0. Please adjust the initial cash balance or the monthly income and cost parameters!", icon="⚠️")
            
            if (stakeholder_allocations + lp_allocation_tokens)/required_circulating_supply*100 > 100.005:
                st.error(f"Initialized / Required Circulating Supply: {(stakeholder_allocations + lp_allocation_tokens)*1e6:,.0f} / {required_circulating_supply*1e6:,.0f}  |  {(stakeholder_allocations + lp_allocation_tokens)/required_circulating_supply*100:,.4f}%. Double check if this allocation matches your intention!", icon="⚠️")
            elif (stakeholder_allocations + lp_allocation_tokens)/required_circulating_supply*100 < 99.995:
                st.error(f"Initialized / Required Circulating Supply: {(stakeholder_allocations + lp_allocation_tokens)*1e6:,.0f} / {required_circulating_supply*1e6:,.0f}  |  {(stakeholder_allocations + lp_allocation_tokens)/required_circulating_supply*100:,.4f}%. Double check if this allocation matches your intention!", icon="⚠️")



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
        
        if ut_return_dict["count_staking_utilities"] > 1:
            st.warning(f"Multiple staking utilities are defined. Please make sure if you really want to activate multiple different staking mechanisms at once.", icon="⚠️")

    col111, col112, col113, col114, col115 = st.columns(5)
    with col111:
        simulation_duration = st.number_input('Simulation Duration / Months', label_visibility="visible", min_value=1, value=int(sys_param['simulation_duration'][0]) if 'simulation_duration' in sys_param else 60, disabled=False, key="simulation_duration", help="The duration of the simulation in months. Note that longer simulation times require more computation time.")
        new_params.update({'simulation_duration': simulation_duration})

    return new_params

def delete_parameter_and_simulation_data(param_id):
    # delete current selected parameter set and simulation data from database
    conn = sqlite3.connect('simulationData.db')
    cur = conn.cursor()
    try:
        cur.execute(''' DELETE FROM simulation_data_{param_id} '''.format(param_id=param_id))
    except:
        pass
    try:
        cur.execute(''' DELETE FROM sys_param WHERE id = ? ''', (param_id,))
    except:
        pass
    conn.commit()
    conn.close()

def calc_vested_tokens_for_stakeholder(token_launch_date, initial_supply, vesting_dict):
    vested_supply_sum = 0
    vested_dict = {}
    
    # use the vesting dictionary to calculate the vested supply for each stakeholder considering the current date, the token_launch_date, the initial vesting, the cliff and the vesting duration
    passed_months = np.abs(int(months_difference(token_launch_date, datetime.today())))
    
    for stakeholder in vesting_dict:
        allocation = vesting_dict[stakeholder]['allocation']
        initial_vesting = vesting_dict[stakeholder]['initial_vesting']
        cliff = vesting_dict[stakeholder]['cliff']
        duration = vesting_dict[stakeholder]['duration']
        if passed_months <= cliff:
            vested_supply = initial_vesting/100 * allocation/100 * initial_supply
        elif passed_months <= duration + cliff:
            vested_supply = initial_vesting/100 * allocation/100 * initial_supply + ((passed_months - cliff) / duration) * (allocation/100 * (1-initial_vesting/100)) * initial_supply
        else:
            vested_supply = allocation/100 * initial_supply
        vested_supply_sum += vested_supply
        vested_dict[stakeholder] = vested_supply
    
    return vested_dict, vested_supply_sum

def calc_airdropped_tokens(token_launch_date, initial_supply, airdrop_allocation, airdrop_dict):
    airdropped_supply_sum = 0

    for airdrop in airdrop_dict:
        amount = airdrop_dict[airdrop]['amount']
        date = datetime.strptime(airdrop_dict[airdrop]['date'], "%d.%m.%Y")
        if date > token_launch_date and date < datetime.today():
            airdropped_supply_sum += amount/100 * airdrop_allocation/100 * initial_supply

    remaining_airdrop_supply = initial_supply * airdrop_allocation / 100 - airdropped_supply_sum
    
    return airdropped_supply_sum, remaining_airdrop_supply

def to_excel(df):
    output = BytesIO()
    writer = pd.ExcelWriter(output, engine='xlsxwriter')
    df.to_excel(writer, index=False, sheet_name='Sheet1')
    workbook = writer.book
    worksheet = writer.sheets['Sheet1']
    format1 = workbook.add_format({'num_format': '0.00'}) 
    worksheet.set_column('A:A', None, format1)  
    writer.save()
    processed_data = output.getvalue()
    return processed_data