import streamlit as st
from datetime import datetime
import time

def marketSimulationInput():
    with st.expander("**Market Simulation**", expanded=False):
        st.markdown("### Market Simulation")
        st.write("**Market Assumptions**")
        switch = st.toggle('Activate', help="Enable market simulation") 
        
        if switch:
            # choose token to use as proxy for market sentiment
            token_choice_predefined = ['bitcoin', 'ethereum'] # extend list if needed
            token_choice = st.radio('Token to simulate', tuple(token_choice_predefined), help="Pick the token you want to use for the simulatation.").lower()
            
            # collect info on the simulation period
            sim_start_date = st.date_input("Start Date", help="The Start and End Dates define the historical market conditions you want to replicate. E.g. If you want to replicate a Bull Run scenario you can select Start Date = 01-01-2021 & End Date = 31-12-2021.") 
            sim_end_date = st.date_input("End Date", help="The Start and End Dates define the historical market conditions you want to replicate. E.g. If you want to replicate a Bull Run scenario you can select Start Date = 01-01-2021 & End Date = 31-12-2021.")

            # Convert datetime objects to Unix timestamps
            start_date_unix = int(time.mktime(sim_start_date.timetuple()))
            end_date_unix = int(time.mktime(sim_end_date.timetuple()))

            active = 1

        else:
            token_choice = 0
            start_date_unix = 0
            end_date_unix = 0
            active = 0

    mkt_return_dict = {
        "token": token_choice,
        "sim_start": start_date_unix,
        "sim_end": end_date_unix,
        "market": active
    }

    return mkt_return_dict

# Inlcude consistency checks and additional parameters:
# -minimum historical period to select with error messages
