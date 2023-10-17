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
        initial_supply = st.number_input('Initial Total Token Supply', min_value=100, max_value=1000000000000, value=int(sys_param['initial_total_supply'][0]), help="The initial total token supply.")
    with col12:
        launch_valuation = st.number_input('Public Sale Valuation / $m', min_value=5, max_value=500, value=int(sys_param['public_sale_valuation'][0]/1e6), help="This is the valuation at which the public sale tokens are sold. It is equivalent to the token launch valuation.")
        public_sale_supply = st.number_input('Public Sale Supply / %', min_value=0.0, max_value=95.0, value=float(str(sys_param['public_sale_supply_perc'][0]).split("%")[0]), help="The percentage of tokens sold in the public sale.")
        st.write("Launch Price: "+ str(launch_valuation*1e6/initial_supply)+" $/token")
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
        show_full_fund_table = st.toggle('Show Full Table', value=False, help="Show the full token fundraising table.")
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
        show_full_alloc_table = st.toggle('Show Full Table', value=False, help="Show the full token allocation and vesting table.")
    with col32:
        incentivisation_toggle = st.toggle('Incentivisation Vesting', value=sys_param['incentivisation_allocation'][0] > 0.0, help=param_help['incentivisation'])
        staking_vesting_toggle = st.toggle('Staking Vesting', value=sys_param['staking_vesting_allocation'][0] > 0.0, help=param_help['staking_vesting'])
        airdrop_toggle = st.toggle('Airdrops', value=sys_param['airdrop_allocation'][0] > 0.0, help=param_help['airdrops'])

    col41, col42, col43, col44, col45 = st.columns(5)
    with col41:
        st.write("Name")
        if vesting_style == 'Custom' or show_full_alloc_table:
            if equity_perc > 0:
                st.text_input("","Angle",disabled=True, key="angle_name")
            if seed_raised > 0:
                st.text_input("","Seed",disabled=True, key="seed_name")
            if presale_1_raised > 0:
                st.text_input("","Presale 1",disabled=True, key="presale_1_name")
            if presale_2_raised > 0:    
                st.text_input("","Presale 2",disabled=True, key="presale_2_name")
            if public_sale_raised > 0:    
                st.text_input("","Public Sale",disabled=True, key="public_sale_name")
            st.text_input("","Team",disabled=True, key="team_name")
            st.text_input("","Advisors",disabled=True, key="advisors_name")
            st.text_input("","Strat. Partners",disabled=True, key="partners_name")
            st.text_input("","Reserve",disabled=True, key="reserve_name")
            st.text_input("","Community",disabled=True, key="community_name")
            st.text_input("","Foundation",disabled=True, key="foundation_name")
            if incentivisation_toggle:
                st.text_input("","Incentivisation",disabled=True, key="incentivisation_name")
            if staking_vesting_toggle:
                st.text_input("","Staking Vesting",disabled=True, key="staking_vesting_name")
            if airdrop_toggle:
                st.markdown("""---""")
                st.text_input("","Airdrops",disabled=True, key="airdrops_name")
                st.write('')
            st.markdown("""---""")
            st.text_input("","DEX LP",disabled=True, key="lp_name")
    with col42:
        st.write("Allocation / %")
        if vesting_style == 'Custom' or show_full_alloc_table:
            equity_allocation = (equity_perc/100) * (sys_param['team_allocation'][0]/(1-equity_perc/100))
            if equity_perc > 0:
                equity_allocation_new = st.number_input('', min_value=0.0, value=equity_allocation, disabled=True, key="angle_allocation")
            else:
                equity_allocation_new = 0.0
            if seed_raised > 0:
                seed_allocation = st.number_input('', min_value=0.0, value=((seed_raised*1e6) / ((seed_valuation*1e6)/initial_supply) / initial_supply) * 1e2, disabled=True, key="seed_allocation")
            else:
                seed_allocation = 0.0
            if presale_1_raised > 0:
                presale_1_allocation = st.number_input('', min_value=0.0, value=((presale_1_raised*1e6) / ((presale_1_valuation*1e6)/initial_supply) / initial_supply) * 1e2, disabled=True, key="presale_1_allocation")
            else:
                presale_1_allocation = 0.0
            if presale_2_raised > 0:
                presale_2_allocation = st.number_input('', min_value=0.0, value=((presale_2_raised*1e6) / ((presale_2_valuation*1e6)/initial_supply) / initial_supply) * 1e2, disabled=True, key="presale_2_allocation")   
            else:
                presale_2_allocation = 0.0
            if public_sale_raised > 0:
                public_sale_allocation = st.number_input('', min_value=0.0, value=((public_sale_raised*1e6) / ((launch_valuation*1e6)/initial_supply) / initial_supply) * 1e2, disabled=True, key="public_sale_allocation")
            else:
                public_sale_allocation = 0.0
            team_allocation = st.number_input('', min_value=0.0, value=sys_param['team_allocation'][0], disabled=False, key="team_allocation")
            ov_advisor_allocation = st.number_input('', min_value=0.0, value=sys_param['ov_allocation'][0]+sys_param['advisor_allocation'][0], disabled=False, key="ov_advisor_allocation")
            strategic_partners_allocation = st.number_input('', min_value=0.0, value=sys_param['strategic_partners_allocation'][0], disabled=False, key="partner_allocation")
            reserve_allocation = st.number_input('', min_value=0.0, value=sys_param['reserve_allocation'][0], disabled=False, key="reserve_allocation")
            community_allocation = st.number_input('', min_value=0.0, value=sys_param['community_allocation'][0], disabled=False, key="community_allocation")
            foundation_allocation = st.number_input('', min_value=0.0, value=sys_param['foundation_allocation'][0], disabled=False, key="foundation_allocation")
            if incentivisation_toggle:
                incentivisation_allocation = st.number_input('', min_value=0.0, value=sys_param['incentivisation_allocation'][0], disabled=False, key="incentivisation_allocation")
            else:
                incentivisation_allocation = 0.0
            if staking_vesting_toggle:
                staking_vesting_allocation = st.number_input('', min_value=0.0, value=sys_param['staking_vesting_allocation'][0], disabled=False, key="staking_vesting_allocation")
            else:
                staking_vesting_allocation = 0.0
            if airdrop_toggle:
                st.markdown("""---""")
                airdrop_allocation = st.number_input('', min_value=0.0, value=sys_param['airdrop_allocation'][0], disabled=False, key="airdrop_allocation")
            else:
                airdrop_allocation = 0.0
            lp_allocation = (100 - equity_allocation_new - seed_allocation - presale_1_allocation
                             - presale_2_allocation - public_sale_allocation - team_allocation - ov_advisor_allocation
                             - strategic_partners_allocation - reserve_allocation - community_allocation
                             - foundation_allocation - incentivisation_allocation - staking_vesting_allocation
                             - airdrop_allocation)
            st.write('')
            st.markdown("""---""")
            st.number_input('', value=lp_allocation, disabled=True, key="lp_allocation", help="The percentage of tokens allocated to the liquidity pool. This is the remaining percentage of tokens after all other allocations have been made. It must not be < 0 and determines the required capital to seed the liquidity: lp_allocation x total_initial_supply / 100 % * token_launch_price.")
        else:
            equity_allocation_new = (equity_perc/100) * (sys_param['team_allocation'][0]/(1-equity_perc/100))
            seed_allocation = ((seed_raised*1e6) / ((seed_valuation*1e6)/initial_supply) / initial_supply) * 1e2
            presale_1_allocation = ((presale_1_raised*1e6) / ((presale_1_valuation*1e6)/initial_supply) / initial_supply) * 1e2
            presale_2_allocation = ((presale_2_raised*1e6) / ((presale_2_valuation*1e6)/initial_supply) / initial_supply) * 1e2
            public_sale_allocation = ((public_sale_raised*1e6) / ((launch_valuation*1e6)/initial_supply) / initial_supply) * 1e2
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
        st.write("Init. Vesting / %")
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
            if equity_perc > 0:
                angle_initial_vesting = st.number_input("", min_value=0.0, value=[sys_param['angle_initial_vesting'][0] if vesting_style == 'Custom' else init_vesting_dict['angle']][0], key="angle_initial_vesting")
            else:
                angle_initial_vesting = 0.0
            if seed_raised > 0:
                seed_initial_vesting = st.number_input("", min_value=0.0, value=[sys_param['seed_initial_vesting'][0] if vesting_style == 'Custom' else init_vesting_dict['seed']][0], key="seed_initial_vesting")
            else:
                seed_initial_vesting = 0.0
            if presale_1_raised > 0:
                presale_1_initial_vesting = st.number_input("", min_value=0.0, value=[sys_param['presale_1_initial_vesting'][0] if vesting_style == 'Custom' else init_vesting_dict['presale_1']][0], key="presale_1_initial_vesting")
            else:
                presale_1_initial_vesting = 0.0
            if presale_2_raised > 0:
                presale_2_initial_vesting = st.number_input("", min_value=0.0, value=[sys_param['presale_2_initial_vesting'][0] if vesting_style == 'Custom' else init_vesting_dict['presale_2']][0], key="presale_2_initial_vesting")
            else:
                presale_2_initial_vesting = 0.0
            if public_sale_raised > 0:
                public_sale_initial_vesting = st.number_input("", min_value=0.0, value=[sys_param['public_sale_initial_vesting'][0] if vesting_style == 'Custom' else init_vesting_dict['public_sale']][0], key="public_sale_initial_vesting")
            else:
                public_sale_initial_vesting = 0.0
            team_initial_vesting = st.number_input("", min_value=0.0, value=[sys_param['team_initial_vesting'][0] if vesting_style == 'Custom' else init_vesting_dict['team']][0], key="team_initial_vesting")
            advisor_initial_vesting = st.number_input("", min_value=0.0, value=[(sys_param['ov_initial_vesting'][0]+sys_param['advisor_initial_vesting'][0])/2 if vesting_style == 'Custom' else init_vesting_dict['advisors']][0], key="advisor_initial_vesting")
            strategic_partners_initial_vesting = st.number_input("", min_value=0.0, value=[sys_param['strategic_partners_initial_vesting'][0] if vesting_style == 'Custom' else init_vesting_dict['strategic_partners']][0], key="strategic_partners_initial_vesting")
            reserve_initial_vesting = st.number_input("", min_value=0.0, value=[sys_param['reserve_initial_vesting'][0] if vesting_style == 'Custom' else init_vesting_dict['reserve']][0], key="reserve_initial_vesting")
            community_initial_vesting = st.number_input("", min_value=0.0, value=[sys_param['community_initial_vesting'][0] if vesting_style == 'Custom' else init_vesting_dict['community']][0], key="community_initial_vesting")
            foundation_initial_vesting = st.number_input("", min_value=0.0, value=[sys_param['foundation_initial_vesting'][0] if vesting_style == 'Custom' else init_vesting_dict['foundation']][0], key="foundation_initial_vesting")
            if incentivisation_toggle:
                incentivisation_initial_vesting = st.number_input("", min_value=0.0, value=[sys_param['incentivisation_initial_vesting'][0] if vesting_style == 'Custom' else init_vesting_dict['incentivisation']][0], key="incentivisation_initial_vesting")
            else:
                incentivisation_initial_vesting = 0.0
            if staking_vesting_toggle:
                staking_vesting_initial_vesting = st.number_input("", min_value=0.0, value=[sys_param['staking_vesting_initial_vesting'][0] if vesting_style == 'Custom' else init_vesting_dict['staking_vesting']][0], key="staking_vesting_initial_vesting")
            else:
                staking_vesting_initial_vesting = 0.0
            if airdrop_toggle:
                st.markdown("""---""")
                airdrop_date1 = st.date_input("Airdrop Date 1", min_value=datetime.strptime(sys_param['launch_date'][0], "%d.%m.%y"), value=datetime.strptime(sys_param['airdrop_date1'][0], "%d.%m.%y"), help="The date of the first airdrop.")
                airdrop_amount1 = st.number_input("Amount 1 / %", min_value=0.0, value=sys_param['airdrop_amount1'][0], help="The share of tokens distributed from the airdrop allocation in the first airdrop.")
                st.number_input('DEX Capital / $m', max_value=raised_funds,value=float((lp_allocation/100 )* initial_supply * launch_valuation*1e6 / initial_supply/1e6), disabled=True, key="liquidity_capital_requirements")


    with col44:
        st.write("Cliff / Mon.")
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
            if equity_perc > 0:
                angle_cliff = st.number_input("", min_value=0, value=int([sys_param['angle_cliff'][0] if vesting_style == 'Custom' else cliff_dict['angle']][0]), key="angle_cliff")
            else:
                angle_cliff = 0.0
            if seed_raised > 0:
                seed_cliff = st.number_input("", min_value=0, value=int([sys_param['seed_cliff'][0] if vesting_style == 'Custom' else cliff_dict['seed']][0]), key="seed_cliff")
            else:
                seed_cliff = 0.0
            if presale_1_raised:
                presale_1_cliff = st.number_input("", min_value=0, value=int([sys_param['presale_1_cliff'][0] if vesting_style == 'Custom' else cliff_dict['presale_1']][0]), key="presale_1_cliff")
            else:
                presale_1_cliff = 0.0
            if presale_2_raised > 0:
                presale_2_cliff = st.number_input("", min_value=0, value=int([sys_param['presale_2_cliff'][0] if vesting_style == 'Custom' else cliff_dict['presale_2']][0]), key="presale_2_cliff")
            else:
                presale_2_cliff = 0.0
            if public_sale_raised > 0:
                public_sale_cliff = st.number_input("", min_value=0, value=int([sys_param['public_sale_cliff'][0] if vesting_style == 'Custom' else cliff_dict['public_sale']][0]), key="public_sale_cliff")
            else:
                public_sale_cliff = 0.0
            team_cliff = st.number_input("", min_value=0, value=int([sys_param['team_cliff'][0] if vesting_style == 'Custom' else cliff_dict['team']][0]), key="team_cliff")
            advisor_cliff = st.number_input("", min_value=0, value=int([sys_param['advisor_cliff'][0] if vesting_style == 'Custom' else cliff_dict['advisors']][0]), key="advisor_cliff")
            strategic_partners_cliff = st.number_input("", min_value=0, value=int([sys_param['strategic_partners_cliff'][0] if vesting_style == 'Custom' else cliff_dict['strategic_partners']][0]), key="strategic_partners_cliff")
            reserve_cliff = st.number_input("", min_value=0, value=int([sys_param['reserve_cliff'][0] if vesting_style == 'Custom' else cliff_dict['reserve']][0]), key="reserve_cliff")
            community_cliff = st.number_input("", min_value=0, value=int([sys_param['community_cliff'][0] if vesting_style == 'Custom' else cliff_dict['community']][0]), key="community_cliff")
            foundation_cliff = st.number_input("", min_value=0, value=int([sys_param['foundation_cliff'][0] if vesting_style == 'Custom' else cliff_dict['foundation']][0]), key="foundation_cliff")
            if incentivisation_toggle:
                incentivisation_cliff = st.number_input("", min_value=0, value=int([sys_param['incentivisation_cliff'][0] if vesting_style == 'Custom' else cliff_dict['incentivisation']][0]), key="incentivisation_cliff")
            else:
                incentivisation_cliff = 0.0
            if staking_vesting_toggle:
                staking_vesting_cliff = st.number_input("", min_value=0, value=int([sys_param['staking_vesting_cliff'][0] if vesting_style == 'Custom' else cliff_dict['staking_vesting']][0]), key="staking_vesting_cliff")
            else:
                staking_vesting_cliff = 0.0
            if airdrop_toggle:
                st.markdown("""---""")                
                airdrop_date2 = st.date_input("Airdrop Date 2", min_value=datetime.strptime(sys_param['launch_date'][0], "%d.%m.%y"), value=datetime.strptime(sys_param['airdrop_date2'][0], "%d.%m.%y"), help="The date of the second airdrop.")
                airdrop_amount2 = st.number_input("Amount 2 / %", min_value=0.0, value=sys_param['airdrop_amount2'][0], help="The share of tokens distributed from the airdrop allocation in the second airdrop.")
                st.markdown("""---""")
  
    with col45:
        st.write("Duration / Mon.")
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
            if equity_perc > 0:
                angle_duration = st.number_input("", min_value=0, value=int([sys_param['angle_vesting_duration'][0] if vesting_style == 'Custom' else duration_dict['angle']][0]), key="angle_vesting_duration")
            else:
                angle_duration = 0.0
            if seed_raised > 0:
                seed_duration = st.number_input("", min_value=0, value=int([sys_param['seed_vesting_duration'][0] if vesting_style == 'Custom' else duration_dict['seed']][0]), key="seed_vesting_duration")
            else:
                seed_duration = 0.0
            if presale_1_raised > 0:
                presale_1_duration = st.number_input("", min_value=0, value=int([sys_param['presale_1_vesting_duration'][0] if vesting_style == 'Custom' else duration_dict['presale_1']][0]), key="presale_1_vesting_duration")
            else:
                presale_1_duration = 0.0
            if presale_2_raised > 0:
                presale_2_duration = st.number_input("", min_value=0, value=int([sys_param['presale_2_vesting_duration'][0] if vesting_style == 'Custom' else duration_dict['presale_2']][0]), key="presale_2_vesting_duration")
            else:
                presale_2_duration = 0.0
            if public_sale_raised > 0:
                public_sale_duration = st.number_input("", min_value=0, value=int([sys_param['public_sale_vesting_duration'][0] if vesting_style == 'Custom' else duration_dict['public_sale']][0]), key="public_sale_vesting_duration")
            else:
                public_sale_duration = 0.0
            team_duration = st.number_input("", min_value=0, value=int([sys_param['team_vesting_duration'][0] if vesting_style == 'Custom' else duration_dict['team']][0]), key="team_vesting_duration")
            advisor_duration = st.number_input("", min_value=0, value=int([(sys_param['advisor_vesting_duration'][0] + sys_param['ov_vesting_duration'][0])/2 if vesting_style == 'Custom' else duration_dict['advisors']][0]), key="advisor_vesting_duration")
            strategic_partners_duration = st.number_input("", min_value=0, value=int([sys_param['strategic_partner_vesting_duration'][0] if vesting_style == 'Custom' else duration_dict['strategic_partners']][0]), key="strategic_partners_vesting_duration")
            reserve_duration = st.number_input("", min_value=0, value=int([sys_param['reserve_vesting_duration'][0] if vesting_style == 'Custom' else duration_dict['reserve']][0]), key="reserve_vesting_duration")
            community_duration = st.number_input("", min_value=0, value=int([sys_param['community_vesting_duration'][0] if vesting_style == 'Custom' else duration_dict['community']][0]), key="community_vesting_duration")
            foundation_duration = st.number_input("", min_value=0, value=int([sys_param['foundation_vesting_duration'][0] if vesting_style == 'Custom' else duration_dict['foundation']][0]), key="foundation_vesting_duration")
            if incentivisation_toggle:
                incentivisation_duration = st.number_input("", min_value=0, value=int([sys_param['incentivisation_vesting_duration'][0] if vesting_style == 'Custom' else duration_dict['incentivisation']][0]), key="incentivisation_vesting_duration")
            else:
                incentivisation_duration = 0.0
            if staking_vesting_toggle:
                staking_vesting_duration = st.number_input("", min_value=0, value=int([sys_param['staking_vesting_vesting_duration'][0] if vesting_style == 'Custom' else duration_dict['staking_vesting']][0]), key="staking_vesting_vesting_duration")
            else:
                staking_vesting_duration = 0.0
            if airdrop_toggle:
                st.markdown("""---""")
                airdrop_date3 = st.date_input("Airdrop Date 3", min_value=datetime.strptime(sys_param['launch_date'][0], "%d.%m.%y"), value=datetime.strptime(sys_param['airdrop_date3'][0], "%d.%m.%y"), help="The date of the third airdrop.")
                airdrop_amount3 = st.number_input("Amount 3 / %", min_value=0.0, value=sys_param['airdrop_amount3'][0], help="The share of tokens distributed from the airdrop allocation in the third airdrop.")
                st.markdown("""---""")

    # Map new parameters to model input parameters
    new_params = {
        'equity_external_shareholders_perc': equity_perc,
        'supply_type': supply_type,
        'initial_total_supply': initial_supply,
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
        'airdrop_amount3': [airdrop_amount3 if airdrop_toggle else sys_param['airdrop_amount3'][0]][0]
    }

    if lp_allocation < 0:
        st.warning(f"The DEX liquidity pool token allocation must be > 0!", icon="⚠️")
        st.session_state['execute_inputs'] = False
    else:
        st.session_state['execute_inputs'] = True
    return new_params