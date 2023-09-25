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
import json

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

from sys_params import *
import state_variables
import state_update_blocks
import sys_params
from parts.utils import *
from plots import *
from post_processing import *

import importlib
importlib.reload(state_variables)
importlib.reload(state_update_blocks)
importlib.reload(sys_params)

# Get the current directory
current_dir = os.path.dirname(os.path.abspath(__file__))

# Go two folders up
parent_dir = os.path.abspath(os.path.join(current_dir, os.pardir))

def simulation():
    start_time = time.process_time()

    MONTE_CARLO_RUNS = 1
    TIMESTEPS = 12*10

    model = Model(initial_state=state_variables.initial_state, params=sys_params.sys_param, state_update_blocks=state_update_blocks.state_update_block)
    simulation = Simulation(model=model, timesteps=TIMESTEPS, runs=MONTE_CARLO_RUNS)

    result = simulation.run()
    df = pd.DataFrame(result)
    simulation_end_time = time.process_time()

     # post processing

    postprocessing_one_start_time = time.process_time()
    data = postprocessing(df, substep=df.substep.max()) # at the end of the timestep = last substep
    postprocessing_all_end_time = time.process_time()

    # display necessery time data
    print("Simulation time: ", simulation_end_time - start_time, " s")
    print("Post processing one dataframe time: ", postprocessing_all_end_time - postprocessing_one_start_time, " s")
    print("Post processing all dataframes time: ", postprocessing_all_end_time - simulation_end_time, " s")
    print("Whole Test time: ", time.process_time() - start_time, " s")


    # Apply the conversion function to each column in the DataFrame
    for col in data.columns:
        data[col] = data[col].apply(convert_to_json)

    conn = sqlite3.connect('interfaceData.db')
    
    # Save the DataFrame to a new SQLite table
    data.to_sql('simulation_data', conn, if_exists='replace', index=False)
    
    # Close the connection
    conn.close()
    return 0
