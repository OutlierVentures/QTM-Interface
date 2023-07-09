# Dependences
import pandas as pd
import numpy as np

# radCAD
from radcad import Model, Simulation, Experiment
from radcad.engine import Engine, Backend

import state_variables
import state_update_blocks
import sys_params
from plots import *
from post_processing import *

import importlib
importlib.reload(state_variables)
importlib.reload(state_update_blocks)
importlib.reload(sys_params)

import traceback

if __name__ == '__main__':
    MONTE_CARLO_RUNS = 1
    TIMESTEPS = 12*10

    model = Model(initial_state=state_variables.initial_state, params=sys_params.sys_param, state_update_blocks=state_update_blocks.state_update_block)
    simulation = Simulation(model=model, timesteps=TIMESTEPS, runs=MONTE_CARLO_RUNS)

    result = simulation.run()
    df = pd.DataFrame(result)




    # post processing
    data = postprocessing(df)



    ##---User adoption Plots---#
    plot_line_chart(data,'timestep',['token_holders','product_users'])
    #plot_line_chart(data,'timestep',['product_revenue'])
    #plot_line_chart(data,'timestep',['token_buys'])

   # monte_carlo_plot(data,'timestep','timestep','team_tokens_vested',1)

#    plt.show()

