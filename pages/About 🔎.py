import streamlit as st
from PIL import Image
import os, sys
from UserInterface.helpers import header, returnToStart

# Get the current directory
current_dir = os.path.dirname(os.path.abspath(__file__))
# Go up one folder
parent_dir = os.path.abspath(os.path.join(os.path.abspath(current_dir), os.pardir))
# Append the parent directory to sys.path
sys.path.append(parent_dir)

if 'authentication_status' in st.session_state:
    if st.session_state["authentication_status"]:
        header(parent_dir)

        st.markdown("## About 🔎")
        st.sidebar.markdown("## About 🔎")

        st.markdown("[Open Source Github Repository](https://github.com/OutlierVentures/QTM-Interface)")
        image = Image.open(parent_dir+'/images/Quantitative_Token_Model_Abstraction.jpeg')
        st.image(image, caption='Quantitative Token Model Abstraction')

    else:
        returnToStart()
else:
    returnToStart()