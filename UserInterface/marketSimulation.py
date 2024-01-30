import streamlit as st
from datetime import datetime
import time

def marketSimulationInput():
    with st.expander("**Market Simulation**", expanded=True):
        st.markdown("### Market Simulation")
        st.write("**Market Assumptions**")

        # choose token to use as proxy for market sentiment
        token_choice_predefined = ['bitcoin', 'ethereum']
        token_choice = st.radio('Token to simulate', tuple(token_choice_predefined), help="Pick the token you want to simulate.").lower()
        
        # colllect info on the simulation period
        sim_start_date = st.date_input("Simulation Start", help="The token launch date is the time when the token becomes liquid to be traded and at which the vesting conditions start to apply. Defining a date before today's date means that the token has already been launched and therefore requires additional information about the current token distribution and valuations in the parameter definitions below.") # change description
        sim_end_date = st.date_input("Simulation End", help="The token launch date is the time when the token becomes liquid to be traded and at which the vesting conditions start to apply. Defining a date before today's date means that the token has already been launched and therefore requires additional information about the current token distribution and valuations in the parameter definitions below.") # change description

        # Convert datetime objects to Unix timestamps
        start_date_unix = int(time.mktime(sim_start_date.timetuple()))
        end_date_unix = int(time.mktime(sim_end_date.timetuple()))

    mkt_return_dict = {
        "token": token_choice,
        "sim_start": start_date_unix,
        "sim_end": end_date_unix
    }

    return mkt_return_dict

# Inlcude a bunch of consistency checks and additional parameters.
