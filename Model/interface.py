import streamlit as st
import os

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

