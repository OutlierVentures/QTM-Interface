import streamlit as st
import pandas as pd
import numpy as np

from plots import *
from simulation import simulation

st.title('Quantitative Token Model')

st.button('Run Simulation', on_click=simulation)

st.button('Plot Results', on_click=plot_results('timestep', ['seed_a_tokens_vested_cum','angle_a_tokens_vested_cum','team_a_tokens_vested_cum','reserve_a_tokens_vested_cum','presale_1_a_tokens_vested_cum'], 1))