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
        if fundraising_style != 'Custom':
            target_raise = st.number_input('Overall Capital Raise Target / $m', min_value=0.1, max_value=500.0, value=float(sys_param['raised_capital_sum'][0])/1e6, help="The overall capital raise target.")
            left_over_raise = target_raise - equity_investments
        show_full_fund_table = st.toggle('Show Full Table', value=False, help="Show the full token fundraising table.")
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
        else:
            seed_raised = st.number_input('Seed Raises / $m', min_value=0.0, value=float([valuation_weights["seed"]/valuation_weights_sum * left_over_raise if uploaded_file is None and fundraising_style != 'Custom' else float(sys_param['seed_raised'][0]/1e6)][0]), help="The amount of money raised in the seed round.")
            presale_1_raised = st.number_input('Presale 1 Raises / $m', min_value=0.0, value=float([valuation_weights["presale_1"]/valuation_weights_sum * left_over_raise if uploaded_file is None and fundraising_style != 'Custom' else float(sys_param['presale_1_raised'][0]/1e6)][0]), help="The amount of money raised in the first presale.")
            presale_2_raised = st.number_input('Presale 2 Raises / $m', min_value=0.0, value=float([valuation_weights["presale_2"]/valuation_weights_sum * left_over_raise if uploaded_file is None and fundraising_style != 'Custom' else float(sys_param['presale_2_raised'][0]/1e6)][0]), help="The amount of money raised in the second presale.")
            public_sale_raised = st.number_input('Public Sale Raises / $m', min_value=0.0, value=float([valuation_weights["public_sale"]/valuation_weights_sum * left_over_raise if uploaded_file is None and fundraising_style != 'Custom' else float(sys_param['public_sale_raised'][0]/1e6)][0]), help="The amount of money raised in the public sale.")


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
    with col42:
        st.write("Allocation / %")
        if vesting_style == 'Custom' or show_full_alloc_table:
            if equity_perc > 0:
                equity_allocation = (equity_perc/100) * (sys_param['team_allocation'][0]/(1-equity_perc/100))
                st.number_input('', min_value=0.0, value=equity_allocation, disabled=True, key="angle_allocation")
            if seed_raised > 0:
                st.number_input('', min_value=0.0, value=((seed_raised*1e6) / ((seed_valuation*1e6)/initial_supply) / initial_supply) * 1e2, disabled=True, key="seed_allocation")
            if presale_1_raised > 0:
                st.number_input('', min_value=0.0, value=((presale_1_raised*1e6) / ((presale_1_valuation*1e6)/initial_supply) / initial_supply) * 1e2, disabled=True, key="presale_1_allocation")
            if presale_2_raised > 0:
                st.number_input('', min_value=0.0, value=((presale_2_raised*1e6) / ((presale_2_valuation*1e6)/initial_supply) / initial_supply) * 1e2, disabled=True, key="presale_2_allocation")   
            if public_sale_raised > 0:
                st.number_input('', min_value=0.0, value=((public_sale_raised*1e6) / ((launch_valuation*1e6)/initial_supply) / initial_supply) * 1e2, disabled=True, key="public_sale_allocation")
            
    with col43:
        st.write("Initial Vesting / %")
        if vesting_style == 'Slow':
            angle_initial_vesting, seed_initial_vesting, presale_1_initial_vesting, presale_2_initial_vesting, public_sale_initial_vesting = 0.0, 0.0, 0.0, 0.0, 10.0
        if vesting_style == 'Medium':
            angle_initial_vesting, seed_initial_vesting, presale_1_initial_vesting, presale_2_initial_vesting, public_sale_initial_vesting = 0.0, 0.0, 0.0, 5.0, 15.0
        if vesting_style == 'Fast':
            angle_initial_vesting, seed_initial_vesting, presale_1_initial_vesting, presale_2_initial_vesting, public_sale_initial_vesting = 0.0, 0.0, 5.0, 15.0, 35.0
        if vesting_style == 'Custom' or show_full_alloc_table:
            angle_initial_vesting = [st.number_input("", min_value=0.0, value=[sys_param['angle_initial_vesting'][0] if vesting_style == 'Custom' else angle_initial_vesting][0], key="angle_initial_vesting") if equity_perc > 0 else 0.0][0]
            seed_initial_vesting = [st.number_input("", min_value=0.0, value=[sys_param['seed_initial_vesting'][0] if vesting_style == 'Custom' else seed_initial_vesting][0], key="seed_initial_vesting") if seed_raised > 0 else 0.0][0]
            presale_1_initial_vesting = [st.number_input("", min_value=0.0, value=[sys_param['presale_1_initial_vesting'][0] if vesting_style == 'Custom' else presale_1_initial_vesting][0], key="presale_1_initial_vesting") if presale_1_raised > 0 else 0.0][0] 
            presale_2_initial_vesting = [st.number_input("", min_value=0.0, value=[sys_param['presale_2_initial_vesting'][0] if vesting_style == 'Custom' else presale_2_initial_vesting][0], key="presale_2_initial_vesting") if presale_2_raised > 0 else 0.0][0]  
            public_sale_initial_vesting = [st.number_input("", min_value=0.0, value=[sys_param['public_sale_initial_vesting'][0] if vesting_style == 'Custom' else public_sale_initial_vesting][0], key="public_sale_initial_vesting") if public_sale_raised > 0 else 0.0][0]

    with col44:
        st.write("Cliff / Months")
        if vesting_style == 'Slow':
            angle_cliff, seed_cliff, presale_1_cliff, presale_2_cliff, public_sale_cliff = 18, 12, 9, 6, 3
        if vesting_style == 'Medium':
            angle_cliff, seed_cliff, presale_1_cliff, presale_2_cliff, public_sale_cliff = 12, 9, 6, 3, 0
        if vesting_style == 'Fast':
            angle_cliff, seed_cliff, presale_1_cliff, presale_2_cliff, public_sale_cliff = 9, 6, 6, 3, 0
        if vesting_style == 'Custom' or show_full_alloc_table:
            angle_cliff = [st.number_input("", min_value=0, value=int([sys_param['angle_cliff'][0] if vesting_style == 'Custom' else angle_cliff][0]), key="angle_cliff") if equity_perc > 0 else 0.0][0]
            seed_cliff = [st.number_input("", min_value=0, value=int([sys_param['seed_cliff'][0] if vesting_style == 'Custom' else seed_cliff][0]), key="seed_cliff") if seed_raised > 0 else 0.0][0]
            presale_1_cliff = [st.number_input("", min_value=0, value=int([sys_param['presale_1_cliff'][0] if vesting_style == 'Custom' else presale_1_cliff][0]), key="presale_1_cliff") if presale_1_raised > 0 else 0.0][0]
            presale_2_cliff = [st.number_input("", min_value=0, value=int([sys_param['presale_2_cliff'][0] if vesting_style == 'Custom' else presale_2_cliff][0]), key="presale_2_cliff") if presale_2_raised > 0 else 0.0][0]
            public_sale_cliff = [st.number_input("", min_value=0, value=int([sys_param['public_sale_cliff'][0] if vesting_style == 'Custom' else public_sale_cliff][0]), key="public_sale_cliff") if public_sale_raised > 0 else 0.0][0]
            
    with col45:
        st.write("Duration / Months")
        if vesting_style == 'Slow':
            angle_duration, seed_duration, presale_1_duration, presale_2_duration, public_sale_duration = 6*12, 4*12, 3*12, 2*12, 1*12
        if vesting_style == 'Medium':
            angle_duration, seed_duration, presale_1_duration, presale_2_duration, public_sale_duration = 4*12, 3*12, 2*12, 1*12, 6
        if vesting_style == 'Fast':
            angle_duration, seed_duration, presale_1_duration, presale_2_duration, public_sale_duration = 2*12, 2*12, 1*12, 6, 3
        if vesting_style == 'Custom' or show_full_alloc_table:
            angle_duration = [st.number_input("", min_value=0, value=int([sys_param['angle_vesting_duration'][0] if vesting_style == 'Custom' else angle_duration][0]), key="angle_vesting_duration") if equity_perc > 0 else 0.0][0]
            seed_duration = [st.number_input("", min_value=0, value=int([sys_param['seed_vesting_duration'][0] if vesting_style == 'Custom' else seed_duration][0]), key="seed_vesting_duration") if seed_raised > 0 else 0.0][0]
            presale_1_duration = [st.number_input("", min_value=0, value=int([sys_param['presale_1_vesting_duration'][0] if vesting_style == 'Custom' else presale_1_duration][0]), key="presale_1_vesting_duration") if presale_1_raised > 0 else 0.0][0]
            presale_2_duration = [st.number_input("", min_value=0, value=int([sys_param['presale_2_vesting_duration'][0] if vesting_style == 'Custom' else presale_2_duration][0]), key="presale_2_vesting_duration") if presale_2_raised > 0 else 0.0][0]
            public_sale_duration = [st.number_input("", min_value=0, value=int([sys_param['public_sale_vesting_duration'][0] if vesting_style == 'Custom' else public_sale_duration][0]), key="public_sale_vesting_duration") if public_sale_raised > 0 else 0.0][0]

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
        'angle_initial_vesting': angle_initial_vesting,
        'angle_cliff': angle_cliff,
        'angle_vesting_duration': angle_duration,
        'seed_initial_vesting': seed_initial_vesting,
        'seed_cliff': seed_cliff,
        'seed_vesting_duration': seed_duration,
        'presale_1_initial_vesting': presale_1_initial_vesting,
        'presale_1_cliff': presale_1_cliff,
        'presale_1_vesting_duration': presale_1_duration,
        'presale_2_initial_vesting': presale_2_initial_vesting,
        'presale_2_cliff': presale_2_cliff,
        'presale_2_vesting_duration': presale_2_duration,
        'public_sale_initial_vesting': public_sale_initial_vesting,
        'public_sale_cliff': public_sale_cliff,
        'public_sale_vesting_duration': public_sale_duration,
    }

    return new_params