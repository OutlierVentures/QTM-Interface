import streamlit as st
import streamlit_authenticator as stauth
import pandas as pd
import yaml
from yaml.loader import SafeLoader
import os, sys
from PIL import Image
from UserInterface.helpers import header, safeToYaml
from brownian_motion_generator import brownian_motion_generator


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
        if st.session_state["authenticator"].register_user(fields=['username', 'password', 'email']):
            st.success('User registered successfully')
            safeToYaml(config)
    except Exception as e:
        st.error(e)

# Login section
with st.expander('Login', expanded=False):
    name, authentication_status, username = st.session_state["authenticator"].login(fields=['username', 'password'])

<<<<<<< HEAD
    if authentication_status:
        st.success(f'✅ Successfully signed in as *{name}*')
    elif authentication_status is False:
=======
    st.session_state["authenticator"].login(location='main', 
            max_concurrent_users=10, 
            fields={'Form name': 'Login', 'Username': 'Enter Username', 'Password': 'Enter Password', 'Login': 'Sign In'}
            )


    if st.session_state["authentication_status"]:
        st.success(f'✅ Successfully signed in as *{st.session_state["name"]}*')
    elif st.session_state["authentication_status"] is False:
>>>>>>> 9168453023767a8dc8b97aab9c2539c668abce4c
        st.error('Username/password is incorrect')
        
        # Forgot password
        try:
            username_of_forgotten_password, email_of_forgotten_password, new_random_password = st.session_state["authenticator"].forgot_password(fields=['username', 'email'])
            if username_of_forgotten_password:
                st.success('New password to be sent securely')
                # Random password should be transferred to user securely
            else:
                st.error('Username not found')
        except Exception as e:
            st.error(e)
        
        # Forgot username
        try:
            username_of_forgotten_username, email_of_forgotten_username = st.session_state["authenticator"].forgot_username(field='email')
            if username_of_forgotten_username:
                st.success('Username to be sent securely')
                # Username should be transferred to user securely
            else:
                st.error('Email not found')
        except Exception as e:
            st.error(e)
    
    elif authentication_status is None:
        st.warning('Please enter your username and password')

# Update user details section
if authentication_status:
    with st.expander('Update User Details', expanded=False):        
        # Update user details
        try:
            if st.session_state["authenticator"].update_user_details(username, fields=['password', 'email']):
                st.success('Entries updated successfully')
                safeToYaml(config)
        except Exception as e:
            st.error(e)
        
        # Reset password
        try:
            if st.session_state["authenticator"].reset_password(username, fields=['old_password', 'new_password']):
                st.success('Password modified successfully')
                safeToYaml(config)
        except Exception as e:
            st.error(e)
