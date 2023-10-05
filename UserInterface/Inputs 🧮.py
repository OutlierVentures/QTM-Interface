import streamlit as st
import pandas as pd
import numpy as np
import os, sys

# Get the current directory
current_dir = os.path.dirname(os.path.abspath(__file__))
# Go up one folder
parent_dir = os.path.abspath(os.path.join(current_dir, os.pardir))
# Append the parent directory to sys.path
sys.path.append(parent_dir)
from plots import *
from Model.simulation import simulation
from Model.parts.utils import *
from data.not_iterable_variables import parameter_list

input_file_base_path = parent_dir+'/data/'

# set the seed multiples over the public sale valuation
fundraising_style_map = {
    'Moderate': 2,
    'Medium': 5,
    'Aggressive': 10
}

st.title('Quantitative Token Model')
st.markdown("## Inputs 🧮")
st.sidebar.markdown("## Inputs 🧮")
st.sidebar.markdown("Parameter input section for the Quantitative Token Model. Use the default parameters, customize them in the user interface, or upload your own input file based on the radCAD_inputs tab in the [spreadsheet QTM](https://drive.google.com/drive/folders/1eSgm4NA1Izx9qhXd6sdveUKF5VFHY6py?usp=sharing).")

# Upload Input File
with st.expander("Upload Own Input File"):
    st.markdown("### Load Input File 📂")
    st.markdown("Use the default input file or upload your own based on the")
    st.markdown("[Spreadsheet QTM](https://drive.google.com/drive/folders/1eSgm4NA1Izx9qhXd6sdveUKF5VFHY6py?usp=sharing) ➡️ navigate to radCAD_inputs tab ➡️ save it as .csv and then upload it here ⬇️")
    uploaded_file = st.file_uploader("Choose a file")

st.markdown("### Basic Token Information")


def model_ui_inputs(input_file_path, parameter_list):
    col11, col12, col13 = st.columns(3)
    # Adjusting Parameters
    sys_param = compose_initial_parameters(pd.read_csv(input_file_path), parameter_list)
    with col11:
        supply_type = st.radio('Supply Type',('Fixed', 'Inflationary'), index=['Fixed', 'Inflationary'].index(sys_param['supply_type'][0]))
    with col12:
        initial_supply = st.number_input('Initial Total Token Supply', min_value=100000, max_value=1000000000000, value=int(sys_param['initial_total_supply'][0]))
        equity_perc = st.number_input('Equity sold to external Stakeholders / %', min_value=0.0, max_value=90.0, value=float(str(sys_param['equity_external_shareholders_perc'][0]).split("%")[0]))
    with col13:
        launch_valuation = st.number_input('Public Sale Valuation / $m', min_value=5, max_value=500, value=int(sys_param['public_sale_valuation'][0]/1e6))
        public_sale_supply = st.number_input('Public Sale Supply / %', min_value=0.0, max_value=95.0, value=float(str(sys_param['public_sale_supply_perc'][0]).split("%")[0]))
    
    st.markdown("### Fundraising")
    if uploaded_file is None:
        col21, col22, col23 = st.columns(3)
        with col21:
            fundraising_style = st.radio('Fundraising Style',('Moderate', 'Medium', 'Aggressive'), index=0)
        with col22:
            target_raise = st.number_input('Overall Capital Raise Target / $m', min_value=0.1, max_value=500.0, value=float(sys_param['raised_capital_sum'][0])/1e6)
            equity_investments = st.number_input('Angle & Equity Raises / $m', min_value=0.01, max_value=target_raise, value=float(sys_param['angle_raised'][0]/1e6))
    else:
        fundraising_style = 'Moderate'
        target_raise = float(sys_param['raised_capital_sum'][0])/1e6
        equity_investments = st.number_input('Angle & Equity Raises / $m', min_value=0.01, max_value=target_raise, value=float(sys_param['angle_raised'][0]/1e6))
    
    left_over_raise = target_raise - equity_investments
    if uploaded_file is None:
        with st.expander("Fundraising Style Explanation"):
            st.markdown("The more aggressive the fundraising style, the more advantageous it is to be an early investor.")
            st.markdown(f"**Moderate:** Public Sale valuation is {fundraising_style_map['Moderate']}x the valuation of the seed round.")
            st.markdown(f"**Medium:** Public Sale valuation is {fundraising_style_map['Medium']}x the valuation of the seed round.")
            st.markdown(f"**Aggressive:** Public Sale valuation is {fundraising_style_map['Aggressive']}x the valuation of the seed round.")

    # Map new parameters to model input parameters
    new_params = {
        'equity_external_shareholders_perc': equity_perc,
        'supply_type': supply_type,
        'initial_total_supply': initial_supply,
        'public_sale_supply_perc': public_sale_supply,
        'public_sale_valuation': launch_valuation * 1e6,
        'angle_raised': equity_investments * 1e6,
        'seed_raised': [left_over_raise/4 * 1e6 if uploaded_file is None else float(sys_param['seed_raised'][0])][0],
        'presale_1_raised': [left_over_raise/4 * 1e6 if uploaded_file is None else float(sys_param['seed_raised'][0])][0],
        'presale_2_raised': [left_over_raise/4 * 1e6 if uploaded_file is None else float(sys_param['seed_raised'][0])][0],
        'public_sale_raised': [left_over_raise/4 * 1e6 if uploaded_file is None else float(sys_param['seed_raised'][0])][0],
        'seed_valuation': [np.linspace(launch_valuation/fundraising_style_map[fundraising_style], launch_valuation, 4)[0] * 1e6 if uploaded_file is None else float(sys_param['seed_valuation'][0])][0],
        'presale_1_valuation': [np.linspace(launch_valuation/fundraising_style_map[fundraising_style], launch_valuation, 4)[1] * 1e6 if uploaded_file is None else float(sys_param['presale_1_valuation'][0])][0],
        'presale_2_valuation': [np.linspace(launch_valuation/fundraising_style_map[fundraising_style], launch_valuation, 4)[2] * 1e6 if uploaded_file is None else float(sys_param['presale_2_valuation'][0])][0],
    }

    st.write(new_params)

    return new_params

if uploaded_file is not None:
    # Get the file name and construct the full path
    input_file_name = uploaded_file.name
    input_file_path = os.path.join(input_file_base_path, input_file_name)
    
    # Write the uploaded file's content to the destination file
    with open(input_file_path, 'wb') as f:
        f.write(uploaded_file.getvalue())

    # get new parameters from UI
    new_params = model_ui_inputs(input_file_path, parameter_list)

else:
    input_file_name = 'Quantitative_Token_Model_V1.89_radCad_integration - radCAD_inputs.csv'
    input_file_path = input_file_base_path + input_file_name
    
    # get new parameters from UI
    new_params = model_ui_inputs(input_file_path, parameter_list)



# Run Simulation
if 'button_clicked' not in st.session_state:
    st.session_state['button_clicked'] = False
if st.button('Run Simulation'):
    st.session_state['button_clicked'] = True
if 'button_clicked' in st.session_state and st.session_state['button_clicked']:
    st.markdown("Use "+input_file_name+" as input file for the simulation.")
    
    # compose adjusted parameters
    adjusted_params = new_params

    # Run the simulation.py script
    result = simulation(input_file_path, adjusted_params=adjusted_params)
    st.write(f"Simulation finished based on these parameters:")
    st.dataframe(get_simulation_data('interfaceData.db', 'sys_param'))
    st.success('Done!')


    # Reset the session state variable after running the simulation
    st.session_state['button_clicked'] = False
