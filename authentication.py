import streamlit as st
import streamlit_authenticator as stauth
import yaml
from yaml.loader import SafeLoader

with open('./config.yaml') as file:
    config = yaml.load(file, Loader=SafeLoader)

authenticator = stauth.Authenticate(
    config['credentials'],
    config['cookie']['name'],
    config['cookie']['key'],
    config['cookie']['expiry_days'],
    config['preauthorized']
)

print(f"config: {config}")
print(f"authenticator {authenticator}")

authenticator.login('Login', 'main')

if st.session_state["authentication_status"]:
    authenticator.logout('Logout', 'main', key='unique_key')
    st.write(f'Welcome *{st.session_state["name"]}*')
    st.title('Some content')
elif st.session_state["authentication_status"] is False:
    st.error('Username/password is incorrect')
elif st.session_state["authentication_status"] is None:
    st.warning('Please enter your username and password')


if st.session_state["authentication_status"]:
    try:
        if authenticator.reset_password(st.session_state["username"], 'Reset password'):
            st.success('Password modified successfully')
    except Exception as e:
        st.error(e)

    try:
        if authenticator.register_user('Register user', preauthorization=False):
            st.success('User registered successfully')
    except Exception as e:
        st.error(e)
    
    try:
        username_of_forgotten_password, email_of_forgotten_password, new_random_password = authenticator.forgot_password('Forgot password')
        if username_of_forgotten_password:
            st.success('New password to be sent securely')
            # Random password should be transferred to user securely
        else:
            st.error('Username not found')
    except Exception as e:
        st.error(e)

    try:
        username_of_forgotten_username, email_of_forgotten_username = authenticator.forgot_username('Forgot username')
        if username_of_forgotten_username:
            st.success('Username to be sent securely')
            # Username should be transferred to user securely
        else:
            st.error('Email not found')
    except Exception as e:
        st.error(e)

    try:
        if authenticator.update_user_details(st.session_state["username"], 'Update user details'):
            st.success('Entries updated successfully')
    except Exception as e:
        st.error(e)
    
# safe to yaml file
with open('../config.yaml', 'w') as file:
    yaml.dump(config, file, default_flow_style=False)