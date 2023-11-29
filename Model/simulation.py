# Dependences
import pandas as pd
import numpy as np
import os
import sys
import traceback
import time
import streamlit as st
import pandas as pd
import sqlite3
import streamlit as st

# radCAD
from radcad import Model, Simulation, Experiment
from radcad.engine import Engine, Backend


# Project dependences
# Get the current directory
current_dir = os.path.dirname(os.path.abspath(__file__))
# Go up one folder
parent_dir = os.path.abspath(os.path.join(current_dir, os.pardir))
# Append the parent directory to sys.path
sys.path.append(parent_dir)


from Model.state_variables import get_initial_state
from Model.state_update_blocks import state_update_blocks
from Model.parts.utils import *
from Model.post_processing import *

@st.cache_data
def simulation(input_file, adjusted_params):
    # get simulation parameters
    initial_state, sys_param, stakeholder_name_mapping, stakeholder_names, conn, cur, param_id, execute_sim = get_initial_state(input_file, adjusted_params)
    start_time = time.process_time()
    listOfSimulationDataTables = cur.execute(''' SELECT count(name) FROM sqlite_master WHERE type='table' AND name='simulation_data_{param_id}' '''.format(length='multi-line', param_id=param_id))
    try:
        length = listOfSimulationDataTables.fetchall()[0][0]
    except:
        length = 0
    
    if length == 0 and execute_sim:
        print("New simulation started...")
        MONTE_CARLO_RUNS = 1
        TIMESTEPS = int(sys_param['simulation_duration'][0])

        model = Model(initial_state=initial_state, params=sys_param, state_update_blocks=state_update_blocks)
        simulation = Simulation(model=model, timesteps=TIMESTEPS, runs=MONTE_CARLO_RUNS)

        result = simulation.run()
        df = pd.DataFrame(result)

        # post processing
        data = postprocessing(df, substep=df.substep.max(), category="all") # at the end of the timestep = last substep
        #data = postprocessing(df, substep=df.substep.min()+1, category="all") # at the end of the timestep = last substep


        # Apply the conversion function to each column in the DataFrame
        for col in data.columns:
            data[col] = data[col].apply(convert_to_json)
        
        # Save the DataFrame to a new SQLite table
        data.to_sql('simulation_data_'+param_id, conn, if_exists='replace', index=False)
        
        # Close the connection
        conn.close()

        # display necessery time
        print("Simulation time: ", time.process_time() - start_time, " s")

    return param_id, execute_sim