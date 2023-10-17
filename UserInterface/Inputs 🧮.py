import streamlit as st
import pandas as pd
import numpy as np
import os, sys
from PIL import Image

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

image = Image.open(parent_dir+'/images/ov_logo.jpg')
st.image(image, width=125)
st.title('Quantitative Token Model')

# side bar
if 'param_id' in st.session_state:
    param_id_init = st.session_state['param_id']
else:
    param_id_init = ""
# get all existing project names
try:
    db_sorted = get_simulation_data('simulationData.db', 'sys_param').sort_values('project_name', ascending=True)
    project_names = db_sorted['project_name']
    project_names = project_names.to_list()
    project_names.append('')
except:
    db_sorted = pd.DataFrame()
    project_names = ['']
if 'project_name' not in st.session_state:
    st.session_state['project_name'] = ''

if 'project_name' in st.session_state and 'param_id' in st.session_state and len(db_sorted) > 0:
    st.session_state['project_name'] = st.sidebar.selectbox('Project Name', tuple(project_names), index=[db_sorted['id'].to_list().index(st.session_state['param_id']) if st.session_state['param_id'] in db_sorted['id'].to_list() else len(project_names)-1][0])
    st.session_state['param_id'] = st.sidebar.text_input('Parameter ID',[db_sorted[db_sorted['project_name']==st.session_state['project_name']]['id'].iloc[0] if st.session_state['project_name'] in db_sorted['project_name'].to_list() else ""][0])
else:
    st.session_state['project_name'] = st.sidebar.selectbox('Project Name', tuple(project_names), index=len(project_names)-1)
    st.session_state['param_id'] = st.sidebar.text_input('Parameter ID', "")

try:
    if st.session_state['param_id'] not in get_simulation_data('simulationData.db', 'sys_param')['id'].to_list():
        st.sidebar.markdown(f"Parameter ID: {st.session_state['param_id']} does not exist. Please enter a valid parameter ID or run the simulation with your parameter set to get a parameter ID.")
    else:
        st.sidebar.markdown(f"This is a valid parameter ID ✅")
except:
    pass
st.sidebar.markdown("## Inputs 🧮")
st.sidebar.markdown("Parameter input section for the Quantitative Token Model. Use the default parameters, customize them in the user interface, or upload your own input file based on the radCAD_inputs tab in the [spreadsheet QTM](https://drive.google.com/drive/folders/1eSgm4NA1Izx9qhXd6sdveUKF5VFHY6py?usp=sharing).")

# main page
st.markdown("## Inputs 🧮")
if 'project_name' in st.session_state:
    project_name = st.text_input('Project Name', st.session_state['project_name'])
else:
    project_name = st.text_input('Project Name', "")
st.session_state['project_name'] = project_name

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
    input_file_name = 'Quantitative_Token_Model_V1.89_radCad_integration - radCAD_inputs DEFAULT.csv'
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
    new_params.update({'project_name':project_name})
    adjusted_params = new_params

    # Run the simulation.py script
    if 'execute_inputs' in st.session_state:
        if st.session_state['execute_inputs']:
            st.session_state['param_id'], execute_sim = simulation(input_file_path, adjusted_params=adjusted_params)
        else:
            execute_sim = False
            st.warning(f"Simulation can't be started due to invalid inputs!", icon="⚠️")
    else:
        st.session_state['param_id'], execute_sim = simulation(input_file_path, adjusted_params=adjusted_params)
    if execute_sim:
        st.write(f"Simulation with id {st.session_state['param_id']} has finished based on these parameters:")
        df = get_simulation_data('simulationData.db', 'sys_param')
        df.insert(0, "id", df.pop("id"))
        df.insert(0, "project_name", df.pop("project_name"))
        st.dataframe(df)
        st.success('Done!')


    # Reset the session state variable after running the simulation
    st.session_state['button_clicked'] = False
