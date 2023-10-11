import streamlit as st
from plots import *
from Model.parts.utils import *

fundraising_style_map = {
    'Moderate': 2,
    'Medium': 5,
    'Aggressive': 10
}

param_help = {
    'fundraising_style': f"The more aggressive the fundraising style, the more advantageous it is to be an early investor: **Moderate** / **Medium** / **Aggressive** : **{fundraising_style_map['Moderate']}x** / **{fundraising_style_map['Medium']}x** / **{fundraising_style_map['Aggressive']}x** public sale to seed round valuation ratio.",
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
        initial_supply = st.number_input('Initial Total Token Supply', min_value=100, max_value=1000000000000, value=int(sys_param['initial_total_supply'][0]), help="The initial total token supply.")
    with col12:
        public_sale_supply = st.number_input('Public Sale Supply / %', min_value=0.0, max_value=95.0, value=float(str(sys_param['public_sale_supply_perc'][0]).split("%")[0]), help="The percentage of tokens sold in the public sale.")
        equity_investments = st.number_input('Angle & Equity Raises / $m', min_value=0.01, value=float(sys_param['angle_raised'][0]/1e6), help="The amount of money raised from equity investors.")
    with col13:
        launch_valuation = st.number_input('Public Sale Valuation / $m', min_value=5, max_value=500, value=int(sys_param['public_sale_valuation'][0]/1e6), help="The valuation of the public sale.")
        equity_perc = st.number_input('Equity sold / %', min_value=0.0, max_value=90.0, value=float(str(sys_param['equity_external_shareholders_perc'][0]).split("%")[0]), help="The percentage of equity sold to external shareholders.")
    
    st.markdown("### Fundraising")
    col21, col22, col23 = st.columns(3)
    with col21:
        fundraising_style = st.radio('Fundraising Style',('Moderate', 'Medium', 'Aggressive','Custom'), index=0, help=param_help['fundraising_style'])
        if fundraising_style != 'Custom':
            target_raise = st.number_input('Overall Capital Raise Target / $m', min_value=0.1, max_value=500.0, value=float(sys_param['raised_capital_sum'][0])/1e6, help="The overall capital raise target.")
            left_over_raise = target_raise - equity_investments
    with col23:
        seed_valuation = st.number_input('Seed Valuation / $m', min_value=0.01, value=float([np.linspace(launch_valuation/fundraising_style_map[fundraising_style], launch_valuation, 4)[0] if uploaded_file is None and fundraising_style != 'Custom' and parameter_id_choice == "" else float(sys_param['seed_valuation'][0]/1e6)][0]), help="The valuation of the seed round.")
        presale_1_valuation = st.number_input('Presale 1 Valuation / $m', min_value=0.01, value=float([np.linspace(launch_valuation/fundraising_style_map[fundraising_style], launch_valuation, 4)[1] if uploaded_file is None and fundraising_style != 'Custom' and parameter_id_choice == "" else float(sys_param['presale_1_valuation'][0]/1e6)][0]), help="The valuation of the first presale.")
        presale_2_valuation = st.number_input('Presale 2 Valuation / $m', min_value=0.01, value=float([np.linspace(launch_valuation/fundraising_style_map[fundraising_style], launch_valuation, 4)[2] if uploaded_file is None and fundraising_style != 'Custom' and parameter_id_choice == "" else float(sys_param['presale_2_valuation'][0]/1e6)][0]), help="The valuation of the second presale.")
    with col22:
        if fundraising_style != 'Custom':
            if parameter_id_choice != "":
                st.markdown(f"Parameter ID {parameter_id_choice} was given.")
                st.markdown(f"Hence no changes to the fundraising style are possible.")
                st.markdown(f"Please choose 'Custom' to adjust the fundraising style manually.")
            
            valuation_weights = {
                "seed" : seed_valuation / launch_valuation,
                "presale_1" : presale_1_valuation / launch_valuation,
                "presale_2" : presale_2_valuation / launch_valuation,
                "public_sale" : 1.0
            }
            valuation_weights_sum = sum(valuation_weights.values())

            seed_raised = float(valuation_weights["seed"]/valuation_weights_sum * left_over_raise)
            presale_1_raised = float(valuation_weights["presale_1"]/valuation_weights_sum * left_over_raise)
            presale_2_raised = float(valuation_weights["presale_2"]/valuation_weights_sum * left_over_raise)
            public_sale_raised = float(valuation_weights["public_sale"]/valuation_weights_sum * left_over_raise)
        else:
            seed_raised = st.number_input('Seed Raises / $m', min_value=0.0, value=float([left_over_raise/4 if uploaded_file is None and fundraising_style != 'Custom' and parameter_id_choice == "" else float(sys_param['seed_raised'][0]/1e6)][0]), help="The amount of money raised in the seed round.")
            presale_1_raised = st.number_input('Presale 1 Raises / $m', min_value=0.0, value=float([left_over_raise/4 if uploaded_file is None and fundraising_style != 'Custom' and parameter_id_choice == "" else float(sys_param['presale_1_raised'][0]/1e6)][0]), help="The amount of money raised in the first presale.")
            presale_2_raised = st.number_input('Presale 2 Raises / $m', min_value=0.0, value=float([left_over_raise/4 if uploaded_file is None and fundraising_style != 'Custom' and parameter_id_choice == "" else float(sys_param['presale_2_raised'][0]/1e6)][0]), help="The amount of money raised in the second presale.")
            public_sale_raised = st.number_input('Public Sale Raises / $m', min_value=0.0, value=float([left_over_raise/4 if uploaded_file is None and fundraising_style != 'Custom' and parameter_id_choice == "" else float(sys_param['public_sale_raised'][0]/1e6)][0]), help="The amount of money raised in the public sale.")


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
    }

    return new_params