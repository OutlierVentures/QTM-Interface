import streamlit as st
import streamlit_authenticator as stauth
import pandas as pd
import yaml
from yaml.loader import SafeLoader
import os, sys
from PIL import Image
from UserInterface.helpers import header, safeToYaml

# Get the current directory
current_dir = os.path.dirname(os.path.abspath(__file__))

header(current_dir)

with open('./config.yaml') as file:
    config = yaml.load(file, Loader=SafeLoader)

st.session_state["authenticator"] = stauth.Authenticate(
    config['credentials'],
    config['cookie']['name'],
    config['cookie']['key'],
    config['cookie']['expiry_days'],
    config['preauthorized']
)

# Sign-up section
with st.expander('Sign-Up', expanded=False):
    try:
        if st.session_state["authenticator"].register_user():
            st.success('User registered successfully')
            safeToYaml(config)
    except Exception as e:
        st.error(e)

# Login section
with st.expander('Login', expanded=False):

    st.session_state["authenticator"].login()

    if st.session_state["authentication_status"]:
        st.success(f'✅ Successfully signed in as *{st.session_state["name"]}*')
    elif st.session_state["authentication_status"] is False:
        st.error('Username/password is incorrect')
        
        # forgot password
        try:
            username_of_forgotten_password, email_of_forgotten_password, new_random_password = st.session_state["authenticator"].forgot_password('Forgot password')
            if username_of_forgotten_password:
                st.success('New password to be sent securely')
                # Random password should be transferred to user securely
            else:
                st.error('Username not found')
        except Exception as e:
            st.error(e)
        
        # forgot username
        try:
            username_of_forgotten_username, email_of_forgotten_username = st.session_state["authenticator"].forgot_username('Forgot username')
            if username_of_forgotten_username:
                st.success('Username to be sent securely')
                # Username should be transferred to user securely
            else:
                st.error('Email not found')
        except Exception as e:
            st.error(e)
    
    elif st.session_state["authentication_status"] is None:
        st.warning('Please enter your username and password')

# update user details section
if st.session_state["authentication_status"]:
    with st.expander('Update User Details', expanded=False):        
        # update user details
        try:
            if st.session_state["authenticator"].update_user_details(username=st.session_state["username"]):
                st.success('Entries updated successfully')
                safeToYaml(config)
        except Exception as e:
            st.error(e)
        
        # reset password
        try:
            if st.session_state["authenticator"].reset_password(username=st.session_state["username"]):
                st.success('Password modified successfully')
                safeToYaml(config)
        except Exception as e:
            st.error(e)