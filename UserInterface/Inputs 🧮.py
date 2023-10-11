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
from UserInterface.helpers import fundraising_style_map, param_help, model_ui_inputs

input_file_base_path = parent_dir+'/data/'

st.title('Quantitative Token Model')

# side bar
if 'param_id' in st.session_state:
    param_id_init = st.session_state['param_id']
else:
    param_id_init = ""
parameter_id_choice = st.sidebar.text_input('Parameter ID',param_id_init)
st.session_state['param_id'] = parameter_id_choice
try:
    if parameter_id_choice not in get_simulation_data('simulationData.db', 'sys_param')['id'].to_list():
        st.sidebar.markdown(f"Parameter ID: {parameter_id_choice} does not exist. Please enter a valid parameter ID or run the simulation with your parameter set to get a parameter ID.")
    else:
        st.sidebar.markdown(f"This is a valid parameter ID ✅")
except:
    pass
st.sidebar.markdown("## Inputs 🧮")
st.sidebar.markdown("Parameter input section for the Quantitative Token Model. Use the default parameters, customize them in the user interface, or upload your own input file based on the radCAD_inputs tab in the [spreadsheet QTM](https://drive.google.com/drive/folders/1eSgm4NA1Izx9qhXd6sdveUKF5VFHY6py?usp=sharing).")

# main page
st.markdown("## Inputs 🧮")

# Upload Input File
with st.expander("Upload Own Input File"):
    st.markdown("### Load Input File 📂")
    st.markdown("Use the default input file or upload your own based on the")
    st.markdown("[Spreadsheet QTM](https://drive.google.com/drive/folders/1eSgm4NA1Izx9qhXd6sdveUKF5VFHY6py?usp=sharing) ➡️ navigate to radCAD_inputs tab ➡️ save it as .csv and then upload it here ⬇️")
    uploaded_file = st.file_uploader("Choose a file")

st.markdown("### Basic Token Information")

if uploaded_file is not None:
    # Get the file name and construct the full path
    input_file_name = uploaded_file.name
    input_file_path = os.path.join(input_file_base_path, input_file_name)
    
    # Write the uploaded file's content to the destination file
    with open(input_file_path, 'wb') as f:
        f.write(uploaded_file.getvalue())

    # get new parameters from UI
    new_params = model_ui_inputs(input_file_path, uploaded_file, parameter_list)

else:
    input_file_name = 'Quantitative_Token_Model_V1.89_radCad_integration - radCAD_inputs.csv'
    input_file_path = input_file_base_path + input_file_name
    
    # get new parameters from UI
    new_params = model_ui_inputs(input_file_path, uploaded_file, parameter_list)



# Run Simulation
if 'param_id' not in st.session_state:
    st.session_state['param_id'] = ""
if 'button_clicked' not in st.session_state:
    st.session_state['button_clicked'] = False
if st.button('Run Simulation'):
    st.session_state['button_clicked'] = True
if 'button_clicked' in st.session_state and st.session_state['button_clicked']:
    # compose adjusted parameters
    adjusted_params = new_params

    # Run the simulation.py script
    st.session_state['param_id'] = simulation(input_file_path, adjusted_params=adjusted_params)
    st.write(f"Simulation with id {st.session_state['param_id']} has finished based on these parameters:")
    df = get_simulation_data('simulationData.db', 'sys_param')
    #col = df.pop("id")
    #st.write(col)
    #st.write(col.name)
    #df = df.insert(0, col.name, col)
    st.dataframe(df)
    st.success('Done!')


    # Reset the session state variable after running the simulation
    st.session_state['button_clicked'] = False
