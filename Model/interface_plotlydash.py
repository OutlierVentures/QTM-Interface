from dash import Dash, html, dcc, callback, Output, Input, State
import plotly.express as px
import pandas as pd
from plots import *
from simulation import simulation

df = get_simulation_data('interfaceData.db', 'simulation_data')

app = Dash(__name__)

app.layout = html.Div([
    html.H1(children='Quantitative Token Model', style={'textAlign':'center'}),
    dcc.Dropdown(df.columns, 'timestep', id='dropdown-selection'),
    dcc.Graph(id='graph-content'),
    html.Button('Run Simulation', id='submit-val', n_clicks=0),
    html.Div(id='container-button-basic',
             children='Restart the simulation by clicking the button.')
])

@callback(
    Output('graph-content', 'figure'),
    Input('dropdown-selection', 'value')
)
def update_graph(value):
    dff = get_simulation_data('interfaceData.db', 'simulation_data')
    return px.line(dff, x='timestep', y=value)

@callback(
    Output('container-button-basic', 'children'),
    Input('submit-val', 'n_clicks'),
    prevent_initial_call=True
)
def update_output(n_clicks):
    result = simulation()
    return 'The simulation return was "{}"'.format(result)

if __name__ == '__main__':
    app.run(debug=True)
