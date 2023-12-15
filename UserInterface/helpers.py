import streamlit as st
from plots import *
from Model.parts.utils import *
import pandas as pd
from io import BytesIO
from pyxlsb import open_workbook as open_xlsb
import random

fundraising_style_map = {
    'Moderate': 2,
    'Medium': 5,
    'Aggressive': 10
}

param_help = {
    'fundraising_style': f"Themore aggressive the fundraising style, the more advantageous it is to be an early investor: **Moderate** / **Medium** / **Aggressive** : **{fundraising_style_map['Moderate']}x** / **{fundraising_style_map['Medium']}x** / **{fundraising_style_map['Aggressive']}x** public sale to seed round valuation ratio.",
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
        token_launch_date = st.date_input("Token Launch Date", value=datetime.strptime(sys_param['launch_date'][0], "%d.%m.%Y"), help="The token launch date is the time when the token becomes liquid to be traded and at which the vesting conditions start to apply. Defining a date before the today's date means that the token has already been launched and therefore requires additional information about the current token distribution and valuations in the parameter definitions below.")
        token_launch_date = datetime(token_launch_date.year, token_launch_date.month, token_launch_date.day)
        if token_launch_date > datetime.today():
            token_launch = True
        else:
            token_launch = False

    with st.expander("**Basic Token Information**"):
        st.markdown("### Basic Token Information")
        col11, col12, col13 = st.columns(3)            
        with col11:
            equity_investors = st.toggle('Equity Investors', value=sys_param['equity_external_shareholders_perc'][0] != 0.0, help="Enable early equity angel investors")
            initial_supply = st.number_input('Initial Total Token Supply / mil.', min_value=0.001, max_value=1000000.0, value=float(sys_param['initial_total_supply'][0]/1e6) , help="The initial total token supply.")
        with col12:
            launch_valuation = st.number_input('Public Sale Valuation / $m', min_value=0.1, max_value=500.0, value=float(sys_param['public_sale_valuation'][0]/1e6), help="This is the valuation at which the public sale tokens are sold. It is equivalent to the token launch valuation.")
            public_sale_supply = st.number_input('Public Sale Supply / %', min_value=0.0, max_value=95.0, value=float(str(sys_param['public_sale_supply_perc'][0]).split("%")[0]), help="The percentage of tokens sold in the public sale.")
            st.write("Launch Price: "+ str(launch_valuation/initial_supply)+" $/token")
        with col13:
            if equity_investors:
                equity_investments = st.number_input('Angel & Equity Raises / $m', min_value=0.0, value=float(sys_param['angel_raised'][0]/1e6), help="The amount of money raised from equity investors.")
                equity_perc = st.number_input('Equity sold / %', min_value=0.0, max_value=100.0, value=float(str(sys_param['equity_external_shareholders_perc'][0]).split("%")[0]), help="The percentage of equity sold to external shareholders.")
            else:
                equity_investments = 0.0
                equity_perc = 0.0        
    
    with st.expander("**Fundraising**"):
        st.markdown("### Fundraising")
        col21, col22, col23, col24 = st.columns(4)
        with col21:
            fundraising_style_choices = ['Moderate', 'Medium', 'Aggressive','Custom']
            fundraising_style = st.radio('Fundraising Style',tuple(fundraising_style_choices), index=fundraising_style_choices.index(sys_param['fundraising_style'][0]) if 'fundraising_style' in sys_param else 0, help=param_help['fundraising_style'])
            if fundraising_style != 'Custom':
                show_full_fund_table = st.toggle('Show Full Table', value=False, help="Show the full token fundraising table.")
            else:
                show_full_fund_table = False
            if fundraising_style != 'Custom':
                target_raise = st.number_input('Overall Capital Raise Target / $m', min_value=0.1, value=float(sys_param['raised_capital_sum'][0])/1e6, help="The overall capital raise target. This is the amount of money raised that will partially be used to seed the DEX liquidity and as a buffer for the financial runway.")
                left_over_raise = target_raise - equity_investments - launch_valuation * (public_sale_supply/100)
        with col23:
            if fundraising_style != 'Custom' and not show_full_fund_table:
                seed_valuation = np.linspace(launch_valuation/fundraising_style_map[fundraising_style], launch_valuation, 4)[0]
                presale_1_valuation = np.linspace(launch_valuation/fundraising_style_map[fundraising_style], launch_valuation, 4)[1]
                presale_2_valuation = np.linspace(launch_valuation/fundraising_style_map[fundraising_style], launch_valuation, 4)[2]
            else:
                seed_valuation = st.number_input('Seed Valuation / $m', min_value=0.01, value=float([np.linspace(launch_valuation/fundraising_style_map[fundraising_style], launch_valuation, 4)[0] if uploaded_file is None and fundraising_style != 'Custom' else float(sys_param['seed_valuation'][0]/1e6)][0]), help="The valuation of the seed round.")
                presale_1_valuation = st.number_input('Presale 1 Valuation / $m', min_value=0.01, value=float([np.linspace(launch_valuation/fundraising_style_map[fundraising_style], launch_valuation, 4)[1] if uploaded_file is None and fundraising_style != 'Custom' else float(sys_param['presale_1_valuation'][0]/1e6)][0]), help="The valuation of the first presale.")
                presale_2_valuation = st.number_input('Presale 2 Valuation / $m', min_value=0.01, value=float([np.linspace(launch_valuation/fundraising_style_map[fundraising_style], launch_valuation, 4)[2] if uploaded_file is None and fundraising_style != 'Custom' else float(sys_param['presale_2_valuation'][0]/1e6)][0]), help="The valuation of the second presale.")
                st.number_input("Public Sale Valuation / $m", disabled=True, value=launch_valuation, help="The valuation of the public sale defined in the Basic Token Information section.")

        with col22:
            valuation_weights = {
                "seed" : seed_valuation / launch_valuation,
                "presale_1" : presale_1_valuation / launch_valuation,
                "presale_2" : presale_2_valuation / launch_valuation
            }
            valuation_weights_sum = sum(valuation_weights.values())
            if fundraising_style != 'Custom' and not show_full_fund_table:
                seed_raised = float(valuation_weights["seed"]/valuation_weights_sum * left_over_raise)
                presale_1_raised = float(valuation_weights["presale_1"]/valuation_weights_sum * left_over_raise)
                presale_2_raised = float(valuation_weights["presale_2"]/valuation_weights_sum * left_over_raise)
                public_sale_raised = launch_valuation * (public_sale_supply/100)
                raised_funds = equity_investments + seed_raised + presale_1_raised + presale_2_raised + public_sale_raised
            else:
                seed_raised = st.number_input('Seed Raises / $m', min_value=0.0, value=float([valuation_weights["seed"]/valuation_weights_sum * left_over_raise if uploaded_file is None and fundraising_style != 'Custom' else float(sys_param['seed_raised'][0]/1e6)][0]), help="The amount of money raised in the seed round.")
                presale_1_raised = st.number_input('Presale 1 Raises / $m', min_value=0.0, value=float([valuation_weights["presale_1"]/valuation_weights_sum * left_over_raise if uploaded_file is None and fundraising_style != 'Custom' else float(sys_param['presale_1_raised'][0]/1e6)][0]), help="The amount of money raised in the first presale.")
                presale_2_raised = st.number_input('Presale 2 Raises / $m', min_value=0.0, value=float([valuation_weights["presale_2"]/valuation_weights_sum * left_over_raise if uploaded_file is None and fundraising_style != 'Custom' else float(sys_param['presale_2_raised'][0]/1e6)][0]), help="The amount of money raised in the second presale.")
                public_sale_raised = st.number_input('Public Sale Raises / $m', min_value=0.0, value=float([launch_valuation * (public_sale_supply/100) if uploaded_file is None and fundraising_style != 'Custom' else float(sys_param['public_sale_raised'][0]/1e6)][0]), disabled=True, help="The amount of money raised in the public sale.")

                raised_funds = equity_investments + seed_raised + presale_1_raised + presale_2_raised + public_sale_raised
                if fundraising_style == 'Custom' or show_full_fund_table:
                    st.write(f"Total Raised: {raised_funds:.3f} $m")
        
        with col24:
            if fundraising_style == 'Custom' or show_full_fund_table:
                seed_allocation = ((seed_raised) / ((seed_valuation)/initial_supply) / initial_supply) * 1e2
                presale_1_allocation = ((presale_1_raised) / ((presale_1_valuation)/initial_supply) / initial_supply) * 1e2
                presale_2_allocation = ((presale_2_raised) / ((presale_2_valuation)/initial_supply) / initial_supply) * 1e2
                public_sale_allocation = ((public_sale_raised) / ((launch_valuation)/initial_supply) / initial_supply) * 1e2
                st.number_input('Seed Alloc / %', disabled=True, value=seed_allocation, help="The seed round token allocation as percentage of the initial total supply.")
                st.number_input('Presale 1 Alloc / %', disabled=True, value=presale_1_allocation, help="The first presale token allocation as percentage of the initial total supply.")
                st.number_input('Presale 2 Alloc / %', disabled=True, value=presale_2_allocation, help="The second presale token allocation as percentage of the initial total supply.")
                st.number_input('Public Sale Alloc / %', disabled=True, value=public_sale_allocation, help="The public sale token allocation as percentage of the initial total supply.")
        
        if fundraising_style == 'Custom' or show_full_fund_table:
            col21a, col22a, col23a = st.columns(3)
            with col21a:
                bar_plot_plotly_from_variables({'Round': ['Angels', 'Seed', 'Presale 1', 'Presale 2', 'Public Sale'], 'Raised / $': [equity_investments, seed_raised, presale_1_raised, presale_2_raised, public_sale_raised]}, 'Round', 'Raised / $', info_box=None, plot_title='Fundraising Round Raised Capital')
            with col22a:
                bar_plot_plotly_from_variables({'Round': ['Angels', 'Seed', 'Presale 1', 'Presale 2', 'Public Sale'], 'Valuation / $m': [equity_investments / (initial_supply * equity_perc/100), seed_valuation, presale_1_valuation, presale_2_valuation, launch_valuation]}, 'Round', 'Valuation / $m', info_box=None, plot_title='Fundraising Round Token Valuations')
            with col23a:
                bar_plot_plotly_from_variables({'Round': ['Angels', 'Seed', 'Presale 1', 'Presale 2', 'Public Sale'], 'Allocation / %': [equity_perc, seed_allocation, presale_1_allocation, presale_2_allocation, public_sale_allocation]}, 'Round', 'Allocation / %', info_box=None, plot_title='Fundraising Round Token Allocations')


    with st.expander("**Token Allocations & Vesting**"):
        st.markdown("### Token Allocations & Vesting")
        vesting_dict = {} # structure: {name: {'allocation': allocation, 'initial_vesting': initial_vesting, 'cliff': cliff, 'duration': duration}}
        col31, col32 = st.columns(2)
        with col31:
            vesting_style_choices = ['Slow', 'Medium', 'Fast','Custom']
            vesting_style = st.radio('Vesting Style',tuple(vesting_style_choices), index=vesting_style_choices.index(sys_param['vesting_style'][0]) if 'vesting_style' in sys_param else 0, help=param_help['vesting_style'])
            if vesting_style != 'Custom':
                show_full_alloc_table = st.toggle('Show Full Table', value=False, help="Show the full token allocation and vesting table.")
            else:
                show_full_alloc_table = False
        with col32:
            incentivisation_toggle = st.toggle('Incentivisation Vesting', value=sys_param['incentivisation_allocation'][0] > 0.0, help=param_help['incentivisation'])
            staking_vesting_toggle = st.toggle('Staking Vesting', value=sys_param['staking_vesting_allocation'][0] > 0.0, help=param_help['staking_vesting'])
            airdrop_toggle = st.toggle('Airdrops', value=sys_param['airdrop_allocation'][0] > 0.0, help=param_help['airdrops'])

        col41, col42, col43, col44, col45 = st.columns(5)
        with col41:
            if vesting_style == 'Custom' or show_full_alloc_table:
                st.write("Name")
                if equity_perc > 0:
                    st.text_input("Angel","Angel", label_visibility="collapsed", disabled=True, key="angel_name")
                if seed_raised > 0:
                    st.text_input("Seed","Seed", label_visibility="collapsed", disabled=True, key="seed_name")
                if presale_1_raised > 0:
                    st.text_input("Presale 1","Presale 1", label_visibility="collapsed", disabled=True, key="presale_1_name")
                if presale_2_raised > 0:    
                    st.text_input("Presale 2","Presale 2", label_visibility="collapsed", disabled=True, key="presale_2_name")
                if public_sale_raised > 0:    
                    st.text_input("Public Sale","Public Sale", label_visibility="collapsed", disabled=True, key="public_sale_name")
                st.text_input("Team","Team", label_visibility="collapsed", disabled=True, key="team_name")
                st.text_input("Advisors","Advisors", label_visibility="collapsed", disabled=True, key="advisors_name")
                st.text_input("Strategic Partners","Strat. Partners", label_visibility="collapsed", disabled=True, key="partners_name")
                st.text_input("Reserve","Reserve", label_visibility="collapsed", disabled=True, key="reserve_name")
                st.text_input("Community","Community", label_visibility="collapsed", disabled=True, key="community_name")
                st.text_input("Foundation","Foundation", label_visibility="collapsed", disabled=True, key="foundation_name")
                if incentivisation_toggle:
                    st.text_input("Incentivisation","Incentivisation", label_visibility="collapsed", disabled=True, key="incentivisation_name")
                if staking_vesting_toggle:
                    st.text_input("Staking Vesting","Staking Vesting", label_visibility="collapsed", disabled=True, key="staking_vesting_name")
                if airdrop_toggle:
                    st.text_input("Airdrops","Airdrops", label_visibility="hidden", disabled=True, key="airdrops_name")
                    st.write('')
        with col42:
            if vesting_style == 'Custom' or show_full_alloc_table:
                st.write("Allocation / %")
                equity_allocation = (equity_perc/100) * (sys_param['team_allocation'][0]/(1-equity_perc/100))
                if equity_perc > 0:
                    equity_allocation_new = st.number_input('equity_allocation_new', label_visibility="collapsed", min_value=0.0, value=equity_allocation, disabled=True, key="angel_allocation")
                else:
                    equity_allocation_new = 0.0
                if seed_raised > 0:
                    seed_allocation = st.number_input('seed_allocation', label_visibility="collapsed", min_value=0.0, value=((seed_raised) / ((seed_valuation)/initial_supply) / initial_supply) * 1e2, disabled=True, key="seed_allocation")
                else:
                    seed_allocation = 0.0
                if presale_1_raised > 0:
                    presale_1_allocation = st.number_input('presale_1_allocation', label_visibility="collapsed", min_value=0.0, value=((presale_1_raised) / ((presale_1_valuation)/initial_supply) / initial_supply) * 1e2, disabled=True, key="presale_1_allocation")
                else:
                    presale_1_allocation = 0.0
                if presale_2_raised > 0:
                    presale_2_allocation = st.number_input('presale_2_allocation', label_visibility="collapsed", min_value=0.0, value=((presale_2_raised) / ((presale_2_valuation)/initial_supply) / initial_supply) * 1e2, disabled=True, key="presale_2_allocation")   
                else:
                    presale_2_allocation = 0.0
                if public_sale_raised > 0:
                    public_sale_allocation = st.number_input('public_sale_allocation', label_visibility="collapsed", min_value=0.0, value=((public_sale_raised) / ((launch_valuation)/initial_supply) / initial_supply) * 1e2, disabled=True, key="public_sale_allocation")
                else:
                    public_sale_allocation = 0.0
                team_allocation = st.number_input('team_allocation', label_visibility="collapsed", min_value=0.0, value=sys_param['team_allocation'][0], disabled=False, key="team_allocation")
                ov_advisor_allocation = st.number_input('ov_advisor_allocation', label_visibility="collapsed", min_value=0.0, value=sys_param['ov_allocation'][0]+sys_param['advisor_allocation'][0], disabled=False, key="ov_advisor_allocation")
                strategic_partners_allocation = st.number_input('strategic_partners_allocation', label_visibility="collapsed", min_value=0.0, value=sys_param['strategic_partners_allocation'][0], disabled=False, key="partner_allocation")
                reserve_allocation = st.number_input('reserve_allocation', label_visibility="collapsed", min_value=0.0, value=sys_param['reserve_allocation'][0], disabled=False, key="reserve_allocation")
                community_allocation = st.number_input('community_allocation', label_visibility="collapsed", min_value=0.0, value=sys_param['community_allocation'][0], disabled=False, key="community_allocation")
                foundation_allocation = st.number_input('foundation_allocation', label_visibility="collapsed", min_value=0.0, value=sys_param['foundation_allocation'][0], disabled=False, key="foundation_allocation")
                if incentivisation_toggle:
                    incentivisation_allocation = st.number_input('incentivisation_allocation', label_visibility="collapsed", min_value=0.0, value=sys_param['incentivisation_allocation'][0], disabled=False, key="incentivisation_allocation")
                else:
                    incentivisation_allocation = 0.0
                if staking_vesting_toggle:
                    staking_vesting_allocation = st.number_input('staking_vesting_allocation', label_visibility="collapsed", min_value=0.0, value=sys_param['staking_vesting_allocation'][0], disabled=False, key="staking_vesting_allocation")
                else:
                    staking_vesting_allocation = 0.0
                if airdrop_toggle:
                    airdrop_allocation = st.number_input('airdrop_allocation', label_visibility="hidden", min_value=0.0, value=sys_param['airdrop_allocation'][0], disabled=False, key="airdrop_allocation")
                else:
                    airdrop_allocation = 0.0
                lp_allocation = (100 - equity_allocation_new - seed_allocation - presale_1_allocation
                                - presale_2_allocation - public_sale_allocation - team_allocation - ov_advisor_allocation
                                - strategic_partners_allocation - reserve_allocation - community_allocation
                                - foundation_allocation - incentivisation_allocation - staking_vesting_allocation
                                - airdrop_allocation)

            else:
                equity_allocation_new = (equity_perc/100) * (sys_param['team_allocation'][0]/(1-equity_perc/100))
                seed_allocation = ((seed_raised) / ((seed_valuation)/initial_supply) / initial_supply) * 1e2
                presale_1_allocation = ((presale_1_raised) / ((presale_1_valuation)/initial_supply) / initial_supply) * 1e2
                presale_2_allocation = ((presale_2_raised) / ((presale_2_valuation)/initial_supply) / initial_supply) * 1e2
                public_sale_allocation = ((public_sale_raised) / ((launch_valuation)/initial_supply) / initial_supply) * 1e2
                team_allocation = sys_param['team_allocation'][0]
                ov_advisor_allocation = sys_param['ov_allocation'][0]+sys_param['advisor_allocation'][0]
                strategic_partners_allocation = sys_param['strategic_partners_allocation'][0]
                reserve_allocation = sys_param['reserve_allocation'][0]
                community_allocation = sys_param['community_allocation'][0]
                foundation_allocation = sys_param['foundation_allocation'][0]
                incentivisation_allocation = sys_param['incentivisation_allocation'][0]
                staking_vesting_allocation = sys_param['staking_vesting_allocation'][0]
                airdrop_allocation = sys_param['airdrop_allocation'][0]
                airdrop_amount1 = sys_param['airdrop_amount1'][0]
                airdrop_amount2 = sys_param['airdrop_amount2'][0]
                airdrop_amount3 = sys_param['airdrop_amount3'][0]
                airdrop_date1 = datetime.strptime(sys_param['airdrop_date1'][0], "%d.%m.%Y")
                airdrop_date2 = datetime.strptime(sys_param['airdrop_date2'][0], "%d.%m.%Y")
                airdrop_date3 = datetime.strptime(sys_param['airdrop_date3'][0], "%d.%m.%Y")
                lp_allocation = (100 - equity_allocation_new - seed_allocation - presale_1_allocation
                                - presale_2_allocation - public_sale_allocation - team_allocation - ov_advisor_allocation
                                - strategic_partners_allocation - reserve_allocation - community_allocation
                                - foundation_allocation - incentivisation_allocation - staking_vesting_allocation
                                - airdrop_allocation)

                
        with col43:
            if vesting_style == 'Slow':
                init_vesting_dict = {
                    "angel" : 0.0,
                    "seed" : 0.0,
                    "presale_1" : 0.0,
                    "presale_2" : 0.0,
                    "public_sale" : 10.0,
                    "team" : 0.0,
                    "advisor" : 0.0,
                    "strategic_partners" : 0.0,
                    "reserve" : 10.0,
                    "community" : 10.0,
                    "foundation" : 10.0,
                    "incentivisation" : 0.0,
                    "staking_vesting" : 0.0
                }
            if vesting_style == 'Medium':
                init_vesting_dict = {
                    "angel" : 0.0,
                    "seed" : 0.0,
                    "presale_1" : 0.0,
                    "presale_2" : 5.0,
                    "public_sale" : 15.0,
                    "team" : 0.0,
                    "advisor" : 0.0,
                    "strategic_partners" : 0.0,
                    "reserve" : 10.0,
                    "community" : 10.0,
                    "foundation" : 10.0,
                    "incentivisation" : 0.0,
                    "staking_vesting" : 0.0
                }
            if vesting_style == 'Fast':
                init_vesting_dict = {
                    "angel" : 0.0,
                    "seed" : 0.0,
                    "presale_1" : 5.0,
                    "presale_2" : 15.0,
                    "public_sale" : 35.0,
                    "team" : 0.0,
                    "advisor" : 0.0,
                    "strategic_partners" : 0.0,
                    "reserve" : 25.0,
                    "community" : 25.0,
                    "foundation" : 25.0,
                    "incentivisation" : 5.0,
                    "staking_vesting" : 5.0
                }
            if vesting_style == 'Custom' or show_full_alloc_table:
                st.write("Init. Vesting / %")
                if equity_perc > 0:
                    angel_initial_vesting = st.number_input("angel_initial_vesting", label_visibility="collapsed", min_value=0.0, value=[sys_param['angel_initial_vesting'][0] if vesting_style == 'Custom' else init_vesting_dict['angel']][0], key="angel_initial_vesting")
                else:
                    angel_initial_vesting = 0.0
                if seed_raised > 0:
                    seed_initial_vesting = st.number_input("seed_initial_vesting", label_visibility="collapsed", min_value=0.0, value=[sys_param['seed_initial_vesting'][0] if vesting_style == 'Custom' else init_vesting_dict['seed']][0], key="seed_initial_vesting")
                else:
                    seed_initial_vesting = 0.0
                if presale_1_raised > 0:
                    presale_1_initial_vesting = st.number_input("presale_1_initial_vesting", label_visibility="collapsed", min_value=0.0, value=[sys_param['presale_1_initial_vesting'][0] if vesting_style == 'Custom' else init_vesting_dict['presale_1']][0], key="presale_1_initial_vesting")
                else:
                    presale_1_initial_vesting = 0.0
                if presale_2_raised > 0:
                    presale_2_initial_vesting = st.number_input("presale_2_initial_vesting", label_visibility="collapsed", min_value=0.0, value=[sys_param['presale_2_initial_vesting'][0] if vesting_style == 'Custom' else init_vesting_dict['presale_2']][0], key="presale_2_initial_vesting")
                else:
                    presale_2_initial_vesting = 0.0
                if public_sale_raised > 0:
                    public_sale_initial_vesting = st.number_input("public_sale_initial_vesting", label_visibility="collapsed", min_value=0.0, value=[sys_param['public_sale_initial_vesting'][0] if vesting_style == 'Custom' else init_vesting_dict['public_sale']][0], key="public_sale_initial_vesting")
                else:
                    public_sale_initial_vesting = 0.0
                team_initial_vesting = st.number_input("team_initial_vesting", label_visibility="collapsed", min_value=0.0, value=[sys_param['team_initial_vesting'][0] if vesting_style == 'Custom' else init_vesting_dict['team']][0], key="team_initial_vesting")
                advisor_initial_vesting = st.number_input("advisor_initial_vesting", label_visibility="collapsed", min_value=0.0, value=[(sys_param['ov_initial_vesting'][0]+sys_param['advisor_initial_vesting'][0])/2 if vesting_style == 'Custom' else init_vesting_dict['advisor']][0], key="advisor_initial_vesting")
                strategic_partners_initial_vesting = st.number_input("strategic_partners_initial_vesting", label_visibility="collapsed", min_value=0.0, value=[sys_param['strategic_partners_initial_vesting'][0] if vesting_style == 'Custom' else init_vesting_dict['strategic_partners']][0], key="strategic_partners_initial_vesting")
                reserve_initial_vesting = st.number_input("reserve_initial_vesting", label_visibility="collapsed", min_value=0.0, value=[sys_param['reserve_initial_vesting'][0] if vesting_style == 'Custom' else init_vesting_dict['reserve']][0], key="reserve_initial_vesting")
                community_initial_vesting = st.number_input("community_initial_vesting", label_visibility="collapsed", min_value=0.0, value=[sys_param['community_initial_vesting'][0] if vesting_style == 'Custom' else init_vesting_dict['community']][0], key="community_initial_vesting")
                foundation_initial_vesting = st.number_input("foundation_initial_vesting", label_visibility="collapsed", min_value=0.0, value=[sys_param['foundation_initial_vesting'][0] if vesting_style == 'Custom' else init_vesting_dict['foundation']][0], key="foundation_initial_vesting")
                if incentivisation_toggle:
                    incentivisation_initial_vesting = st.number_input("incentivisation_initial_vesting", label_visibility="collapsed", min_value=0.0, value=[sys_param['incentivisation_initial_vesting'][0] if vesting_style == 'Custom' else init_vesting_dict['incentivisation']][0], key="incentivisation_initial_vesting")
                else:
                    incentivisation_initial_vesting = 0.0
                if staking_vesting_toggle:
                    staking_vesting_initial_vesting = st.number_input("staking_vesting_initial_vesting", label_visibility="collapsed", min_value=0.0, value=[sys_param['staking_vesting_initial_vesting'][0] if vesting_style == 'Custom' else init_vesting_dict['staking_vesting']][0], key="staking_vesting_initial_vesting")
                else:
                    staking_vesting_initial_vesting = 0.0
                if airdrop_toggle:
                    airdrop_date1 = st.date_input("Airdrop Date 1", min_value=token_launch_date, value=datetime.strptime(sys_param['airdrop_date1'][0], "%d.%m.%Y"), help="The date of the first airdrop.")
                    airdrop_amount1 = st.number_input("Amount 1 / %", min_value=0.0, value=sys_param['airdrop_amount1'][0], help="The share of tokens distributed from the airdrop allocation in the first airdrop.")

        with col44:
            if vesting_style == 'Slow':
                cliff_dict = {
                    "angel" : 24,
                    "seed" : 18,
                    "presale_1" : 12,
                    "presale_2" : 9,
                    "public_sale" : 3,
                    "team" : 24,
                    "advisor" : 18,
                    "strategic_partners" : 18,
                    "reserve" : 0,
                    "community" : 0,
                    "foundation" : 0,
                    "incentivisation" : 0,
                    "staking_vesting" : 0
                }
            if vesting_style == 'Medium':
                cliff_dict = {
                    "angel" : 18,
                    "seed" : 12,
                    "presale_1" : 9,
                    "presale_2" : 6,
                    "public_sale" : 0,
                    "team" : 18,
                    "advisor" : 12,
                    "strategic_partners" : 12,
                    "reserve" : 0,
                    "community" : 0,
                    "foundation" : 0,
                    "incentivisation" : 0,
                    "staking_vesting" : 0
                }
            if vesting_style == 'Fast':
                cliff_dict = {
                    "angel" : 12,
                    "seed" : 9,
                    "presale_1" : 6,
                    "presale_2" : 3,
                    "public_sale" : 0,
                    "team" : 12,
                    "advisor" : 9,
                    "strategic_partners" : 9,
                    "reserve" : 0,
                    "community" : 0,
                    "foundation" : 0,
                    "incentivisation" : 0,
                    "staking_vesting" : 0
                }
            if vesting_style == 'Custom' or show_full_alloc_table:
                st.write("Cliff / Mon.")
                if equity_perc > 0:
                    angel_cliff = st.number_input("angel_cliff", label_visibility="collapsed", min_value=0, value=int([sys_param['angel_cliff'][0] if vesting_style == 'Custom' else cliff_dict['angel']][0]), key="angel_cliff")
                else:
                    angel_cliff = 0.0
                if seed_raised > 0:
                    seed_cliff = st.number_input("seed_cliff", label_visibility="collapsed", min_value=0, value=int([sys_param['seed_cliff'][0] if vesting_style == 'Custom' else cliff_dict['seed']][0]), key="seed_cliff")
                else:
                    seed_cliff = 0.0
                if presale_1_raised:
                    presale_1_cliff = st.number_input("presale_1_cliff", label_visibility="collapsed", min_value=0, value=int([sys_param['presale_1_cliff'][0] if vesting_style == 'Custom' else cliff_dict['presale_1']][0]), key="presale_1_cliff")
                else:
                    presale_1_cliff = 0.0
                if presale_2_raised > 0:
                    presale_2_cliff = st.number_input("presale_2_cliff", label_visibility="collapsed", min_value=0, value=int([sys_param['presale_2_cliff'][0] if vesting_style == 'Custom' else cliff_dict['presale_2']][0]), key="presale_2_cliff")
                else:
                    presale_2_cliff = 0.0
                if public_sale_raised > 0:
                    public_sale_cliff = st.number_input("public_sale_cliff", label_visibility="collapsed", min_value=0, value=int([sys_param['public_sale_cliff'][0] if vesting_style == 'Custom' else cliff_dict['public_sale']][0]), key="public_sale_cliff")
                else:
                    public_sale_cliff = 0.0
                team_cliff = st.number_input("team_cliff", label_visibility="collapsed", min_value=0, value=int([sys_param['team_cliff'][0] if vesting_style == 'Custom' else cliff_dict['team']][0]), key="team_cliff")
                advisor_cliff = st.number_input("advisor_cliff", label_visibility="collapsed", min_value=0, value=int([sys_param['advisor_cliff'][0] if vesting_style == 'Custom' else cliff_dict['advisor']][0]), key="advisor_cliff")
                strategic_partners_cliff = st.number_input("strategic_partners_cliff", label_visibility="collapsed", min_value=0, value=int([sys_param['strategic_partners_cliff'][0] if vesting_style == 'Custom' else cliff_dict['strategic_partners']][0]), key="strategic_partners_cliff")
                reserve_cliff = st.number_input("reserve_cliff", label_visibility="collapsed", min_value=0, value=int([sys_param['reserve_cliff'][0] if vesting_style == 'Custom' else cliff_dict['reserve']][0]), key="reserve_cliff")
                community_cliff = st.number_input("community_cliff", label_visibility="collapsed", min_value=0, value=int([sys_param['community_cliff'][0] if vesting_style == 'Custom' else cliff_dict['community']][0]), key="community_cliff")
                foundation_cliff = st.number_input("foundation_cliff", label_visibility="collapsed", min_value=0, value=int([sys_param['foundation_cliff'][0] if vesting_style == 'Custom' else cliff_dict['foundation']][0]), key="foundation_cliff")
                if incentivisation_toggle:
                    incentivisation_cliff = st.number_input("incentivisation_cliff", label_visibility="collapsed", min_value=0, value=int([sys_param['incentivisation_cliff'][0] if vesting_style == 'Custom' else cliff_dict['incentivisation']][0]), key="incentivisation_cliff")
                else:
                    incentivisation_cliff = 0.0
                if staking_vesting_toggle:
                    staking_vesting_cliff = st.number_input("staking_vesting_cliff", label_visibility="collapsed", min_value=0, value=int([sys_param['staking_vesting_cliff'][0] if vesting_style == 'Custom' else cliff_dict['staking_vesting']][0]), key="staking_vesting_cliff")
                else:
                    staking_vesting_cliff = 0.0
                if airdrop_toggle:
                    airdrop_date2 = st.date_input("Airdrop Date 2", min_value=token_launch_date, value=datetime.strptime(sys_param['airdrop_date2'][0], "%d.%m.%Y"), help="The date of the second airdrop.")
                    airdrop_amount2 = st.number_input("Amount 2 / %", min_value=0.0, value=sys_param['airdrop_amount2'][0], help="The share of tokens distributed from the airdrop allocation in the second airdrop.")
    
        with col45:
            if vesting_style == 'Slow':
                duration_dict = {
                    "angel" : 72,
                    "seed" : 48,
                    "presale_1" : 36,
                    "presale_2" : 24,
                    "public_sale" : 12,
                    "team" : 72,
                    "advisor" : 48,
                    "strategic_partners" : 48,
                    "reserve" : 72,
                    "community" : 72,
                    "foundation" : 72,
                    "incentivisation" : 72,
                    "staking_vesting" : 72
                }
            if vesting_style == 'Medium':
                duration_dict = {
                    "angel" : 48,
                    "seed" : 36,
                    "presale_1" : 24,
                    "presale_2" : 12,
                    "public_sale" : 6,
                    "team" : 48,
                    "advisor" : 36,
                    "strategic_partners" : 36,
                    "reserve" : 48,
                    "community" : 48,
                    "foundation" : 48,
                    "incentivisation" : 48,
                    "staking_vesting" : 48
                }
            if vesting_style == 'Fast':
                duration_dict = {
                    "angel" : 36,
                    "seed" : 24,
                    "presale_1" : 12,
                    "presale_2" : 6,
                    "public_sale" : 3,
                    "team" : 36,
                    "advisor" : 24,
                    "strategic_partners" : 24,
                    "reserve" : 24,
                    "community" : 24,
                    "foundation" : 24,
                    "incentivisation" : 24,
                    "staking_vesting" : 24
                }
            if vesting_style == 'Custom' or show_full_alloc_table:
                st.write("Duration / Mon.")
                if equity_perc > 0:
                    angel_duration = st.number_input("angel_duration", label_visibility="collapsed", min_value=0, value=int([sys_param['angel_vesting_duration'][0] if vesting_style == 'Custom' else duration_dict['angel']][0]), key="angel_vesting_duration")
                else:
                    angel_duration = 0.0
                if seed_raised > 0:
                    seed_duration = st.number_input("seed_duration", label_visibility="collapsed", min_value=0, value=int([sys_param['seed_vesting_duration'][0] if vesting_style == 'Custom' else duration_dict['seed']][0]), key="seed_vesting_duration")
                else:
                    seed_duration = 0.0
                if presale_1_raised > 0:
                    presale_1_duration = st.number_input("presale_1_duration", label_visibility="collapsed", min_value=0, value=int([sys_param['presale_1_vesting_duration'][0] if vesting_style == 'Custom' else duration_dict['presale_1']][0]), key="presale_1_vesting_duration")
                else:
                    presale_1_duration = 0.0
                if presale_2_raised > 0:
                    presale_2_duration = st.number_input("presale_2_duration", label_visibility="collapsed", min_value=0, value=int([sys_param['presale_2_vesting_duration'][0] if vesting_style == 'Custom' else duration_dict['presale_2']][0]), key="presale_2_vesting_duration")
                else:
                    presale_2_duration = 0.0
                if public_sale_raised > 0:
                    public_sale_duration = st.number_input("public_sale_duration", label_visibility="collapsed", min_value=0, value=int([sys_param['public_sale_vesting_duration'][0] if vesting_style == 'Custom' else duration_dict['public_sale']][0]), key="public_sale_vesting_duration")
                else:
                    public_sale_duration = 0.0
                team_duration = st.number_input("team_duration", label_visibility="collapsed", min_value=0, value=int([sys_param['team_vesting_duration'][0] if vesting_style == 'Custom' else duration_dict['team']][0]), key="team_vesting_duration")
                advisor_duration = st.number_input("advisor_duration", label_visibility="collapsed", min_value=0, value=int([(sys_param['advisor_vesting_duration'][0] + sys_param['ov_vesting_duration'][0])/2 if vesting_style == 'Custom' else duration_dict['advisor']][0]), key="advisor_vesting_duration")
                strategic_partners_duration = st.number_input("strategic_partners_duration", label_visibility="collapsed", min_value=0, value=int([sys_param['strategic_partner_vesting_duration'][0] if vesting_style == 'Custom' else duration_dict['strategic_partners']][0]), key="strategic_partners_vesting_duration")
                reserve_duration = st.number_input("reserve_duration", label_visibility="collapsed", min_value=0, value=int([sys_param['reserve_vesting_duration'][0] if vesting_style == 'Custom' else duration_dict['reserve']][0]), key="reserve_vesting_duration")
                community_duration = st.number_input("community_duration", label_visibility="collapsed", min_value=0, value=int([sys_param['community_vesting_duration'][0] if vesting_style == 'Custom' else duration_dict['community']][0]), key="community_vesting_duration")
                foundation_duration = st.number_input("foundation_duration", label_visibility="collapsed", min_value=0, value=int([sys_param['foundation_vesting_duration'][0] if vesting_style == 'Custom' else duration_dict['foundation']][0]), key="foundation_vesting_duration")
                if incentivisation_toggle:
                    incentivisation_duration = st.number_input("incentivisation_duration", label_visibility="collapsed", min_value=0, value=int([sys_param['incentivisation_vesting_duration'][0] if vesting_style == 'Custom' else duration_dict['incentivisation']][0]), key="incentivisation_vesting_duration")
                else:
                    incentivisation_duration = 0.0
                if staking_vesting_toggle:
                    staking_vesting_duration = st.number_input("staking_vesting_duration", label_visibility="collapsed", min_value=0, value=int([sys_param['staking_vesting_vesting_duration'][0] if vesting_style == 'Custom' else duration_dict['staking_vesting']][0]), key="staking_vesting_vesting_duration")
                else:
                    staking_vesting_duration = 0.0
                if airdrop_toggle:
                    airdrop_date3 = st.date_input("Airdrop Date 3", min_value=token_launch_date, value=datetime.strptime(sys_param['airdrop_date3'][0], "%d.%m.%Y"), help="The date of the third airdrop.")
                    airdrop_amount3 = st.number_input("Amount 3 / %", min_value=0.0, value=sys_param['airdrop_amount3'][0], help="The share of tokens distributed from the airdrop allocation in the third airdrop.")

        if token_launch:
            if show_full_alloc_table or vesting_style == 'Custom':
                col51, col52, col53 = st.columns(3)
                with col51:
                    st.text_input("DEX LP","DEX Liquidity Pool", label_visibility="hidden", disabled=True, key="lp_name")
                with col52:
                    st.number_input('LP Token Allocation / %', label_visibility="visible", value=lp_allocation, disabled=True, key="lp_allocation", help="The percentage of tokens allocated to the liquidity pool. This is the remaining percentage of tokens after all other allocations have been made. It must not be < 0 and determines the required capital to seed the liquidity.")
                with col53:
                    dex_capital = st.number_input('DEX Capital / $m', value=float((lp_allocation/100 )* initial_supply * launch_valuation / initial_supply), disabled=True, key="liquidity_capital_requirements", help="The required capital to seed the liquidity: lp_allocation x total_initial_supply / 100 % * token_launch_price.")
            else:
                dex_capital = (lp_allocation/100 )* initial_supply * launch_valuation / initial_supply
            if dex_capital > raised_funds:
                st.error(f"The required capital ({round(dex_capital,2)}m) to seed the liquidity is higher than the raised funds (${round(raised_funds,2)}m). Please reduce the LP Token Allocation or the Launch Valuation!", icon="⚠️")
            if lp_allocation < 0:
                st.error(f"The LP token allocation ({round(lp_allocation,2)}%) is negative. Please increase the token launch valuation or reduce stakeholder allocations!", icon="⚠️")
        
        airdrop_date1 = datetime(airdrop_date1.year, airdrop_date1.month, airdrop_date1.day)
        airdrop_date2 = datetime(airdrop_date2.year, airdrop_date2.month, airdrop_date2.day)
        airdrop_date3 = datetime(airdrop_date3.year, airdrop_date3.month, airdrop_date3.day)

        if airdrop_toggle:
            if airdrop_date1 < token_launch_date:
                st.error(f"The first airdrop date ({airdrop_date1.strftime('%d.%m.%Y')}) is before the launch date ({token_launch_date}). Please adjust the airdrop date!", icon="⚠️")
            if airdrop_date2 < token_launch_date:
                st.error(f"The second airdrop date ({airdrop_date2.strftime('%d.%m.%Y')}) is before the launch date ({token_launch_date}). Please adjust the airdrop date!", icon="⚠️")
            if airdrop_date3 < token_launch_date:
                st.error(f"The third airdrop date ({airdrop_date3.strftime('%d.%m.%Y')}) is before the launch date ({token_launch_date}). Please adjust the airdrop date!", icon="⚠️")
        
                
        airdrop_dict = {
            'ad1': {
                'date': [airdrop_date1.strftime('%d.%m.%Y') if airdrop_toggle else sys_param['airdrop_date1'][0]][0],
                'amount': [airdrop_amount1 if airdrop_toggle else sys_param['airdrop_amount1'][0]][0]
            },
            'ad2': {
                'date': [airdrop_date2.strftime('%d.%m.%Y') if airdrop_toggle else sys_param['airdrop_date2'][0]][0],
                'amount': [airdrop_amount2 if airdrop_toggle else sys_param['airdrop_amount2'][0]][0]
            },
            'ad3': {
                'date': [airdrop_date3.strftime('%d.%m.%Y') if airdrop_toggle else sys_param['airdrop_date3'][0]][0],
                'amount': [airdrop_amount3 if airdrop_toggle else sys_param['airdrop_amount3'][0]][0]
            }}

        # fill vesting_dict
        vesting_dict = {
            "angel" : {
                "allocation" : equity_allocation_new,
                "initial_vesting" : [angel_initial_vesting if vesting_style == 'Custom' or show_full_alloc_table else init_vesting_dict['angel']][0],
                "cliff" : [angel_cliff if vesting_style == 'Custom' or show_full_alloc_table else cliff_dict['angel']][0],
                "duration" : [angel_duration if vesting_style == 'Custom' or show_full_alloc_table else duration_dict['angel']][0]
            },
            "seed" : {
                "allocation" : seed_allocation,
                "initial_vesting" : [seed_initial_vesting if vesting_style == 'Custom' or show_full_alloc_table else init_vesting_dict['seed']][0],
                "cliff" : [seed_cliff if vesting_style == 'Custom' or show_full_alloc_table else cliff_dict['seed']][0],
                "duration" : [seed_duration if vesting_style == 'Custom' or show_full_alloc_table else duration_dict['seed']][0]
            },
            "presale_1" : {
                "allocation" : presale_1_allocation,
                "initial_vesting" : [presale_1_initial_vesting if vesting_style == 'Custom' or show_full_alloc_table else init_vesting_dict['presale_1']][0],
                "cliff" : [presale_1_cliff if vesting_style == 'Custom' or show_full_alloc_table else cliff_dict['presale_1']][0],
                "duration" : [presale_1_duration if vesting_style == 'Custom' or show_full_alloc_table else duration_dict['presale_1']][0]
            },
            "presale_2" : {
                "allocation" : presale_2_allocation,
                "initial_vesting" : [presale_2_initial_vesting if vesting_style == 'Custom' or show_full_alloc_table else init_vesting_dict['presale_2']][0],
                "cliff" : [presale_2_cliff if vesting_style == 'Custom' or show_full_alloc_table else cliff_dict['presale_2']][0],
                "duration" : [presale_2_duration if vesting_style == 'Custom' or show_full_alloc_table else duration_dict['presale_2']][0]
            },
            "public_sale" : {
                "allocation" : public_sale_allocation,
                "initial_vesting" : [public_sale_initial_vesting if vesting_style == 'Custom' or show_full_alloc_table else init_vesting_dict['public_sale']][0],
                "cliff" : [public_sale_cliff if vesting_style == 'Custom' or show_full_alloc_table else cliff_dict['public_sale']][0],
                "duration" : [public_sale_duration if vesting_style == 'Custom' or show_full_alloc_table else duration_dict['public_sale']][0]
            },
            "team" : {
                "allocation" : team_allocation,
                "initial_vesting" : [team_initial_vesting if vesting_style == 'Custom' or show_full_alloc_table else init_vesting_dict['team']][0],
                "cliff" : [team_cliff if vesting_style == 'Custom' or show_full_alloc_table else cliff_dict['team']][0],
                "duration" : [team_duration if vesting_style == 'Custom' or show_full_alloc_table else duration_dict['team']][0]
            },
            "advisor" : {
                "allocation" : ov_advisor_allocation,
                "initial_vesting" : [advisor_initial_vesting if vesting_style == 'Custom' or show_full_alloc_table else init_vesting_dict['advisor']][0],
                "cliff" : [advisor_cliff if vesting_style == 'Custom' or show_full_alloc_table else cliff_dict['advisor']][0],
                "duration" : [advisor_duration if vesting_style == 'Custom' or show_full_alloc_table else duration_dict['advisor']][0]
            },
            "strategic_partners" : {
                "allocation" : strategic_partners_allocation,
                "initial_vesting" : [strategic_partners_initial_vesting if vesting_style == 'Custom' or show_full_alloc_table else init_vesting_dict['strategic_partners']][0],
                "cliff" : [strategic_partners_cliff if vesting_style == 'Custom' or show_full_alloc_table else cliff_dict['strategic_partners']][0],
                "duration" : [strategic_partners_duration if vesting_style == 'Custom' or show_full_alloc_table else duration_dict['strategic_partners']][0]
            },
            "reserve" : {
                "allocation" : reserve_allocation,
                "initial_vesting" : [reserve_initial_vesting if vesting_style == 'Custom' or show_full_alloc_table else init_vesting_dict['reserve']][0],
                "cliff" : [reserve_cliff if vesting_style == 'Custom' or show_full_alloc_table else cliff_dict['reserve']][0],
                "duration" : [reserve_duration if vesting_style == 'Custom' or show_full_alloc_table else duration_dict['reserve']][0]
            },
            "community" : {
                "allocation" : community_allocation,
                "initial_vesting" : [community_initial_vesting if vesting_style == 'Custom' or show_full_alloc_table else init_vesting_dict['community']][0],
                "cliff" : [community_cliff if vesting_style == 'Custom' or show_full_alloc_table else cliff_dict['community']][0],
                "duration" : [community_duration if vesting_style == 'Custom' or show_full_alloc_table else duration_dict['community']][0]
            },
            "foundation" : {
                "allocation" : foundation_allocation,
                "initial_vesting" : [foundation_initial_vesting if vesting_style == 'Custom' or show_full_alloc_table else init_vesting_dict['foundation']][0],
                "cliff" : [foundation_cliff if vesting_style == 'Custom' or show_full_alloc_table else cliff_dict['foundation']][0],
                "duration" : [foundation_duration if vesting_style == 'Custom' or show_full_alloc_table else duration_dict['foundation']][0]
            },
            "incentivisation" : {
                "allocation" : incentivisation_allocation,
                "initial_vesting" : [incentivisation_initial_vesting if vesting_style == 'Custom' or show_full_alloc_table else init_vesting_dict['incentivisation']][0],
                "cliff" : [incentivisation_cliff if vesting_style == 'Custom' or show_full_alloc_table else cliff_dict['incentivisation']][0],
                "duration" : [incentivisation_duration if vesting_style == 'Custom' or show_full_alloc_table else duration_dict['incentivisation']][0]
            },
            "staking_vesting" : {
                "allocation" : staking_vesting_allocation,
                "initial_vesting" : [staking_vesting_initial_vesting if vesting_style == 'Custom' or show_full_alloc_table else init_vesting_dict['staking_vesting']][0],
                "cliff" : [staking_vesting_cliff if vesting_style == 'Custom' or show_full_alloc_table else cliff_dict['staking_vesting']][0],
                "duration" : [staking_vesting_duration if vesting_style == 'Custom' or show_full_alloc_table else duration_dict['staking_vesting']][0]
            }            
        }

    with st.expander("**User Adoption**"):
        st.markdown("### User Adoption")
        # adoption style choice | user numbers | revenues | meta bucket allocations
        col61, col62, col63 = st.columns(3)
        with col61:
            adoption_style_choices = ['Weak', 'Medium', 'Strong', 'Custom']
            adoption_style = st.radio('Adoption Assumption',tuple(adoption_style_choices), index=adoption_style_choices.index(sys_param['adoption_style'][0]) if 'adoption_style' in sys_param else 0, help='The adoption style determines the scaling velocity for the product revenue and token demand. Moreover it influences the average agent sentiment in terms of selling and utility adoption behavior.')
            show_full_adoption_table = st.toggle('Show Full Table', value=False, help="Show the full adoption parameter set.")
        with col62:
            product_token_ratio = st.slider('Product / Token Weight', min_value=-1.0, max_value=1.0, step=0.1, value=(-float(sys_param['initial_product_users'][0]) + float(sys_param['initial_token_holders'][0])), format="%.2f", help="The weight of product users to token holders. -1 means there are no product users, but only token holders. 1 means the opposite and 0 means that there are as many product users as token holders.")
            initial_users = st.number_input('Initial Users', label_visibility="visible", min_value=0, value=int(sys_param['initial_product_users'][0]) + int(sys_param['initial_token_holders'][0]), disabled=False, key="initial_users", help="Initial amount of users to be divided between product users and token holders according to the Product / Token Weight.")
            initial_product_users = initial_users * (1 - (product_token_ratio)) / 2
            initial_token_holders = initial_users - initial_product_users

        with col63:
            st.write(f"Initial Token Holders: {int(np.ceil(initial_token_holders)):+,}")
            st.write(f"Initial Product Users: {int(np.ceil(initial_product_users)):+,}")

        adoption_dict = {
            "Weak" : {
                "avg_product_user_growth_rate" : 2.0,
                "avg_token_holder_growth_rate" : 2.0,
                "product_adoption_velocity" : 0.5,
                "token_adoption_velocity" : 0.5,
                "one_time_product_revenue_per_user" : 0.0,
                "regular_product_revenue_per_user" : 8.0,
                "one_time_token_buy_per_user" : 0.0,
                "regular_token_buy_per_user" : 8.0,
                "avg_token_utility_allocation" : 20.0,
                "avg_token_selling_allocation" : 70.0,
                "avg_token_holding_allocation" : 10.0,
                "avg_token_utility_removal" : 10.0,

            },
            "Medium" : {
                "avg_product_user_growth_rate" : 4.0,
                "avg_token_holder_growth_rate" : 4.0,
                "product_adoption_velocity" : 1.5,
                "token_adoption_velocity" : 1.5,
                "one_time_product_revenue_per_user" : 0.0,
                "regular_product_revenue_per_user" : 10.0,
                "one_time_token_buy_per_user" : 0.0,
                "regular_token_buy_per_user" : 18.0,
                "avg_token_utility_allocation" : 60.0,
                "avg_token_selling_allocation" : 30.0,
                "avg_token_holding_allocation" : 10.0,
                "avg_token_utility_removal" : 6.0,

            },
            "Strong" : {
                "avg_product_user_growth_rate" : 5.0,
                "avg_token_holder_growth_rate" : 5.0,
                "product_adoption_velocity" : 2.5,
                "token_adoption_velocity" : 2.5,
                "one_time_product_revenue_per_user" : 0.0,
                "regular_product_revenue_per_user" : 12.5,
                "one_time_token_buy_per_user" : 0.0,
                "regular_token_buy_per_user" : 25.0,
                "avg_token_utility_allocation" : 75.0,
                "avg_token_selling_allocation" : 20.0,
                "avg_token_holding_allocation" : 5.0,
                "avg_token_utility_removal" : 3.0,
            }
        }

        if adoption_style == 'Custom' or show_full_adoption_table:
            col71, col72 = st.columns(2)
            with col71:
                avg_product_user_growth_rate = st.number_input('Avg. Product Users Growth Rate / %', label_visibility="visible", min_value=0.0, value=[((float(sys_param['product_users_after_10y'][0]) / float(sys_param['initial_product_users'][0]))**(1/120.0)-1)*100 if adoption_style == 'Custom' else adoption_dict[adoption_style]['avg_product_user_growth_rate']][0], disabled=False, key="product_users_growth_rate", help="The average monthly growth rate of product users.")
                product_users_after_10y = initial_product_users * (1 + avg_product_user_growth_rate/100)**120
                st.write(f"Projected Product Users (10y): {int(np.ceil(product_users_after_10y)):+,}")
                product_adoption_velocity = st.number_input('Product Adoption Velocity', label_visibility="visible", min_value=0.1, value=[float(sys_param['product_adoption_velocity'][0]) if adoption_style == 'Custom' else adoption_dict[adoption_style]['product_adoption_velocity']][0], disabled=False, key="product_adoption_velocity", help="The velocity of product adoption. The higher the velocity, the faster the product adoption in the early years towards market saturation.")
                regular_product_revenue_per_user = st.number_input('Regular Product Revenue / $', label_visibility="visible", min_value=0.0, value=[float(sys_param['regular_product_revenue_per_user'][0]) if adoption_style == 'Custom' else adoption_dict[adoption_style]['regular_product_revenue_per_user']][0], disabled=False, key="regular_product_revenue_per_user", help="The average regular monthly product revenue per user. This will accrue directly to the business funds.")
            with col72:
                avg_token_holder_growth_rate = st.number_input('Avg. Token Holder Growth Rate / %', label_visibility="visible", min_value=0.0, value=[((float(sys_param['token_holders_after_10y'][0]) / float(sys_param['initial_token_holders'][0]))**(1/120.0)-1)*100 if adoption_style == 'Custom' else adoption_dict[adoption_style]['avg_token_holder_growth_rate']][0], disabled=False, key="avg_token_holder_growth_rate", help="The average monthly growth rate of token holders.")
                token_holders_after_10y = initial_token_holders * (1 + avg_token_holder_growth_rate/100)**120
                st.write(f"Projected Token Holders (10y): {int(np.ceil(token_holders_after_10y)):+,}")
                token_adoption_velocity = st.number_input('Token Adoption Velocity', label_visibility="visible", min_value=0.1, value=[float(sys_param['token_adoption_velocity'][0]) if adoption_style == 'Custom' else adoption_dict[adoption_style]['token_adoption_velocity']][0], disabled=False, key="token_adoption_velocity", help="The velocity of token adoption. The higher the velocity, the faster the token adoption in the early years towards market saturation.")
                regular_token_buy_per_user = st.number_input('Regular Token Buy / $', label_visibility="visible", min_value=0.0, value=[float(sys_param['regular_token_buy_per_user'][0]) if adoption_style == 'Custom' else adoption_dict[adoption_style]['regular_token_buy_per_user']][0], disabled=False, key="regular_token_buy_per_user", help="The average regular monthly token buy per token holder. This will accrue directly to the token via buys from the DEX liquidity pool.")
        else:
            avg_product_user_growth_rate = adoption_dict[adoption_style]['avg_product_user_growth_rate']
            product_users_after_10y = initial_product_users * (1 + avg_product_user_growth_rate/100)**120
            avg_token_holder_growth_rate = adoption_dict[adoption_style]['avg_token_holder_growth_rate']
            token_holders_after_10y = initial_token_holders * (1 + avg_token_holder_growth_rate/100)**120

    with st.expander("**Agent Behavior**"):
        st.markdown("### Agent Behavior")
        agent_behavior_choices = ['Static', 'Random']
        agent_behavior = st.radio('Agent Meta Bucket Behavior',tuple(agent_behavior_choices), index=agent_behavior_choices.index(sys_param['agent_behavior'][0].capitalize()), help="Pick the agent behavior model. **Static**:  Every agent will use tokens for selling, utility, and holding always at the same rate throughout the whole simulation. **Random**: The agent behavior is completely random for every agent and timestep.").lower()
        col73, col74, col75 = st.columns(3)
        if agent_behavior == 'static':
            st.write("**Meta Bucket Allocations**")
            col7a, col7b, col7c, col7d = st.columns(4)
            with col7a:
                avg_token_selling_allocation = st.number_input('Avg. Token Selling Alloc. / %', label_visibility="visible", min_value=0.0, max_value=100.0, value=[float(sys_param['avg_token_selling_allocation'][0])*100 if adoption_style == 'Custom' else adoption_dict[adoption_style]['avg_token_selling_allocation']][0], disabled=False, key="avg_token_selling_allocation", help="The average monthly token allocation for selling purposes from all holding supply.")
            with col7b:
                avg_token_holding_allocation = st.number_input('Avg. Token Holding Alloc. / %', label_visibility="visible", min_value=0.0, max_value=100.0, value=[float(sys_param['avg_token_holding_allocation'][0])*100 if adoption_style == 'Custom' else adoption_dict[adoption_style]['avg_token_holding_allocation']][0], disabled=False, key="avg_token_holding_allocation", help="The average monthly token allocation for holding purposes from all holding supply.")
            with col7c:
                avg_token_utility_allocation = st.number_input('Avg. Token Utility Alloc. / %', label_visibility="visible", min_value=0.0, max_value=100.0, value=[float(sys_param['avg_token_utility_allocation'][0])*100 if adoption_style == 'Custom' else adoption_dict[adoption_style]['avg_token_utility_allocation']][0], disabled=False, key="avg_token_utility_allocation", help="The average monthly token allocation for utility purposes from all holding supply.")
            with col7d:
                avg_token_utility_removal = st.number_input('Avg. Token Utility Removal / %', label_visibility="visible", min_value=0.0, max_value=100.0, value=[float(sys_param['avg_token_utility_removal'][0])*100 if adoption_style == 'Custom' else adoption_dict[adoption_style]['avg_token_utility_removal']][0], disabled=False, key="avg_token_utility_removal", help="The average monthly token removal from staking and liquidity mining utilities.")
        elif agent_behavior == 'random':
            with col73:
                random_seed = st.number_input("Random Seed", label_visibility="visible", min_value=float(0.0), value=float(sys_param['random_seed'][0]) if 'random_seed' in sys_param else 1111.11, disabled=False, key="random_seed", help="The random seed for the random agent behavior. This will be used to reproduce the same random agent behavior.")
        avg_token_utility_allocation = avg_token_utility_allocation if (adoption_style == 'Custom' or show_full_adoption_table) and agent_behavior =='static' else adoption_dict[adoption_style]['avg_token_utility_allocation'] if agent_behavior =='static' else 60.0
        avg_token_selling_allocation = avg_token_selling_allocation if (adoption_style == 'Custom' or show_full_adoption_table) and agent_behavior =='static' else adoption_dict[adoption_style]['avg_token_selling_allocation'] if agent_behavior =='static' else 30.0
        avg_token_holding_allocation = avg_token_holding_allocation if (adoption_style == 'Custom' or show_full_adoption_table) and agent_behavior =='static' else adoption_dict[adoption_style]['avg_token_holding_allocation'] if agent_behavior =='static' else 10.0
        meta_bucket_alloc_sum = avg_token_utility_allocation + avg_token_selling_allocation + avg_token_holding_allocation
        if meta_bucket_alloc_sum != 100 and agent_behavior == 'static':
            st.error(f"The sum of the average token allocations for utility, selling and holding ({avg_token_utility_allocation + avg_token_selling_allocation + avg_token_holding_allocation}%) is not equal to 100%. Please adjust the values!", icon="⚠️")


    with st.expander("**Business Assumptions**"):
        st.markdown("### Business Assumptions")
        # income | expenditures | buybacks | burns
        st.write("**Financial Streams**")
        col81, col82, col83 = st.columns(3)
        with col81:
            show_full_business_table = st.toggle('Use Full Custom Table', value=False, help="Show the full financial stream parameter set. Note that all income streams from the table will be added on top of the adoption product revenue.")
            if not show_full_business_table:
                income = st.number_input('Additional income per month / $k', label_visibility="visible", min_value=0.0, value=float(sys_param['royalty_income_per_month'][0] + sys_param['other_income_per_month'][0] + sys_param['treasury_income_per_month'][0])/1e3, disabled=False, key="income", help="The monthly income for the business on top of the product revenue, defined in the user adoption section.")
                expenditures = st.number_input('Expenditures per month / $k', label_visibility="visible", min_value=0.0, value=float(sys_param['salaries_per_month'][0] + sys_param['license_costs_per_month'][0] + sys_param['other_monthly_costs'][0] + (sys_param['one_time_payments_1'][0]+ sys_param['one_time_payments_2'][0])/120)/1e3, disabled=False, key="expenditures", help="The monthly expenditures for the business.")
        if show_full_business_table:
            with col82:
                st.write("**Income**")
                royalty_income_per_month = st.number_input('Royalty income per month / $k', label_visibility="visible", min_value=0.0, value=[float(sys_param['royalty_income_per_month'][0])/1e3 if show_full_business_table else 0.0][0], disabled=False, key="royalty_income_per_month", help="The monthly royalty income for the business.")
                treasury_income_per_month = st.number_input('Treasury income per month / $k', label_visibility="visible", min_value=0.0, value=[float(sys_param['treasury_income_per_month'][0])/1e3 if show_full_business_table else 0.0][0], disabled=False, key="treasury_income_per_month", help="The monthly income for the business from treasury investments yields.")
                other_income_per_month = st.number_input('Other income per month / $k', label_visibility="visible", min_value=0.0, value=[float(sys_param['other_income_per_month'][0])/1e3 if show_full_business_table else 0.0][0], disabled=False, key="other_income_per_month", help="The monthly income for the business from other sources.")
            with col83:
                st.write("**Expenditures**")
                one_time_payments_1 = st.number_input('One-time payments / $k', label_visibility="visible", min_value=0.0, value=[float(sys_param['one_time_payments_1'][0] + sys_param['one_time_payments_2'][0])/1e3 if show_full_business_table else 0.0][0], disabled=False, key="one_time_payments_1", help="The one-time payments for the business at launch (e.g. any back payment of liabilities or treasury investments).")
                salaries_per_month = st.number_input('Salaries per month / $k', label_visibility="visible", min_value=0.0, value=[float(sys_param['salaries_per_month'][0])/1e3 if show_full_business_table else 0.0][0], disabled=False, key="salaries_per_month", help="The monthly salaries paid by the business.")
                license_costs_per_month = st.number_input('License costs per month / $k', label_visibility="visible", min_value=0.0, value=[float(sys_param['license_costs_per_month'][0])/1e3 if show_full_business_table else 0.0][0], disabled=False, key="license_costs_per_month", help="The monthly license costs paid by the business.")
                other_monthly_costs = st.number_input('Other monthly costs / $k', label_visibility="visible", min_value=0.0, value=[float(sys_param['other_monthly_costs'][0])/1e3 if show_full_business_table else 0.0][0], disabled=False, key="other_monthly_costs", help="The monthly costs paid by the business for other purposes.")
        else:
            royalty_income_per_month = [float(sys_param['royalty_income_per_month'][0])/1e3 if income == 0.0 else 0.0][0]
            treasury_income_per_month = [float(sys_param['treasury_income_per_month'][0])/1e3 if income == 0.0 else 0.0][0]
            other_income_per_month = [float(sys_param['other_income_per_month'][0])/1e3 if income == 0.0 else income][0]
            one_time_payments_1 = [float(sys_param['one_time_payments_1'][0] + sys_param['one_time_payments_2'][0])/1e3 if expenditures == 0.0 else 0.0][0]
            salaries_per_month = [float(sys_param['salaries_per_month'][0])/1e3 if expenditures == 0.0 else 0.0][0]
            license_costs_per_month = [float(sys_param['license_costs_per_month'][0])/1e3 if expenditures == 0.0 else 0.0][0]
            other_monthly_costs = [float(sys_param['other_monthly_costs'][0])/1e3 if expenditures == 0.0 else expenditures][0]
        
        if not token_launch:
            months_since_launch = np.abs(int(months_difference(token_launch_date, datetime.today())))
            projected_cash_balance = raised_funds*1e3 - one_time_payments_1 + (royalty_income_per_month + treasury_income_per_month + other_income_per_month - salaries_per_month - license_costs_per_month - other_monthly_costs) * months_since_launch
            initial_cash_balance = st.number_input('Financial Reserves / $k', label_visibility="visible", min_value=0.0, value=float(sys_param['initial_cash_balance'][0])/1e3 if 'initial_cash_balance' in sys_param else projected_cash_balance if projected_cash_balance > 0 else 0.0, format="%.5f", disabled=False, key="initial_cash_balance", help="The financial reserves of the business today. The financial reserves determine the runway of the business.")
            if initial_cash_balance == 0 and (royalty_income_per_month + treasury_income_per_month + other_income_per_month + initial_product_users * regular_product_revenue_per_user - salaries_per_month - license_costs_per_month - other_monthly_costs) < 0:
                st.error(f"The financial reserves are 0 and the monthly expenditures are greater than the revenues. Increase the initial cash reserves to achieve a proper financial runway!", icon="⚠️")
        else:
            initial_cash_balance = 0.0


        st.write("**Buybacks and Burns**")
        col91, col92 = st.columns(2)
        with col91:
            enable_protocol_buybacks = st.toggle('Enable Protocol Token Buybacks', value=float(sys_param['buyback_perc_per_month'][0]) > 0 or float(sys_param['buyback_fixed_per_month'][0]) > 0, help=" Enable the buyback of tokens to refill a protocol bucket.")
            if enable_protocol_buybacks:
                buyback_type = st.radio('Buyback Type',('Fixed', 'Percentage'), index=0, help='The buyback type determines the buyback behavior of the business. A fixed buyback means that the business buys back a fixed USD worth amount of tokens per month. A percentage buyback means that the business buys back a percentage USD worth amount of tokens per month, depending on the business funds.')
                if buyback_type == 'Fixed':
                    buyback_fixed_per_month = st.number_input('Buyback per month / $k', label_visibility="visible", min_value=0.0, value=[float(sys_param['buyback_fixed_per_month'][0])/1e3 if enable_protocol_buybacks else 0.0][0], disabled=False, key="buyback_fixed_per_month", help="The fixed USD worth amount of tokens bought back by the business per month.")
                    buyback_perc_per_month = 0.0
                elif buyback_type == 'Percentage':
                    buyback_perc_per_month = st.number_input('Buyback per month / %', label_visibility="visible", min_value=0.0, value=[float(sys_param['buyback_perc_per_month'][0]) if enable_protocol_buybacks else 0.0][0], disabled=False, key="buyback_perc_per_month", help="The USD worth of tokens bought back by the business per month as percentage of the current business funds.")
                    buyback_fixed_per_month = 0.0
                
                buyback_buckets = ['Reserve', 'Community', 'Foundation', 'Incentivisation', 'Staking Vesting']
                if not incentivisation_toggle:
                    buyback_buckets.pop(buyback_buckets.index('Incentivisation'))
                if not staking_vesting_toggle:
                    buyback_buckets.pop(buyback_buckets.index('Staking Vesting'))
                buyback_bucket = st.radio('Buyback Bucket',tuple(buyback_buckets), index=0, help='The buyback bucket determines the destination of the bought back tokens.')
                buyback_start = st.date_input("Buybacks Start", min_value=token_launch_date, value=datetime.strptime(sys_param['buyback_start'][0], "%d.%m.%Y"), help="The date when monthly buybacks should start.")
                buyback_end = st.date_input("Buybacks End", min_value=buyback_start, value=datetime.strptime(sys_param['buyback_end'][0], "%d.%m.%Y") if datetime(buyback_start.year, buyback_start.month, buyback_start.day) <= datetime.strptime(sys_param['buyback_end'][0], "%d.%m.%Y") else datetime(buyback_start.year, buyback_start.month, buyback_start.day), help="The date when monthly buybacks should end.")

            else:
                buyback_perc_per_month = [float(sys_param['buyback_perc_per_month'][0]) if enable_protocol_buybacks else 0.0][0]
                buyback_fixed_per_month = [float(sys_param['buyback_fixed_per_month'][0])/1e3 if enable_protocol_buybacks else 0.0][0]
                buyback_bucket = [sys_param['buyback_bucket'][0] if enable_protocol_buybacks else 'Reserve'][0]
                buyback_start = [datetime.strptime(sys_param['buyback_start'][0], "%d.%m.%Y") if enable_protocol_buybacks else token_launch_date][0]
                buyback_end = [datetime.strptime(sys_param['buyback_end'][0], "%d.%m.%Y") if enable_protocol_buybacks else token_launch_date][0]
        with col92:
            enable_protocol_burning = st.toggle('Enable Protocol Token Burning', value=float(sys_param['burn_per_month'][0]) > 0, help=" Enable the burning of tokens from a protocol bucket.")
            if enable_protocol_burning:
                burn_per_month = st.number_input('Burn per month / %', label_visibility="visible", min_value=0.0, value=[float(sys_param['burn_per_month'][0]) if enable_protocol_burning else 0.0][0], disabled=False, key="burn_per_month", help="The total supply percentage of tokens being burned from the determined protocol bucket per month.")
                burn_start = st.date_input("Burning Start", min_value=token_launch_date, value=datetime.strptime(sys_param['burn_start'][0], "%d.%m.%Y"), help="The date when monthly burning should start.")
                burn_end = st.date_input("Burning End", min_value=burn_start, value=datetime.strptime(sys_param['burn_end'][0], "%d.%m.%Y") if datetime(burn_start.year, burn_start.month, burn_start.day) <= datetime.strptime(sys_param['burn_end'][0], "%d.%m.%Y") else datetime(burn_start.year, burn_start.month, burn_start.day), help="The date when monthly burning should end.")
                burn_buckets = ['Reserve', 'Community', 'Foundation']
                burn_bucket = st.radio('Burn Bucket',tuple(burn_buckets), index=0, help='The burn bucket determines the protocol bucket origin of the burned tokens.')
            else:
                burn_per_month = [float(sys_param['burn_per_month'][0]) if enable_protocol_burning else 0.0][0]
                burn_bucket = [sys_param['burn_bucket'][0] if enable_protocol_burning else 'Reserve'][0]
                burn_start = [datetime.strptime(sys_param['burn_start'][0], "%d.%m.%Y") if enable_protocol_burning else token_launch_date][0]
                burn_end = [datetime.strptime(sys_param['burn_end'][0], "%d.%m.%Y") if enable_protocol_burning else token_launch_date][0]

        buyback_start = datetime(buyback_start.year, buyback_start.month, buyback_start.day)
        buyback_end = datetime(buyback_end.year, buyback_end.month, buyback_end.day)
        burn_start = datetime(burn_start.year, burn_start.month, burn_start.day)
        burn_end = datetime(burn_end.year, burn_end.month, burn_end.day)

        if enable_protocol_buybacks:
            if buyback_start < token_launch_date:
                st.error(f"The buyback starting date ({buyback_start.strftime('%d.%m.%Y')}) is before the launch date ({token_launch_date}). Please adjust the buyback starting date!", icon="⚠️")
        if enable_protocol_burning:
            if burn_start < token_launch_date:
                st.error(f"The burn starting date ({burn_start.strftime('%d.%m.%Y')}) is before the launch date ({token_launch_date}). Please adjust the burn starting date!", icon="⚠️")
        

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
        if agent_behavior == 'random':
            utility_values['Stake'].update({'agent_staking_apr_target':{
                    'value': sys_param['agent_staking_apr_target'][0] if 'agent_staking_apr_target' in sys_param else 10.0,
                    'display_name': 'APR Target / %',
                    'description': 'The agents target APR for staking rewards. Agents with random behavior will prioritize utility allocations over selling on average as long as the staking APR is above the APR target. Only applicable for random agent behavior!'
                    }})
        
        # remove utilities when not activated in the token allocation section
        if not incentivisation_toggle:
            try:
                utility_values.pop('Incentivisation')
            except:
                pass
        if not staking_vesting_toggle:
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

    """ with st.expander("**Advanced Settings**"):
        st.markdown("### Advanced Settings")
        st.write("Under development...") """
    
    if not token_launch:
        with st.expander("**Token In-Market Initialization (for already launched tokens)**"):
            st.markdown("### Token In-Market Initialization")
            st.markdown("Use the following input parameters to initialize the model for a token that already launched in the market. Note that all the above settings will still be valid and important for the simulation.")

            current_holdings = {}
            current_staked = {}
            vested_dict, vested_supply_sum = calc_vested_tokens_for_stakeholder(token_launch_date, initial_supply, vesting_dict)
            airdropped_supply_sum, remaining_airdrop_supply = calc_airdropped_tokens(token_launch_date, initial_supply, airdrop_allocation, airdrop_dict)
            
            staking_vesting_vested = vested_dict['staking_vesting']
            # distribute staking vesting rewarded tokens according to the staking vesting allocation
            # calculate all vested tokens for all non-protocol bucket stakeholders
            stakeholder_names, stakeholder_name_mapping = get_stakeholders()
            staking_vesting_receiver_vested_tokens = sum([vested_dict[stakeholder] for stakeholder in vested_dict if stakeholder_name_mapping[stakeholder] != 'protocol_bucket'])
            vested_dict_plus_staking_rewards = {}
            for stakeholder in vested_dict:
                if stakeholder_name_mapping[stakeholder] != 'protocol_bucket':
                    vested_dict_plus_staking_rewards[stakeholder] = vested_dict[stakeholder] + (vested_dict[stakeholder] / staking_vesting_receiver_vested_tokens) * staking_vesting_vested
                elif stakeholder != 'staking_vesting':
                    vested_dict_plus_staking_rewards[stakeholder] = vested_dict[stakeholder]
                else:
                    vested_dict_plus_staking_rewards[stakeholder] = 0.0

            col101, col102 = st.columns(2)
            with col101:
                current_initial_supply = st.number_input('Total Supply / m', label_visibility="visible", min_value=0.001, value=initial_supply, disabled=False, key="initial_supply", help="The total token supply. This can be different from the initial total supply if tokens got minted or burned since token launch.")
                if initial_supply < current_initial_supply:
                    st.info(f"The current total supply ({current_initial_supply}m) is higher than the initial total supply ({initial_supply}m). This means that new tokens got **minted** since token launch.", icon="ℹ️")
                if initial_supply > current_initial_supply:
                    st.info(f"The current total supply ({current_initial_supply}m) is lower than the initial total supply ({initial_supply}m). This means that tokens got **burned** since token launch.", icon="ℹ️")
                
                token_fdv = st.number_input('Current Token FDV / $m', label_visibility="visible", min_value=0.1, value=launch_valuation, disabled=False, key="token_fdv", help="The token fully diluted valuation.")

            with col102:
                st.text_input('Total Vested Tokens / m', value=f"{round(vested_supply_sum,2)}m", disabled=True, key=f"vested_supply_sum", help="Total amount of vested tokens according to the vesting schedule and token launch date.")
                st.text_input('Total Vested Tokens / % init. total supply', value=f"{round(vested_supply_sum/initial_supply*100,2)}%", disabled=True, key=f"vested_supply_sum_perc", help="Total amount of vested tokens as percentage share of the total supply according to the vesting schedule and token launch date.")

            col101a, col102a, col103a = st.columns(3)
            with col101a:
                col101b, col102b = st.columns(2)
                with col101b:
                    st.text_input('Blank', value="", label_visibility="hidden", disabled=True, key=f"blank_1")
                with col102b:
                    st.text_input('Blank', value="", label_visibility="hidden", disabled=True, key=f"blank_2")
                st.write("**Stakeholder**")
                for stakeholder in vested_dict_plus_staking_rewards:
                    if vesting_dict[stakeholder]['allocation'] > 0:
                        st.text_input('Stakeholder', value=[stakeholder if stakeholder is not 'incentivisation' else 'incentivisation_receivers'][0].replace("_"," ").title(), label_visibility="collapsed", disabled=True, key=f"stakeholder_{stakeholder}")
                if airdrop_toggle:
                    st.text_input('Airdrop Receivers', value='Airdrop Receivers', label_visibility="collapsed", disabled=True, key=f"stakeholder_airdrop_receivers")
                st.text_input('Market Investors', value='Market Investers', label_visibility="collapsed", disabled=True, key=f"stakeholder_market_investors")
                st.text_input('DEX Liquidity Pool', value='DEX Liquidity Pool', label_visibility="hidden", disabled=True, key=f"dex_liquidity_pool_in_market")
            
            with col102a:
                if 'Stake' not in utility_shares:
                    token_holding_ratio_share = st.number_input("Token Holding Ratio Share / %", value=100, disabled=True, key="avg_token_holding_allocation1", help="The currently held token supply share by the stakeholders")
                else:
                    token_holding_ratio_share = st.number_input("Token Holding Ratio Share / %", value=avg_token_holding_allocation, disabled=False, key="avg_token_holding_allocation2", help="The currently held token supply share by the stakeholders")
                st.write("**Token Holdings / m**")
                for stakeholder in vested_dict_plus_staking_rewards:
                    if vesting_dict[stakeholder]['allocation'] > 0:
                        current_holdings[stakeholder if stakeholder is not 'incentivisation' else 'incentivisation_receivers'] = st.number_input(f'Token Holdings ({stakeholder if stakeholder is not "incentivisation" else "incentivisation_receivers"}) / m', label_visibility="collapsed", format="%.4f", min_value=0.0, value=vested_dict_plus_staking_rewards[stakeholder]*token_holding_ratio_share/100 if stakeholder != 'staking_vesting' else 0.0, disabled=False if stakeholder != 'staking_vesting' else True, key=f"current_holdings_{stakeholder if stakeholder is not 'incentivisation' else 'incentivisation_receivers'}", help=f"The current holdings of {stakeholder if stakeholder is not 'incentivisation' else 'incentivisation_receivers'}.")
                if airdrop_toggle:
                    current_holdings['airdrop_receivers'] = st.number_input(f'Token Holdings (Airdrop Receivers) / m', label_visibility="collapsed", format="%.4f", min_value=0.0, value=float(airdropped_supply_sum)*token_holding_ratio_share/100, disabled=False, key=f"current_holdings_airdrop_receivers", help=f"The current holdings of the airdrop receivers.")
                current_holdings['market_investors'] = st.number_input(f'Token Holdings (Market Investors) / m', label_visibility="collapsed", format="%.4f", min_value=0.0, value=float(sys_param['market_investors_current_holdings'][0]/1e6) if 'market_investors_current_holdings' in sys_param else 0.0, disabled=False, key=f"current_holdings_market_investors", help=f"The current holdings of the market investors.")
            
            with col103a:
                if 'Stake' in utility_shares:
                    st.number_input("Token Staking Ratio Share / %", min_value=0.0, value=100.0-token_holding_ratio_share, disabled=True, key="avg_token_utility_allocation1", help="The currently staked token supply share by the stakeholders as ")
                    st.write("**Tokens Staked / m**")
                    for stakeholder in vested_dict_plus_staking_rewards:
                        if vesting_dict[stakeholder]['allocation'] > 0:
                            current_staked[stakeholder if stakeholder is not 'incentivisation' else 'incentivisation_receivers'] = st.number_input(f'Tokens Staked ({stakeholder if stakeholder is not "incentivisation" else "incentivisation_receivers"}) / m', label_visibility="collapsed", format="%.4f", min_value=0.0, value=vested_dict_plus_staking_rewards[stakeholder]*(1-token_holding_ratio_share/100) if stakeholder != 'staking_vesting' else 0.0, disabled=False if stakeholder != 'staking_vesting' else True, key=f"current_staked_{stakeholder if stakeholder is not 'incentivisation' else 'incentivisation_receivers'}", help=f"The current staked tokens of {stakeholder if stakeholder is not 'incentivisation' else 'incentivisation_receivers'}.")
                    if airdrop_toggle:
                        current_staked['airdrop_receivers'] = st.number_input(f'Tokens Staked (Airdrop Receivers) / m', label_visibility="collapsed", format="%.4f", min_value=0.0, value=float(airdropped_supply_sum)*(1-token_holding_ratio_share/100), disabled=False, key=f"current_staked_airdrop_receivers", help=f"The current staked tokens of the airdrop receivers.")
                    current_staked['market_investors'] = st.number_input(f'Tokens Staked (Market Investors) / m', label_visibility="collapsed", format="%.4f", min_value=0.0, value=float(sys_param['market_investors_current_staked'][0]/1e6) if 'market_investors_current_staked' in sys_param else 0.0, disabled=False, key=f"current_staked_market_investors", help=f"The current staked tokens of the market investors.")
            
            # calculate stakeholder allocation amounts
            stakeholder_allocations = 0
            for stakeholder in vesting_dict:
                stakeholder_allocations += vesting_dict[stakeholder]['allocation']
            stakeholder_allocations += airdrop_allocation if airdrop_toggle else 0
            stakeholder_allocations += current_holdings['market_investors'] + current_staked['market_investors']
            
            lp_allocation = (current_initial_supply - stakeholder_allocations)
            with col102a:
                st.number_input('LP Token Allocation / %', label_visibility="visible", value=lp_allocation / current_initial_supply * 100, disabled=True, key="lp_allocation1", help="The percentage of tokens allocated to the liquidity pool. This is the remaining percentage of tokens after all other allocations have been made. It must not be < 0 and determines the required capital to seed the liquidity.")
            with col103a:
                dex_capital = st.number_input('DEX Capital / $m', value=lp_allocation * token_fdv / current_initial_supply, disabled=True, key="liquidity_capital_requirements1", help="The required capital to seed the liquidity: left over lp token allocation x total_initial_supply / 100 % * token_launch_price.")

            # calculate the amount of tokens held and staked per stakeholder and check if the sum is greater than their initial allocation
            for stakeholder in current_holdings:
                if stakeholder != 'market_investors':
                    if stakeholder == 'airdrop_receivers':
                        if current_holdings[stakeholder] + current_staked[stakeholder] > airdropped_supply_sum + remaining_airdrop_supply:
                            st.warning(f"The current airdrop receiver holdings ({round(current_holdings[stakeholder],2)}m) plus staked supply ({round(current_staked[stakeholder],2)}m) are greater than the overall airdrop allocation ({round(airdrop_allocation,2)}m). Double check if this allocation matches your intention!", icon="⚠️")
                    else:
                        if current_holdings[stakeholder] + current_staked[stakeholder] > vesting_dict[stakeholder if stakeholder is not 'incentivisation_receivers' else 'incentivisation']['allocation']:
                            st.warning(f"The current holdings ({round(current_holdings[stakeholder],2)}m) plus staked supply ({round(current_staked[stakeholder],2)}m) are greater than the initial allocation ({round(vesting_dict[stakeholder if stakeholder is not 'incentivisation_receivers' else 'incentivisation']['allocation'],2)}m) for {stakeholder}. Double check if this allocation matches your intention!", icon="⚠️")

            if lp_allocation < 0:
                st.error(f"The LP token allocation ({round(lp_allocation,2)}%) is negative. Reduce stakeholder allocations!", icon="⚠️")
            
    # Map new parameters to model input parameters
    new_params = {
        'token_launch': token_launch,
        'launch_date': token_launch_date.strftime("%d.%m.%Y").split(" ")[0],
        'equity_external_shareholders_perc': equity_perc,
        'initial_total_supply': initial_supply*1e6,
        'public_sale_supply_perc': public_sale_supply,
        'public_sale_valuation': launch_valuation * 1e6,
        'angel_raised': equity_investments * 1e6,
        'fundraising_style': fundraising_style if not show_full_fund_table else 'Custom',
        'seed_raised': seed_raised* 1e6,
        'presale_1_raised': presale_1_raised* 1e6,
        'presale_2_raised': presale_2_raised* 1e6,
        'public_sale_raised': public_sale_raised* 1e6,
        'seed_valuation': seed_valuation* 1e6,
        'presale_1_valuation': presale_1_valuation* 1e6,
        'presale_2_valuation': presale_2_valuation* 1e6,
        'vesting_style': vesting_style if not show_full_alloc_table else 'Custom',
        'angel_initial_vesting': [angel_initial_vesting if vesting_style == 'Custom' or show_full_alloc_table else init_vesting_dict['angel']][0],
        'angel_cliff': [angel_cliff if vesting_style == 'Custom' or show_full_alloc_table else cliff_dict['angel']][0],
        'angel_vesting_duration': [angel_duration if vesting_style == 'Custom' or show_full_alloc_table else duration_dict['angel']][0],
        'seed_initial_vesting': [seed_initial_vesting if vesting_style == 'Custom' or show_full_alloc_table else init_vesting_dict['seed']][0],
        'seed_cliff': [seed_cliff if vesting_style == 'Custom' or show_full_alloc_table else cliff_dict['seed']][0],
        'seed_vesting_duration': [seed_duration if vesting_style == 'Custom' or show_full_alloc_table else duration_dict['seed']][0],
        'presale_1_initial_vesting': [presale_1_initial_vesting if vesting_style == 'Custom' or show_full_alloc_table else init_vesting_dict['presale_1']][0],
        'presale_1_cliff': [presale_1_cliff if vesting_style == 'Custom' or show_full_alloc_table else cliff_dict['presale_1']][0],
        'presale_1_vesting_duration': [presale_1_duration if vesting_style == 'Custom' or show_full_alloc_table else duration_dict['presale_1']][0],
        'presale_2_initial_vesting': [presale_2_initial_vesting if vesting_style == 'Custom' or show_full_alloc_table else init_vesting_dict['presale_2']][0],
        'presale_2_cliff': [presale_2_cliff if vesting_style == 'Custom' or show_full_alloc_table else cliff_dict['presale_2']][0],
        'presale_2_vesting_duration': [presale_2_duration if vesting_style == 'Custom' or show_full_alloc_table else duration_dict['presale_2']][0],
        'public_sale_initial_vesting': [public_sale_initial_vesting if vesting_style == 'Custom' or show_full_alloc_table else init_vesting_dict['public_sale']][0],
        'public_sale_cliff': [public_sale_cliff if vesting_style == 'Custom' or show_full_alloc_table else cliff_dict['public_sale']][0],
        'public_sale_vesting_duration': [public_sale_duration if vesting_style == 'Custom' or show_full_alloc_table else duration_dict['public_sale']][0],
        'team_allocation': team_allocation,
        'team_initial_vesting': [team_initial_vesting if vesting_style == 'Custom' or show_full_alloc_table else init_vesting_dict['team']][0],
        'team_cliff': [team_cliff if vesting_style == 'Custom' or show_full_alloc_table else cliff_dict['team']][0],
        'team_vesting_duration': [team_duration if vesting_style == 'Custom' or show_full_alloc_table else duration_dict['team']][0],
        'ov_allocation': 0,
        'ov_initial_vesting': 0,
        'ov_cliff': 0,
        'ov_vesting_duration': 0,
        'advisor_allocation': ov_advisor_allocation,
        'advisor_initial_vesting': [advisor_initial_vesting if vesting_style == 'Custom' or show_full_alloc_table else init_vesting_dict['advisor']][0],
        'advisor_cliff': [advisor_cliff if vesting_style == 'Custom' or show_full_alloc_table else cliff_dict['advisor']][0],
        'advisor_vesting_duration': [advisor_duration if vesting_style == 'Custom' or show_full_alloc_table else duration_dict['advisor']][0],
        'strategic_partners_allocation': strategic_partners_allocation,
        'strategic_partners_initial_vesting': [strategic_partners_initial_vesting if vesting_style == 'Custom' or show_full_alloc_table else init_vesting_dict['strategic_partners']][0],
        'strategic_partners_cliff': [strategic_partners_cliff if vesting_style == 'Custom' or show_full_alloc_table else cliff_dict['strategic_partners']][0],
        'strategic_partners_vesting_duration': [strategic_partners_duration if vesting_style == 'Custom' or show_full_alloc_table else duration_dict['strategic_partners']][0],
        'reserve_allocation': reserve_allocation,
        'reserve_initial_vesting': [reserve_initial_vesting if vesting_style == 'Custom' or show_full_alloc_table else init_vesting_dict['reserve']][0],
        'reserve_cliff': [reserve_cliff if vesting_style == 'Custom' or show_full_alloc_table else cliff_dict['reserve']][0],
        'reserve_vesting_duration': [reserve_duration if vesting_style == 'Custom' or show_full_alloc_table else duration_dict['reserve']][0],
        'community_allocation': community_allocation,
        'community_initial_vesting': [community_initial_vesting if vesting_style == 'Custom' or show_full_alloc_table else init_vesting_dict['community']][0],
        'community_cliff': [community_cliff if vesting_style == 'Custom' or show_full_alloc_table else cliff_dict['community']][0],
        'community_vesting_duration': [community_duration if vesting_style == 'Custom' or show_full_alloc_table else duration_dict['community']][0],
        'foundation_allocation': foundation_allocation,
        'foundation_initial_vesting': [foundation_initial_vesting if vesting_style == 'Custom' or show_full_alloc_table else init_vesting_dict['foundation']][0],
        'foundation_cliff': [foundation_cliff if vesting_style == 'Custom' or show_full_alloc_table else cliff_dict['foundation']][0],
        'foundation_vesting_duration': [foundation_duration if vesting_style == 'Custom' or show_full_alloc_table else duration_dict['foundation']][0],
        'incentivisation_allocation': incentivisation_allocation,
        'incentivisation_initial_vesting': [incentivisation_initial_vesting if vesting_style == 'Custom' or show_full_alloc_table else init_vesting_dict['incentivisation']][0],
        'incentivisation_cliff': [incentivisation_cliff if vesting_style == 'Custom' or show_full_alloc_table else cliff_dict['incentivisation']][0],
        'incentivisation_vesting_duration': [incentivisation_duration if vesting_style == 'Custom' or show_full_alloc_table else duration_dict['incentivisation']][0],
        'staking_vesting_allocation': staking_vesting_allocation,
        'staking_vesting_initial_vesting': [staking_vesting_initial_vesting if vesting_style == 'Custom' or show_full_alloc_table else init_vesting_dict['staking_vesting']][0],
        'staking_vesting_cliff': [staking_vesting_cliff if vesting_style == 'Custom' or show_full_alloc_table else cliff_dict['staking_vesting']][0],
        'staking_vesting_vesting_duration': [staking_vesting_duration if vesting_style == 'Custom' or show_full_alloc_table else duration_dict['staking_vesting']][0],
        'airdrop_allocation': airdrop_allocation,
        'airdrop_date1': [airdrop_date1.strftime('%d.%m.%Y') if airdrop_toggle else sys_param['airdrop_date1'][0]][0],
        'airdrop_amount1': [airdrop_amount1 if airdrop_toggle else sys_param['airdrop_amount1'][0]][0],
        'airdrop_date2': [airdrop_date2.strftime('%d.%m.%Y') if airdrop_toggle else sys_param['airdrop_date2'][0]][0],
        'airdrop_amount2': [airdrop_amount2 if airdrop_toggle else sys_param['airdrop_amount2'][0]][0],
        'airdrop_date3': [airdrop_date3.strftime('%d.%m.%Y') if airdrop_toggle else sys_param['airdrop_date3'][0]][0],
        'airdrop_amount3': [airdrop_amount3 if airdrop_toggle else sys_param['airdrop_amount3'][0]][0],
        'adoption_style': adoption_style if not show_full_adoption_table else 'Custom',
        'initial_product_users': initial_product_users,
        'initial_token_holders': initial_token_holders,
        'product_users_after_10y': product_users_after_10y,
        'token_holders_after_10y': token_holders_after_10y,
        'product_adoption_velocity': [product_adoption_velocity if adoption_style == 'Custom' or show_full_adoption_table else adoption_dict[adoption_style]['product_adoption_velocity']][0],
        'token_adoption_velocity': [token_adoption_velocity if adoption_style == 'Custom' or show_full_adoption_table else adoption_dict[adoption_style]['token_adoption_velocity']][0],
        'regular_product_revenue_per_user': [regular_product_revenue_per_user if adoption_style == 'Custom' or show_full_adoption_table else adoption_dict[adoption_style]['regular_product_revenue_per_user']][0],
        'regular_token_buy_per_user': [regular_token_buy_per_user if adoption_style == 'Custom' or show_full_adoption_table else adoption_dict[adoption_style]['regular_token_buy_per_user']][0],
        'agent_behavior': agent_behavior,
        'avg_token_utility_allocation': avg_token_utility_allocation,
        'avg_token_selling_allocation': avg_token_selling_allocation,
        'avg_token_holding_allocation': avg_token_holding_allocation,
        'avg_token_utility_removal': avg_token_utility_removal if (adoption_style == 'Custom' or show_full_adoption_table) and agent_behavior == 'static' else adoption_dict[adoption_style]['avg_token_utility_removal'] if agent_behavior == 'static' else 0,
        'royalty_income_per_month': royalty_income_per_month*1e3,
        'treasury_income_per_month': treasury_income_per_month*1e3,
        'other_income_per_month': other_income_per_month*1e3,
        'one_time_payments_1': one_time_payments_1*1e3,
        'salaries_per_month': salaries_per_month*1e3,
        'license_costs_per_month': license_costs_per_month*1e3,
        'other_monthly_costs': other_monthly_costs*1e3,
        'buyback_perc_per_month': buyback_perc_per_month,
        'buyback_fixed_per_month': buyback_fixed_per_month*1e3,
        'buyback_bucket': buyback_bucket,
        'buyback_start': buyback_start.strftime('%d.%m.%Y'),
        'buyback_end': buyback_end.strftime('%d.%m.%Y'),
        'burn_per_month': burn_per_month,
        'burn_bucket': burn_bucket,
        'burn_start': burn_start.strftime('%d.%m.%Y'),
        'burn_end': burn_end.strftime('%d.%m.%Y'),
    }

    # add utility parameters to new_params
    new_params.update(utility_parameter_choice)

    # add random seed to new_params
    if agent_behavior == 'random':
        new_params['random_seed'] = random_seed

    # add in-market initialization parameters to new_params
    if not token_launch:
        new_params['initial_total_supply'] = current_initial_supply*1e6
        new_params.update({
            'token_fdv': token_fdv*1e6
        })
        # add current_holdings, current_staked, and vested_dict dict entries to new_params
        for stakeholder in vested_dict:
            if vesting_dict[stakeholder]['allocation'] > 0:
                new_params.update({
                    f'{stakeholder if stakeholder is not "incentivisation" else "incentivisation_receivers"}_current_holdings': current_holdings[stakeholder if stakeholder is not 'incentivisation' else 'incentivisation_receivers']*1e6,
                    f'{stakeholder if stakeholder is not "incentivisation" else "incentivisation_receivers"}_current_staked': current_staked[stakeholder if stakeholder is not 'incentivisation' else 'incentivisation_receivers']*1e6,
                    f'{stakeholder}_vested_init': vested_dict[stakeholder]*1e6,
                })
        # add airdrop receivers to new_params
        if airdrop_toggle:
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
        new_params['initial_cash_balance'] = initial_cash_balance*1e3

    # Consistency Checks
    if (lp_allocation < 0 or (meta_bucket_alloc_sum != 100 and agent_behavior == 'static') or (dex_capital > raised_funds and token_launch) or utility_sum != 100 or
        (min(airdrop_date1, airdrop_date2, airdrop_date3) < token_launch_date and airdrop_toggle) or
        (buyback_start < token_launch_date and enable_protocol_buybacks) or (burn_start < token_launch_date and enable_protocol_burning) or
        (initial_cash_balance == 0 and (royalty_income_per_month + treasury_income_per_month + other_income_per_month + initial_product_users *
                                        [regular_product_revenue_per_user if adoption_style == 'Custom' or show_full_adoption_table else adoption_dict[adoption_style]['regular_product_revenue_per_user']][0] -
                                        salaries_per_month - license_costs_per_month - other_monthly_costs) and not token_launch)):
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
        
        if dex_capital > raised_funds and token_launch:
            st.error(f"The required capital ({round(dex_capital,2)}m) to seed the liquidity is higher than the raised funds (${round(raised_funds,2)}m). Please reduce the LP Token Allocation or the Launch Valuation!", icon="⚠️")
        
        if not token_launch:
            if (initial_cash_balance == 0 and (royalty_income_per_month + treasury_income_per_month + other_income_per_month + initial_product_users *
                                               [regular_product_revenue_per_user if adoption_style == 'Custom' or show_full_adoption_table else adoption_dict[adoption_style]['regular_product_revenue_per_user']][0] -
                                               salaries_per_month - license_costs_per_month - other_monthly_costs) and not token_launch):
                st.error(f"The initial cash balance is 0. Please adjust the initial cash balance or the monthly income and cost parameters!", icon="⚠️")


        if lp_allocation < 0:
            st.error(f"The LP token allocation ({round(lp_allocation,2)}%) is negative. Reduce the stakeholder allocations!", icon="⚠️")
        
        if airdrop_toggle:
            if airdrop_date1 < token_launch_date:
                st.error(f"The first airdrop date ({airdrop_date1.strftime('%d.%m.%Y')}) is before the launch date ({token_launch_date}). Please adjust the airdrop date!", icon="⚠️")
            if airdrop_date2 < token_launch_date:
                st.error(f"The second airdrop date ({airdrop_date2.strftime('%d.%m.%Y')}) is before the launch date ({token_launch_date}). Please adjust the airdrop date!", icon="⚠️")
            if airdrop_date3 < token_launch_date:
                st.error(f"The third airdrop date ({airdrop_date3.strftime('%d.%m.%Y')}) is before the launch date ({token_launch_date}). Please adjust the airdrop date!", icon="⚠️")

        if enable_protocol_buybacks:
            if buyback_start < token_launch_date:
                st.error(f"The buyback starting date ({buyback_start.strftime('%d.%m.%Y')}) is before the launch date ({token_launch_date}). Please adjust the buyback starting date!", icon="⚠️")
        if enable_protocol_burning:
            if burn_start < token_launch_date:
                st.error(f"The burn starting date ({burn_start.strftime('%d.%m.%Y')}) is before the launch date ({token_launch_date}). Please adjust the burn starting date!", icon="⚠️")

        if meta_bucket_alloc_sum != 100 and agent_behavior == 'static':
            st.error(f"The sum of the average token allocations for utility, selling and holding ({avg_token_utility_allocation + avg_token_selling_allocation + avg_token_holding_allocation}%) is not equal to 100%. Please adjust the values!", icon="⚠️")
        
        if utility_sum != 100:
            st.error(f"The sum of the utility allocations ({utility_sum}%) is not equal to 100%. Please adjust the values!", icon="⚠️")
        
        if count_staking_utilities > 1:
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