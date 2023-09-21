import streamlit as st
import os
import subprocess


st.title('QTM File Upload')

st.markdown("Using the original Excel file, upload only the input file as a CSV.")

uploaded_file = st.file_uploader("Choose a file")

if uploaded_file is not None:
    # Create the directory structure if it doesn't exist
    os.makedirs('data/test_data', exist_ok=True)
    
        
    # Get the file name and construct the full path
    file_path = os.path.join('data/test_data', uploaded_file.name)
    
    # Check if the file already exists
    if os.path.exists(file_path):
        st.write(f"File '{uploaded_file.name}' already exists, overwriting...")
    
    # Write the uploaded file's content to the destination file
    with open(file_path, 'wb') as f:
        f.write(uploaded_file.getvalue())
    
    st.write(f"File '{uploaded_file.name}' uploaded successfully!")


if st.button('Run Simulation'):
    # Set a session state variable to indicate the button has been clicked
    st.session_state.run_simulation_clicked = True

# Check the session state variable to determine whether to run the simulation
if st.session_state.run_simulation_clicked:
    # Code to run the simulation goes here
    st.markdown("<div style='background-color:blue; padding:10px; border-radius:5px;'>Simulation running...</div>", unsafe_allow_html=True)
    
    # Get the directory of the current script
    script_dir = os.path.dirname(os.path.abspath(__file__))
    script_path = os.path.join(script_dir, 'simulation.py')
    
    # Run the simulation.py script
    result = subprocess.run(['python', script_path], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    
    if result.returncode == 0:
        st.markdown("<div style='background-color:green; padding:10px; border-radius:5px;'>Simulation completed successfully!</div>", unsafe_allow_html=True)
        #st.write(result.stdout.decode('utf-8'))
    else:
        st.markdown("<div style='background-color:red; padding:10px; border-radius:5px;'>Simulation encountered an error.</div>", unsafe_allow_html=True)
        #st.write(result.stderr.decode('utf-8'))
    
    # Reset the session state variable after running the simulation
    st.session_state.run_simulation_clicked = False