import streamlit as st
from plots import *

st.title('Quantitative Token Model')

# side bar
if 'param_id' in st.session_state:
    param_id_init = st.session_state['param_id']
else:
    param_id_init = ""
parameter_id_choice = st.sidebar.text_input('Parameter ID',param_id_init)
st.session_state['param_id'] = parameter_id_choice
if parameter_id_choice not in get_simulation_data('simulationData.db', 'sys_param')['id'].to_list():
    st.sidebar.markdown(f"Parameter ID: {parameter_id_choice} does not exist. Please enter a valid parameter ID or run the simulation with your parameter set to get a parameter ID.")
else:
    st.sidebar.markdown(f"This is a valid parameter ID ✅")
st.sidebar.markdown("## Fundraising 💰")

# main page
st.markdown("## Fundraising 💰")
if 'param_id' in st.session_state:
    if st.session_state['param_id'] != "":
        plot_fundraising(st.session_state['param_id'])
