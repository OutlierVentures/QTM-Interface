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
from plots import pie_plot_st
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

from state_variables import get_initial_state
import state_variables
import state_update_blocks
from parts.utils import *
from plots import *
from post_processing import *

import importlib
importlib.reload(state_variables)
importlib.reload(state_update_blocks)

# Get the current directory
current_dir = os.path.dirname(os.path.abspath(__file__))

# Go two folders up
parent_dir = os.path.abspath(os.path.join(current_dir, os.pardir))

# Append the parent directory to sys.path
sys.path.append(parent_dir)

@st.experimental_memo
def simulation(input_file):
    initial_state, sys_param, stakeholder_name_mapping, stakeholder_names = get_initial_state(input_file)
    
    start_time = time.process_time()

    MONTE_CARLO_RUNS = 1
    TIMESTEPS = 12*10

    model = Model(initial_state=initial_state, params=sys_param, state_update_blocks=state_update_blocks.state_update_block)
    simulation = Simulation(model=model, timesteps=TIMESTEPS, runs=MONTE_CARLO_RUNS)

    result = simulation.run()
    df = pd.DataFrame(result)
    simulation_end_time = time.process_time()

     # post processing

    postprocessing_one_start_time = time.process_time()
    data = postprocessing(df, substep=df.substep.max(), category="all") # at the end of the timestep = last substep
    postprocessing_all_end_time = time.process_time()

    # display necessery time data
    print("Simulation time: ", simulation_end_time - start_time, " s")
    print("Post processing one dataframe time: ", postprocessing_all_end_time - postprocessing_one_start_time, " s")
    print("Post processing all dataframes time: ", postprocessing_all_end_time - simulation_end_time, " s")
    print("Whole simulation + post processing time: ", time.process_time() - start_time, " s")


    # Apply the conversion function to each column in the DataFrame
    for col in data.columns:
        data[col] = data[col].apply(convert_to_json)

    conn = sqlite3.connect('interfaceData.db')
    
    # Save the DataFrame to a new SQLite table
    data.to_sql('simulation_data', conn, if_exists='replace', index=False)
    
    # Close the connection
    conn.close()
    return 0

if __name__ == '__main__':
    simulation(parent_dir+'/data/Quantitative_Token_Model_V1.89_radCad_integration - radCAD_inputs.csv')
