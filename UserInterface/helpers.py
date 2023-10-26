import streamlit as st
from plots import *
from Model.parts.utils import *

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

def model_ui_inputs(input_file_path, uploaded_file, parameter_list):
    if 'param_id' in st.session_state:
        parameter_id_choice = st.session_state['param_id']
    else:
        parameter_id_choice = ""

    col11, col12, col13 = st.columns(3)
    # Adjusting Parameters
    if parameter_id_choice == "":
        sys_param = compose_initial_parameters(pd.read_csv(input_file_path), parameter_list)
    else:
        sys_param_df = get_simulation_data('simulationData.db', 'sys_param')
        if len(sys_param_df[sys_param_df['id'] == parameter_id_choice])<1:
            sys_param = compose_initial_parameters(pd.read_csv(input_file_path), parameter_list)
        else:
            sys_param = {k:[v] for k, v in sys_param_df[sys_param_df['id'] == parameter_id_choice].to_dict('index')[list(sys_param_df[sys_param_df['id'] == parameter_id_choice].to_dict('index').keys())[0]].items()}
        
    with col11:
        supply_type = st.radio('Supply Type',('Fixed', 'Inflationary'), index=['Fixed', 'Inflationary'].index(sys_param['supply_type'][0]), key='supply_type_radio', help="Determines if a minting functionallity is allowed.")
        equity_investors = st.toggle('Equity Investors', value=sys_param['equity_external_shareholders_perc'][0] != 0.0, help="Enable early equity angle investors")
        initial_supply = st.number_input('Initial Total Token Supply / mil.', min_value=0.001, max_value=1000000.0, value=float(sys_param['initial_total_supply'][0]/1e6) , help="The initial total token supply.")
    with col12:
        launch_valuation = st.number_input('Public Sale Valuation / $m', min_value=0.1, max_value=500.0, value=float(sys_param['public_sale_valuation'][0]/1e6), help="This is the valuation at which the public sale tokens are sold. It is equivalent to the token launch valuation.")
        public_sale_supply = st.number_input('Public Sale Supply / %', min_value=0.0, max_value=95.0, value=float(str(sys_param['public_sale_supply_perc'][0]).split("%")[0]), help="The percentage of tokens sold in the public sale.")
        st.write("Launch Price: "+ str(launch_valuation/initial_supply)+" $/token")
    with col13:
        if equity_investors:
            equity_investments = st.number_input('Angle & Equity Raises / $m', min_value=0.0, value=float(sys_param['angle_raised'][0]/1e6), help="The amount of money raised from equity investors.")
            equity_perc = st.number_input('Equity sold / %', min_value=0.0, max_value=90.0, value=float(str(sys_param['equity_external_shareholders_perc'][0]).split("%")[0]), help="The percentage of equity sold to external shareholders.")
        else:
            equity_investments = 0.0
            equity_perc = 0.0        
    


    st.markdown("### Fundraising")
    col21, col22, col23 = st.columns(3)
    with col21:
        fundraising_style = st.radio('Fundraising Style',('Moderate', 'Medium', 'Aggressive','Custom'), index=0, help=param_help['fundraising_style'])
        if fundraising_style != 'Custom':
            show_full_fund_table = st.toggle('Show Full Table', value=False, help="Show the full token fundraising table.")
        else:
            show_full_fund_table = False
        if fundraising_style != 'Custom':
            target_raise = st.number_input('Overall Capital Raise Target / $m', min_value=0.1, max_value=500.0, value=float(sys_param['raised_capital_sum'][0])/1e6, help="The overall capital raise target.")
            left_over_raise = target_raise - equity_investments
    with col23:
        if fundraising_style != 'Custom' and not show_full_fund_table:
            seed_valuation = np.linspace(launch_valuation/fundraising_style_map[fundraising_style], launch_valuation, 4)[0]
            presale_1_valuation = np.linspace(launch_valuation/fundraising_style_map[fundraising_style], launch_valuation, 4)[1]
            presale_2_valuation = np.linspace(launch_valuation/fundraising_style_map[fundraising_style], launch_valuation, 4)[2]
        else:
            seed_valuation = st.number_input('Seed Valuation / $m', min_value=0.01, value=float([np.linspace(launch_valuation/fundraising_style_map[fundraising_style], launch_valuation, 4)[0] if uploaded_file is None and fundraising_style != 'Custom' else float(sys_param['seed_valuation'][0]/1e6)][0]), help="The valuation of the seed round.")
            presale_1_valuation = st.number_input('Presale 1 Valuation / $m', min_value=0.01, value=float([np.linspace(launch_valuation/fundraising_style_map[fundraising_style], launch_valuation, 4)[1] if uploaded_file is None and fundraising_style != 'Custom' else float(sys_param['presale_1_valuation'][0]/1e6)][0]), help="The valuation of the first presale.")
            presale_2_valuation = st.number_input('Presale 2 Valuation / $m', min_value=0.01, value=float([np.linspace(launch_valuation/fundraising_style_map[fundraising_style], launch_valuation, 4)[2] if uploaded_file is None and fundraising_style != 'Custom' else float(sys_param['presale_2_valuation'][0]/1e6)][0]), help="The valuation of the second presale.")

    with col22:
        valuation_weights = {
            "seed" : seed_valuation / launch_valuation,
            "presale_1" : presale_1_valuation / launch_valuation,
            "presale_2" : presale_2_valuation / launch_valuation,
            "public_sale" : 1.0
        }
        valuation_weights_sum = sum(valuation_weights.values())
        if fundraising_style != 'Custom' and not show_full_fund_table:
            seed_raised = float(valuation_weights["seed"]/valuation_weights_sum * left_over_raise)
            presale_1_raised = float(valuation_weights["presale_1"]/valuation_weights_sum * left_over_raise)
            presale_2_raised = float(valuation_weights["presale_2"]/valuation_weights_sum * left_over_raise)
            public_sale_raised = float(valuation_weights["public_sale"]/valuation_weights_sum * left_over_raise)
            raised_funds = equity_investments + seed_raised + presale_1_raised + presale_2_raised + public_sale_raised
        else:
            seed_raised = st.number_input('Seed Raises / $m', min_value=0.0, value=float([valuation_weights["seed"]/valuation_weights_sum * left_over_raise if uploaded_file is None and fundraising_style != 'Custom' else float(sys_param['seed_raised'][0]/1e6)][0]), help="The amount of money raised in the seed round.")
            presale_1_raised = st.number_input('Presale 1 Raises / $m', min_value=0.0, value=float([valuation_weights["presale_1"]/valuation_weights_sum * left_over_raise if uploaded_file is None and fundraising_style != 'Custom' else float(sys_param['presale_1_raised'][0]/1e6)][0]), help="The amount of money raised in the first presale.")
            presale_2_raised = st.number_input('Presale 2 Raises / $m', min_value=0.0, value=float([valuation_weights["presale_2"]/valuation_weights_sum * left_over_raise if uploaded_file is None and fundraising_style != 'Custom' else float(sys_param['presale_2_raised'][0]/1e6)][0]), help="The amount of money raised in the second presale.")
            public_sale_raised = st.number_input('Public Sale Raises / $m', min_value=0.0, value=float([valuation_weights["public_sale"]/valuation_weights_sum * left_over_raise if uploaded_file is None and fundraising_style != 'Custom' else float(sys_param['public_sale_raised'][0]/1e6)][0]), help="The amount of money raised in the public sale.")

            raised_funds = equity_investments + seed_raised + presale_1_raised + presale_2_raised + public_sale_raised
            if fundraising_style == 'Custom' or show_full_fund_table:
                st.write("Total Raised: "+str(raised_funds)+" $m")



    st.markdown("### Token Allocations & Vesting")
    col31, col32 = st.columns(2)
    with col31:
        vesting_style = st.radio('Vesting Style',('Slow', 'Medium', 'Fast','Custom'), index=0, help=param_help['vesting_style'])
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
                st.text_input("Angle","Angle", label_visibility="collapsed", disabled=True, key="angle_name")
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
                equity_allocation_new = st.number_input('equity_allocation_new', label_visibility="collapsed", min_value=0.0, value=equity_allocation, disabled=True, key="angle_allocation")
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
            airdrop_date1 = datetime.strptime(sys_param['airdrop_date1'][0], "%d.%m.%y")
            airdrop_date2 = datetime.strptime(sys_param['airdrop_date2'][0], "%d.%m.%y")
            airdrop_date3 = datetime.strptime(sys_param['airdrop_date3'][0], "%d.%m.%y")
            lp_allocation = (100 - equity_allocation_new - seed_allocation - presale_1_allocation
                             - presale_2_allocation - public_sale_allocation - team_allocation - ov_advisor_allocation
                             - strategic_partners_allocation - reserve_allocation - community_allocation
                             - foundation_allocation - incentivisation_allocation - staking_vesting_allocation
                             - airdrop_allocation)

            
    with col43:
        if vesting_style == 'Slow':
            init_vesting_dict = {
                "angle" : 0.0,
                "seed" : 0.0,
                "presale_1" : 0.0,
                "presale_2" : 0.0,
                "public_sale" : 10.0,
                "team" : 0.0,
                "advisors" : 0.0,
                "strategic_partners" : 0.0,
                "reserve" : 10.0,
                "community" : 10.0,
                "foundation" : 10.0,
                "incentivisation" : 0.0,
                "staking_vesting" : 0.0
            }
        if vesting_style == 'Medium':
            init_vesting_dict = {
                "angle" : 0.0,
                "seed" : 0.0,
                "presale_1" : 0.0,
                "presale_2" : 5.0,
                "public_sale" : 15.0,
                "team" : 0.0,
                "advisors" : 0.0,
                "strategic_partners" : 0.0,
                "reserve" : 10.0,
                "community" : 10.0,
                "foundation" : 10.0,
                "incentivisation" : 0.0,
                "staking_vesting" : 0.0
            }
        if vesting_style == 'Fast':
            init_vesting_dict = {
                "angle" : 0.0,
                "seed" : 0.0,
                "presale_1" : 5.0,
                "presale_2" : 15.0,
                "public_sale" : 35.0,
                "team" : 0.0,
                "advisors" : 0.0,
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
                angle_initial_vesting = st.number_input("angle_initial_vesting", label_visibility="collapsed", min_value=0.0, value=[sys_param['angle_initial_vesting'][0] if vesting_style == 'Custom' else init_vesting_dict['angle']][0], key="angle_initial_vesting")
            else:
                angle_initial_vesting = 0.0
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
            advisor_initial_vesting = st.number_input("advisor_initial_vesting", label_visibility="collapsed", min_value=0.0, value=[(sys_param['ov_initial_vesting'][0]+sys_param['advisor_initial_vesting'][0])/2 if vesting_style == 'Custom' else init_vesting_dict['advisors']][0], key="advisor_initial_vesting")
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
                airdrop_date1 = st.date_input("Airdrop Date 1", min_value=datetime.strptime(sys_param['launch_date'][0], "%d.%m.%y"), value=datetime.strptime(sys_param['airdrop_date1'][0], "%d.%m.%y"), help="The date of the first airdrop.")
                airdrop_amount1 = st.number_input("Amount 1 / %", min_value=0.0, value=sys_param['airdrop_amount1'][0], help="The share of tokens distributed from the airdrop allocation in the first airdrop.")

    with col44:
        if vesting_style == 'Slow':
            cliff_dict = {
                "angle" : 24,
                "seed" : 18,
                "presale_1" : 12,
                "presale_2" : 9,
                "public_sale" : 3,
                "team" : 24,
                "advisors" : 18,
                "strategic_partners" : 18,
                "reserve" : 0,
                "community" : 0,
                "foundation" : 0,
                "incentivisation" : 0,
                "staking_vesting" : 0
            }
        if vesting_style == 'Medium':
            cliff_dict = {
                "angle" : 18,
                "seed" : 12,
                "presale_1" : 9,
                "presale_2" : 6,
                "public_sale" : 0,
                "team" : 18,
                "advisors" : 12,
                "strategic_partners" : 12,
                "reserve" : 0,
                "community" : 0,
                "foundation" : 0,
                "incentivisation" : 0,
                "staking_vesting" : 0
            }
        if vesting_style == 'Fast':
            cliff_dict = {
                "angle" : 12,
                "seed" : 9,
                "presale_1" : 6,
                "presale_2" : 3,
                "public_sale" : 0,
                "team" : 12,
                "advisors" : 9,
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
                angle_cliff = st.number_input("angle_cliff", label_visibility="collapsed", min_value=0, value=int([sys_param['angle_cliff'][0] if vesting_style == 'Custom' else cliff_dict['angle']][0]), key="angle_cliff")
            else:
                angle_cliff = 0.0
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
            advisor_cliff = st.number_input("advisor_cliff", label_visibility="collapsed", min_value=0, value=int([sys_param['advisor_cliff'][0] if vesting_style == 'Custom' else cliff_dict['advisors']][0]), key="advisor_cliff")
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
                airdrop_date2 = st.date_input("Airdrop Date 2", min_value=datetime.strptime(sys_param['launch_date'][0], "%d.%m.%y"), value=datetime.strptime(sys_param['airdrop_date2'][0], "%d.%m.%y"), help="The date of the second airdrop.")
                airdrop_amount2 = st.number_input("Amount 2 / %", min_value=0.0, value=sys_param['airdrop_amount2'][0], help="The share of tokens distributed from the airdrop allocation in the second airdrop.")
  
    with col45:
        if vesting_style == 'Slow':
            duration_dict = {
                "angle" : 72,
                "seed" : 48,
                "presale_1" : 36,
                "presale_2" : 24,
                "public_sale" : 12,
                "team" : 72,
                "advisors" : 48,
                "strategic_partners" : 48,
                "reserve" : 72,
                "community" : 72,
                "foundation" : 72,
                "incentivisation" : 72,
                "staking_vesting" : 72
            }
        if vesting_style == 'Medium':
            duration_dict = {
                "angle" : 48,
                "seed" : 36,
                "presale_1" : 24,
                "presale_2" : 12,
                "public_sale" : 6,
                "team" : 48,
                "advisors" : 36,
                "strategic_partners" : 36,
                "reserve" : 48,
                "community" : 48,
                "foundation" : 48,
                "incentivisation" : 48,
                "staking_vesting" : 48
            }
        if vesting_style == 'Fast':
            duration_dict = {
                "angle" : 36,
                "seed" : 24,
                "presale_1" : 12,
                "presale_2" : 6,
                "public_sale" : 0,
                "team" : 36,
                "advisors" : 24,
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
                angle_duration = st.number_input("angle_duration", label_visibility="collapsed", min_value=0, value=int([sys_param['angle_vesting_duration'][0] if vesting_style == 'Custom' else duration_dict['angle']][0]), key="angle_vesting_duration")
            else:
                angle_duration = 0.0
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
            advisor_duration = st.number_input("advisor_duration", label_visibility="collapsed", min_value=0, value=int([(sys_param['advisor_vesting_duration'][0] + sys_param['ov_vesting_duration'][0])/2 if vesting_style == 'Custom' else duration_dict['advisors']][0]), key="advisor_vesting_duration")
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
                airdrop_date3 = st.date_input("Airdrop Date 3", min_value=datetime.strptime(sys_param['launch_date'][0], "%d.%m.%y"), value=datetime.strptime(sys_param['airdrop_date3'][0], "%d.%m.%y"), help="The date of the third airdrop.")
                airdrop_amount3 = st.number_input("Amount 3 / %", min_value=0.0, value=sys_param['airdrop_amount3'][0], help="The share of tokens distributed from the airdrop allocation in the third airdrop.")

    if show_full_alloc_table or vesting_style == 'Custom':
        col51, col52, col53 = st.columns(3)
        with col51:
            st.text_input("DEX LP","DEX Liquidity Pool", label_visibility="hidden", disabled=True, key="lp_name")
        with col52:
            st.number_input('LP Token Allocation / %', label_visibility="visible", value=lp_allocation, disabled=True, key="lp_allocation", help="The percentage of tokens allocated to the liquidity pool. This is the remaining percentage of tokens after all other allocations have been made. It must not be < 0 and determines the required capital to seed the liquidity.")
        with col53:
            st.number_input('DEX Capital / $m', max_value=raised_funds,value=float((lp_allocation/100 )* initial_supply * launch_valuation / initial_supply), disabled=True, key="liquidity_capital_requirements", help="The required capital to seed the liquidity: lp_allocation x total_initial_supply / 100 % * token_launch_price.")


    st.markdown("### User Adoption")
    # adoption style choice | user numbers | revenues | meta bucket allocations
    col61, col62, col63 = st.columns(3)
    with col61:
        adoption_style = st.radio('Adoption Assumption',('Weak', 'Medium', 'Strong', 'Custom'), index=0, help='The adoption style determines the scaling velocity for the product revenue and token demand. Moreover it influences the average agent sentiment in terms of selling and utility adoption behavior.')
        show_full_adoption_table = st.toggle('Show Full Table', value=False, help="Show the full adoption parameter set.")
    with col62:
        product_token_ratio = st.slider('Product / Token Weight', min_value=-1.0, max_value=1.0, step=0.1, value=(-float(sys_param['initial_product_users'][0]) + float(sys_param['initial_token_holders'][0])), format="%.2f", help="The weight of product users to token holders. -1 means there are no product users, but only token holders. 1 means the opposite and 0 means that there are as many product users as token holders.")
        initial_users = st.number_input('Initial Users', label_visibility="visible", value=int(sys_param['initial_product_users'][0]) + int(sys_param['initial_token_holders'][0]), disabled=False, key="initial_users", help="Initial amount of users to be divided between product users and token holders according to the Product / Token Weight.")
        initial_product_users = initial_users * (1 - (product_token_ratio)) / 2
        initial_token_holders = initial_users - initial_product_users

    with col63:
        st.write(f"Initial Token Holders: {int(np.ceil(initial_token_holders)):+,}")
        st.write(f"Initial Product Users: {int(np.ceil(initial_product_users)):+,}")

    adoption_dict = {
        "Weak" : {
            "avg_product_user_growth_rate" : 1.0,
            "avg_token_holder_growth_rate" : 1.0,
            "product_adoption_velocity" : 0.5,
            "token_adoption_velocity" : 0.5,
            "one_time_product_revenue_per_user" : 0.0,
            "regular_product_revenue_per_user" : 5.0,
            "one_time_token_buy_per_user" : 0.0,
            "regular_token_buy_per_user" : 5.0,
            "avg_token_utility_allocation" : 20.0,
            "avg_token_selling_allocation" : 70.0,
            "avg_token_holding_allocation" : 10.0,
            "avg_token_utility_removal" : 10.0,

        },
        "Medium" : {
            "avg_product_user_growth_rate" : 3.5,
            "avg_token_holder_growth_rate" : 3.5,
            "product_adoption_velocity" : 1.5,
            "token_adoption_velocity" : 1.5,
            "one_time_product_revenue_per_user" : 0.0,
            "regular_product_revenue_per_user" : 15.0,
            "one_time_token_buy_per_user" : 0.0,
            "regular_token_buy_per_user" : 15.0,
            "avg_token_utility_allocation" : 50.0,
            "avg_token_selling_allocation" : 40.0,
            "avg_token_holding_allocation" : 10.0,
            "avg_token_utility_removal" : 6.0,

        },
        "Strong" : {
            "avg_product_user_growth_rate" : 8.0,
            "avg_token_holder_growth_rate" : 8.0,
            "product_adoption_velocity" : 3.5,
            "token_adoption_velocity" : 3.5,
            "one_time_product_revenue_per_user" : 0.0,
            "regular_product_revenue_per_user" : 25.0,
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
            avg_product_user_growth_rate = st.number_input('Avg. Product Users Growth Rate / %', label_visibility="visible", value=[((float(sys_param['product_users_after_10y'][0]) / float(sys_param['initial_product_users'][0]))**(1/120.0)-1)*100 if adoption_style == 'Custom' else adoption_dict[adoption_style]['avg_product_user_growth_rate']][0], disabled=False, key="product_users_growth_rate", help="The average monthly growth rate of product users.")
            product_users_after_10y = initial_product_users * (1 + avg_product_user_growth_rate/100)**120
            st.write(f"Projected Product Users (10y): {int(np.ceil(product_users_after_10y)):+,}")
            product_adoption_velocity = st.number_input('Product Adoption Velocity', label_visibility="visible", value=[float(sys_param['product_adoption_velocity'][0]) if adoption_style == 'Custom' else adoption_dict[adoption_style]['product_adoption_velocity']][0], disabled=False, key="product_adoption_velocity", help="The velocity of product adoption. The higher the velocity, the faster the product adoption in the early years towards market saturation.")
            regular_product_revenue_per_user = st.number_input('Regular Product Revenue / $', label_visibility="visible", value=[float(sys_param['regular_product_revenue_per_user'][0]) if adoption_style == 'Custom' else adoption_dict[adoption_style]['regular_product_revenue_per_user']][0], disabled=False, key="regular_product_revenue_per_user", help="The average regular monthly product revenue per user. This will accrue directly to the business funds.")
        with col72:
            avg_token_holder_growth_rate = st.number_input('Avg. Token Holder Growth Rate / %', label_visibility="visible", value=[((float(sys_param['token_holders_after_10y'][0]) / float(sys_param['initial_token_holders'][0]))**(1/120.0)-1)*100 if adoption_style == 'Custom' else adoption_dict[adoption_style]['avg_token_holder_growth_rate']][0], disabled=False, key="avg_token_holder_growth_rate", help="The average monthly growth rate of token holders.")
            token_holders_after_10y = initial_token_holders * (1 + avg_token_holder_growth_rate/100)**120
            st.write(f"Projected Token Holders (10y): {int(np.ceil(token_holders_after_10y)):+,}")
            token_adoption_velocity = st.number_input('Token Adoption Velocity', label_visibility="visible", value=[float(sys_param['token_adoption_velocity'][0]) if adoption_style == 'Custom' else adoption_dict[adoption_style]['token_adoption_velocity']][0], disabled=False, key="token_adoption_velocity", help="The velocity of token adoption. The higher the velocity, the faster the token adoption in the early years towards market saturation.")
            regular_token_buy_per_user = st.number_input('Regular Token Buy / $', label_visibility="visible", value=[float(sys_param['regular_token_buy_per_user'][0]) if adoption_style == 'Custom' else adoption_dict[adoption_style]['regular_token_buy_per_user']][0], disabled=False, key="regular_token_buy_per_user", help="The average regular monthly token buy per token holder. This will accrue directly to the token via buys from the DEX liquidity pool.")
        st.write("**Meta Bucket Allocations**")
        col73, col74, col75, col76 = st.columns(4)
        with col73:
            avg_token_selling_allocation = st.number_input('Avg. Token Selling Allocation / %', label_visibility="visible", value=[float(sys_param['avg_token_selling_allocation'][0]) if adoption_style == 'Custom' else adoption_dict[adoption_style]['avg_token_selling_allocation']][0], disabled=False, key="avg_token_selling_allocation", help="The average monthly token allocation for selling purposes from all holding supply.")
        with col74:
            avg_token_holding_allocation = st.number_input('Avg. Token Holding Allocation / %', label_visibility="visible", value=[float(sys_param['avg_token_holding_allocation'][0]) if adoption_style == 'Custom' else adoption_dict[adoption_style]['avg_token_holding_allocation']][0], disabled=False, key="avg_token_holding_allocation", help="The average monthly token allocation for holding purposes from all holding supply.")
        with col75:
            avg_token_utility_allocation = st.number_input('Avg. Token Utility Allocation / %', label_visibility="visible", value=[float(sys_param['avg_token_utility_allocation'][0]) if adoption_style == 'Custom' else adoption_dict[adoption_style]['avg_token_utility_allocation']][0], disabled=False, key="avg_token_utility_allocation", help="The average monthly token allocation for utility purposes from all holding supply.")
        with col76:
            avg_token_utility_removal = st.number_input('Avg. Token Utility Removal / %', label_visibility="visible", value=[float(sys_param['avg_token_utility_removal'][0]) if adoption_style == 'Custom' else adoption_dict[adoption_style]['avg_token_utility_removal']][0], disabled=False, key="avg_token_utility_removal", help="The average monthly token removal from staking and liquidity mining utilities.")
    else:
        avg_product_user_growth_rate = adoption_dict[adoption_style]['avg_product_user_growth_rate']
        product_users_after_10y = initial_product_users * (1 + avg_product_user_growth_rate/100)**120
        avg_token_holder_growth_rate = adoption_dict[adoption_style]['avg_token_holder_growth_rate']
        token_holders_after_10y = initial_token_holders * (1 + avg_token_holder_growth_rate/100)**120


    st.markdown("### Business Assumptions")
    # income | expenditures | buybacks | burns
    st.write("**Financial Streams**")
    col81, col82, col83 = st.columns(3)
    with col81:
        show_full_business_table = st.toggle('Use Full Custom Table', value=False, help="Show the full business assumption parameter set.")
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
    
    st.write("**Buybacks and Burns**")
    col91, col92, col93 = st.columns(3)
    with col91:
        enable_protocol_buybacks = st.toggle('Enable Protocol Token Buybacks', value=float(sys_param['buyback_perc_per_month'][0]) > 0 or float(sys_param['buyback_fixed_per_month'][0]) > 0, help=" Enable the buyback of tokens from a protocol bucket.")
        enable_protocol_burning = st.toggle('Enable Protocol Token Burning', value=float(sys_param['burn_per_month'][0]) > 0, help=" Enable the burning of tokens from a protocol bucket.")
    with col92:
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
            buyback_start = st.date_input("Buybacks Start", min_value=datetime.strptime(sys_param['launch_date'][0], "%d.%m.%y"), value=datetime.strptime(sys_param['buyback_start'][0], "%d.%m.%y"), help="The date when monthly buybacks should start.")
            buyback_end = st.date_input("Buybacks End", min_value=buyback_start, value=datetime.strptime(sys_param['buyback_end'][0], "%d.%m.%y"), help="The date when monthly buybacks should end.")

        else:
            buyback_perc_per_month = [float(sys_param['buyback_perc_per_month'][0]) if enable_protocol_buybacks else 0.0][0]
            buyback_fixed_per_month = [float(sys_param['buyback_fixed_per_month'][0])/1e3 if enable_protocol_buybacks else 0.0][0]
            buyback_bucket = [sys_param['buyback_bucket'][0] if enable_protocol_buybacks else 'Reserve'][0]
            buyback_start = [datetime.strptime(sys_param['buyback_start'][0], "%d.%m.%y") if enable_protocol_buybacks else datetime.strptime(sys_param['launch_date'][0], "%d.%m.%y")][0]
            buyback_end = [datetime.strptime(sys_param['buyback_end'][0], "%d.%m.%y") if enable_protocol_buybacks else datetime.strptime(sys_param['launch_date'][0], "%d.%m.%y")][0]
    with col93:
        if enable_protocol_burning:
            burn_per_month = st.number_input('Burn per month / %', label_visibility="visible", min_value=0.0, value=[float(sys_param['burn_per_month'][0]) if enable_protocol_burning else 0.0][0], disabled=False, key="burn_per_month", help="The total supply percentage of tokens being burned from the determined protocol bucket per month.")
            burn_start = st.date_input("Burning Start", min_value=datetime.strptime(sys_param['launch_date'][0], "%d.%m.%y"), value=datetime.strptime(sys_param['burn_start'][0], "%d.%m.%y"), help="The date when monthly burning should start.")
            burn_end = st.date_input("Burning End", min_value=burn_start, value=datetime.strptime(sys_param['burn_end'][0], "%d.%m.%y"), help="The date when monthly burning should end.")
            burn_buckets = ['Reserve', 'Community', 'Foundation']
            burn_bucket = st.radio('Burn Bucket',tuple(burn_buckets), index=0, help='The burn bucket determines the protocol bucket origin of the burned tokens.')
        else:
            burn_per_month = [float(sys_param['burn_per_month'][0]) if enable_protocol_burning else 0.0][0]
            burn_bucket = [sys_param['burn_bucket'][0] if enable_protocol_burning else 'Reserve'][0]
            burn_start = [datetime.strptime(sys_param['burn_start'][0], "%d.%m.%y") if enable_protocol_burning else datetime.strptime(sys_param['launch_date'][0], "%d.%m.%y")][0]
            burn_end = [datetime.strptime(sys_param['burn_end'][0], "%d.%m.%y") if enable_protocol_burning else datetime.strptime(sys_param['launch_date'][0], "%d.%m.%y")][0]
    
    # Map new parameters to model input parameters
    new_params = {
        'equity_external_shareholders_perc': equity_perc,
        'supply_type': supply_type,
        'initial_total_supply': initial_supply*1e6,
        'public_sale_supply_perc': public_sale_supply,
        'public_sale_valuation': launch_valuation * 1e6,
        'angle_raised': equity_investments * 1e6,
        'seed_raised': seed_raised* 1e6,
        'presale_1_raised': presale_1_raised* 1e6,
        'presale_2_raised': presale_2_raised* 1e6,
        'public_sale_raised': public_sale_raised* 1e6,
        'seed_valuation': seed_valuation* 1e6,
        'presale_1_valuation': presale_1_valuation* 1e6,
        'presale_2_valuation': presale_2_valuation* 1e6,
        'angle_initial_vesting': [angle_initial_vesting if vesting_style == 'Custom' or show_full_alloc_table else init_vesting_dict['angle']][0],
        'angle_cliff': [angle_cliff if vesting_style == 'Custom' or show_full_alloc_table else cliff_dict['angle']][0],
        'angle_vesting_duration': [angle_duration if vesting_style == 'Custom' or show_full_alloc_table else duration_dict['angle']][0],
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
        'advisor_initial_vesting': [advisor_initial_vesting if vesting_style == 'Custom' or show_full_alloc_table else init_vesting_dict['advisors']][0],
        'advisor_cliff': [advisor_cliff if vesting_style == 'Custom' or show_full_alloc_table else cliff_dict['advisors']][0],
        'advisor_vesting_duration': [advisor_duration if vesting_style == 'Custom' or show_full_alloc_table else duration_dict['advisors']][0],
        'strategic_partners_allocation': strategic_partners_allocation,
        'strategic_partners_initial_vesting': [strategic_partners_initial_vesting if vesting_style == 'Custom' or show_full_alloc_table else init_vesting_dict['strategic_partners']][0],
        'strategic_partners_cliff': [strategic_partners_cliff if vesting_style == 'Custom' or show_full_alloc_table else cliff_dict['strategic_partners']][0],
        'strategic_partner_vesting_duration': [strategic_partners_duration if vesting_style == 'Custom' or show_full_alloc_table else duration_dict['strategic_partners']][0],
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
        'airdrop_date1': [airdrop_date1.strftime('%d.%m.%y') if airdrop_toggle else sys_param['airdrop_date1'][0]][0],
        'airdrop_amount1': [airdrop_amount1 if airdrop_toggle else sys_param['airdrop_amount1'][0]][0],
        'airdrop_date2': [airdrop_date2.strftime('%d.%m.%y') if airdrop_toggle else sys_param['airdrop_date2'][0]][0],
        'airdrop_amount2': [airdrop_amount2 if airdrop_toggle else sys_param['airdrop_amount2'][0]][0],
        'airdrop_date3': [airdrop_date3.strftime('%d.%m.%y') if airdrop_toggle else sys_param['airdrop_date3'][0]][0],
        'airdrop_amount3': [airdrop_amount3 if airdrop_toggle else sys_param['airdrop_amount3'][0]][0],
        'initial_product_users': initial_product_users,
        'initial_token_holders': initial_token_holders,
        'product_users_after_10y': product_users_after_10y,
        'token_holders_after_10y': token_holders_after_10y,
        'product_adoption_velocity': [product_adoption_velocity if adoption_style == 'Custom' or show_full_adoption_table else adoption_dict[adoption_style]['product_adoption_velocity']][0],
        'token_adoption_velocity': [token_adoption_velocity if adoption_style == 'Custom' or show_full_adoption_table else adoption_dict[adoption_style]['token_adoption_velocity']][0],
        'regular_product_revenue_per_user': [regular_product_revenue_per_user if adoption_style == 'Custom' or show_full_adoption_table else adoption_dict[adoption_style]['regular_product_revenue_per_user']][0],
        'regular_token_buy_per_user': [regular_token_buy_per_user if adoption_style == 'Custom' or show_full_adoption_table else adoption_dict[adoption_style]['regular_token_buy_per_user']][0],
        'avg_token_utility_allocation': [avg_token_utility_allocation if adoption_style == 'Custom' or show_full_adoption_table else adoption_dict[adoption_style]['avg_token_utility_allocation']][0],
        'avg_token_selling_allocation': [avg_token_selling_allocation if adoption_style == 'Custom' or show_full_adoption_table else adoption_dict[adoption_style]['avg_token_selling_allocation']][0],
        'avg_token_holding_allocation': [avg_token_holding_allocation if adoption_style == 'Custom' or show_full_adoption_table else adoption_dict[adoption_style]['avg_token_holding_allocation']][0],
        'avg_token_utility_removal': [avg_token_utility_removal if adoption_style == 'Custom' or show_full_adoption_table else adoption_dict[adoption_style]['avg_token_utility_removal']][0],
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
        'buyback_start': buyback_start.strftime('%d.%m.%y'),
        'buyback_end': buyback_end.strftime('%d.%m.%y'),
        'burn_per_month': burn_per_month,
        'burn_bucket': burn_bucket,
        'burn_start': burn_start.strftime('%d.%m.%y'),
        'burn_end': burn_end.strftime('%d.%m.%y'),
    }

    if lp_allocation < 0:
        st.warning(f"The DEX liquidity pool token allocation must be > 0!", icon="⚠️")
        st.session_state['execute_inputs'] = False
    else:
        st.session_state['execute_inputs'] = True
    return new_params