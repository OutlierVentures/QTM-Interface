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
from UserInterface.plots import *
from Model.simulation import simulation
from Model.parts.utils import *
from data.not_iterable_variables import parameter_list
from UserInterface.inputConsolidation import model_ui_inputs, get_simulation_data
from UserInterface.helpers import delete_parameter_and_simulation_data, ui_base, returnToStart, header
st.set_page_config(layout="wide")


input_file_base_path = parent_dir+'/data/'
if 'authentication_status' in st.session_state:
    if st.session_state["authentication_status"]:
        header(parent_dir)
        db_sorted = ui_base(parent_dir, return_db_sorted=True)
        try:
            # delete current selected parameter set and simulation data from database
            if 'delete_parameters_clicked' not in st.session_state:
                st.session_state['delete_parameters_clicked'] = False
            if st.sidebar.button('Delete Parameter Set'):
                st.session_state['delete_parameters_clicked'] = True
            if 'delete_parameters_clicked' in st.session_state:
                if st.session_state['delete_parameters_clicked']:
                    if st.session_state['param_id'] != "":
                        delete_parameter_and_simulation_data(st.session_state['param_id'])
                        st.session_state['param_id'] = ""
                        st.session_state['project_name'] = ""
                        st.session_state['delete_parameters_clicked'] = False
                        st.cache_data.clear()
                        st.sidebar.success('Parameter set and simulation data deleted successfully ✅')
                    else:
                        st.sidebar.error(f"Please enter a valid parameter ID to delete the parameter set.", icon="⚠️")
                else:
                    st.session_state['delete_parameters_clicked'] = False
        except Exception as e: print(e)

        st.sidebar.markdown("## Inputs 🧮")
        st.sidebar.markdown("Parameter input section for the Quantitative Token Model. Use the default parameters, customize them in the user interface, or upload your own input file based on the radCAD_inputs tab in the [spreadsheet QTM](https://drive.google.com/drive/folders/1eSgm4NA1Izx9qhXd6sdveUKF5VFHY6py?usp=sharing).")

        # main page
        st.markdown(
            '''
            <style>
            .streamlit-expanderHeader {
                color: #4E32BF; # Adjust this for expander header color
            }
            .streamlit-expanderContent {
                color: #4E32BF; # Expander content color
            }
            </style>
            ''',
            unsafe_allow_html=True
        )
        st.markdown("## Inputs 🧮")
        col01, col02 = st.columns(2)
        with col01:
            if 'project_name' in st.session_state:
                project_name = st.text_input('Project Name', st.session_state['project_name'])
            else:
                project_name = st.text_input('Project Name', "")
            st.session_state['project_name'] = project_name

        with col02:
            # Upload Input File
            with st.expander("Upload Own Input File (optional)"):
                st.markdown("### Load Input File 📂")
                st.markdown("Use the default input file or upload your own based on the")
                st.markdown("[Spreadsheet QTM](https://drive.google.com/drive/folders/1eSgm4NA1Izx9qhXd6sdveUKF5VFHY6py?usp=sharing) ➡️ navigate to radCAD_inputs tab ➡️ save it as .csv and then upload it here ⬇️")
                uploaded_file = st.file_uploader("Choose a file")
                if uploaded_file is not None:
                    st.success('File uploaded successfully ✅')
                    if 'param_id' in st.session_state:
                        if st.session_state['param_id'] != "":
                            st.error(f"Delete the Parameter ID to apply the new input file parameters.", icon="⚠️")

        if uploaded_file is not None:
            # reset the parameter id
            st.session_state['param_id'] = ""

            # Get the file name and construct the full path
            input_file_name = uploaded_file.name
            input_file_path = os.path.join(input_file_base_path, input_file_name)
            
            # Write the uploaded file's content to the destination file
            with open(input_file_path, 'wb') as f:
                f.write(uploaded_file.getvalue())

            # get new parameters from UI
            new_params = model_ui_inputs(input_file_path, uploaded_file, parameter_list, col01)
        else:
            input_file_name = 'Quantitative_Token_Model_V1.90_radCAD_integration - radCAD_inputs DEFAULT.csv'
            input_file_path = input_file_base_path + input_file_name
            
            # get new parameters from UI
            new_params = model_ui_inputs(input_file_path, uploaded_file, parameter_list, col01)


        # Run Simulation
        if 'param_id' not in st.session_state:
            st.session_state['param_id'] = ""
        if 'button_clicked' not in st.session_state:
            st.session_state['button_clicked'] = False
        if 'parameter_button_clicked' not in st.session_state:
            st.session_state['parameter_button_clicked'] = False
        if 'execute_inputs' in st.session_state:
            status_msg = ["" if st.session_state['execute_inputs'] else "❌"][0]
        else:
            status_msg = ""
        bcol1, bcol2 = st.columns(2)
        with bcol1:
            if st.button('Run Simulation'+ status_msg):
                st.session_state['button_clicked'] = True
        with bcol2:
            if st.button('Show Parameter Sets'):
                st.session_state['parameter_button_clicked'] = True
            
        if 'button_clicked' in st.session_state and st.session_state['button_clicked']:
            # compose adjusted parameters
            new_params.update({'project_name':project_name})
            adjusted_params = new_params

            # Run the simulation.py script
            if 'execute_inputs' in st.session_state:
                if st.session_state['execute_inputs']:
                    st.session_state['param_id'], execute_sim = simulation(input_file_path, adjusted_params, True)
                else:
                    execute_sim = False
                    st.error(f"Simulation can't be started due to invalid inputs!", icon="⚠️")
            else:
                st.session_state['param_id'], execute_sim = simulation(input_file_path, adjusted_params, True)
            
            if execute_sim:
                st.write(f"Simulation with id {st.session_state['param_id']} has finished based on these parameters:")
                df = get_simulation_data('simulationData.db', 'sys_param')
                df.insert(0, "id", df.pop("id"))
                df.insert(0, "project_name", df.pop("project_name"))
                st.dataframe(df)
                st.success('Done!')
                # write hint for user to switch to the next page
                st.info("Go to the Fundraising 💰, Business 📈, Token Economy 🪙, or Data 💾 page in the navigation bar on the left side to see the respective simulation results!", icon="ℹ️")

            # Reset the session state variable after running the simulation
            st.session_state['button_clicked'] = False

        if 'parameter_button_clicked' in st.session_state and st.session_state['parameter_button_clicked']:
            if len(db_sorted) > 0:
                st.write(f"Parameter sets:")
                df = get_simulation_data('simulationData.db', 'sys_param')
                df.insert(0, "id", df.pop("id"))
                df.insert(0, "project_name", df.pop("project_name"))
                st.dataframe(df)
            else:
                st.error(f"No parameter sets available!", icon="⚠️")
            st.session_state['parameter_button_clicked'] = False

    else:
        returnToStart()
else:
    returnToStart()