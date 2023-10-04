import streamlit as st
import pandas as pd
import numpy as np

from plots import *
from simulation import simulation

# Get the current directory
current_dir = os.path.dirname(os.path.abspath(__file__))
# Go up one folder
parent_dir = os.path.abspath(os.path.join(current_dir, os.pardir))
# Append the parent directory to sys.path
sys.path.append(parent_dir)
input_file_base_path = parent_dir+'/data/'

st.title('Quantitative Token Model')


# Upload Input File
st.markdown("Use the default input file or upload your own.")
uploaded_file = st.file_uploader("Choose a file")

if uploaded_file is not None:
    # Get the file name and construct the full path
    input_file_name = uploaded_file.name
    input_file_path = os.path.join(input_file_base_path, input_file_name)
    
    # Check if the file already exists
    if os.path.exists(input_file_path):
        st.write(f"File '{uploaded_file.name}' already exists, overwriting...")
    
    # Write the uploaded file's content to the destination file
    with open(input_file_path, 'wb') as f:
        f.write(uploaded_file.getvalue())
    
    st.write(f"File '{uploaded_file.name}' uploaded successfully!")
else:
    input_file_name = 'Quantitative_Token_Model_V1.89_radCad_integration - radCAD_inputs.csv'
    input_file_path = input_file_base_path + input_file_name



# Run Simulation
if 'button_clicked' not in st.session_state:
    st.session_state['button_clicked'] = False
if st.button('Run Simulation'):
    st.session_state['button_clicked'] = True
if 'button_clicked' in st.session_state and st.session_state['button_clicked']:
    st.markdown("Use "+input_file_name+" as input file for the simulation...")
    # Run the simulation.py script
    result = simulation(input_file_path)
    # Reset the session state variable after running the simulation
    st.session_state['button_clicked'] = False



# Plot Results
if 'button_plot_clicked' not in st.session_state:
    st.session_state['button_plot_clicked'] = False
if st.button('Plot All Results'):
    st.session_state['button_plot_clicked'] = True
if 'button_plot_clicked' in st.session_state and st.session_state['button_plot_clicked']:
    # Plot all results
    plot_all()
    # Reset the session state variable after running the simulation
    st.session_state['button_plot_clicked'] = False