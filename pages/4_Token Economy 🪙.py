import streamlit as st
from UserInterface.plots import plot_token_economy, get_simulation_data
import os, sys
from UserInterface.helpers import ui_base, returnToStart, header

# Get the current directory
current_dir = os.path.dirname(os.path.abspath(__file__))
# Go up one folder
parent_dir = os.path.abspath(os.path.join(os.path.abspath(current_dir), os.pardir))
# Append the parent directory to sys.path
sys.path.append(parent_dir)

if 'authentication_status' in st.session_state:
    if st.session_state["authentication_status"]:
        header(parent_dir)
        ui_base(parent_dir)

        st.sidebar.markdown("## Token Economy 🪙")

        # main page
        st.markdown("## Token Economy 🪙")
        if 'param_id' in st.session_state:
            if st.session_state['param_id'] != "":
                sys_param_df = get_simulation_data('simulationData.db', 'sys_param')
                sys_param = sys_param_df[sys_param_df['id'] == st.session_state['param_id']]
                if 'max_months' in st.session_state:
                    if st.session_state['max_months']<sys_param['simulation_duration'].iloc[0]:
                        st.error(f"The simulation stopped after {st.session_state['max_months']} months, because the business ran out of funds.", icon="⚠️")
                    plot_token_economy(st.session_state['param_id'], st.session_state['max_months'])
                else:
                    plot_token_economy(st.session_state['param_id'], sys_param['simulation_duration'].iloc[0])
    else:
        returnToStart()
else:
    returnToStart()