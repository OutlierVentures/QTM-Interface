import streamlit as st
import os
import subprocess
import pandas as pd
import sqlite3
import time
from plots import *

st.title('QTM File Upload')

st.markdown("Using the original Excel file, upload only the input file as a CSV.")

uploaded_file = st.file_uploader("Choose a file")

if uploaded_file is not None:
    # Create the directory structure if it doesn't exist
    os.makedirs('test_data', exist_ok=True)
    
        
    # Get the file name and construct the full path
    file_path = os.path.join('test_data', uploaded_file.name)
    
    # Check if the file already exists
    if os.path.exists(file_path):
        st.write(f"File '{uploaded_file.name}' already exists, overwriting...")
    
    # Write the uploaded file's content to the destination file
    with open(file_path, 'wb') as f:
        f.write(uploaded_file.getvalue())
    
    st.write(f"File '{uploaded_file.name}' uploaded successfully!")

script_dir = os.path.dirname(os.path.abspath(__file__))
script_path = os.path.join(script_dir, 'simulation.py')

if 'button_clicked' not in st.session_state:
    st.session_state.button_clicked = False

if st.button('Run Simulation'):
    st.session_state.button_clicked = True

if 'button_plot_clicked' not in st.session_state:
    st.session_state.button_plot_clicked = False

if st.button('Plot Results'):
    st.session_state.button_plot_clicked = True

if st.session_state.button_clicked:
    
    st.markdown("<div style='background-color:blue; padding:10px; border-radius:5px;'>Simulation running...</div>", unsafe_allow_html=True)
    
    # Run the simulation.py script
    result = subprocess.run(['python', script_path], stdout=subprocess.PIPE, stderr=subprocess.PIPE)

    if result.returncode == 0:
        st.markdown("<div style='background-color:green; padding:10px; border-radius:5px;'>Simulation completed successfully!</div>", unsafe_allow_html=True)
        #st.write(result.stdout.decode('utf-8'))
    else:
        st.markdown("<div style='background-color:red; padding:10px; border-radius:5px;'>Simulation encountered an error.</div>", unsafe_allow_html=True)
        st.write(result.stderr.decode('utf-8'))

    plot_results('timestep', ['seed_a_tokens_vested_cum','angle_a_tokens_vested_cum','team_a_tokens_vested_cum','reserve_a_tokens_vested_cum'], 1)

    # Reset the session state variable after running the simulation
    st.session_state.button_clicked = False



if st.session_state.button_plot_clicked:
    
    st.markdown("<div style='background-color:blue; padding:10px; border-radius:5px;'>Plotting Results...</div>", unsafe_allow_html=True)

    plot_results('timestep', ['seed_a_tokens_vested_cum','angle_a_tokens_vested_cum','team_a_tokens_vested_cum','reserve_a_tokens_vested_cum','presale_1_a_tokens_vested_cum'], 1)

    # Reset the session state variable after running the simulation
    st.session_state.button_plot_clicked = False
 

 

