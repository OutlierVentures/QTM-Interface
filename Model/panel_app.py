import os
import param
import panel as pn
import pandas as pd
import sqlite3
from plots import *
from simulation import simulation
import time 

class MyApp(param.Parameterized):
    uploaded_file = param.FileSelector()
    run_simulation = param.Action(lambda x: x.param.trigger('run_simulation'), label='Run Simulation')
    plot_results = param.Action(lambda x: x.param.trigger('plot_results'), label='Plot Results')
    simulation_output = param.String(default='', doc='Simulation output')
    plotting_output = param.String(default='', doc='Plotting output')

    def __init__(self, **params):
        super().__init__(**params)
        self.file_path = None

    @param.depends('uploaded_file', watch=True)
    def _on_file_upload(self):
        if self.uploaded_file:
            os.makedirs('test_data', exist_ok=True)
            self.file_path = os.path.join('test_data', self.uploaded_file.filename)
            if os.path.exists(self.file_path):
                print(f"File '{self.uploaded_file.filename}' already exists, overwriting...")
            with open(self.file_path, 'wb') as f:
                f.write(self.uploaded_file.read())
            print(f"File '{self.uploaded_file.filename}' uploaded successfully!")



    @param.depends('run_simulation', watch=True)
    def _on_run_simulation(self):
        self.simulation_output = "Simulation running..."
        start_time = time.process_time()

        result = simulation()
        end_time = time.process_time()

        if result == 0:
            self.simulation_output = "Simulation completed successfully in " + str(end_time - start_time)
            plot_results('timestep', ['seed_a_tokens_vested_cum','angle_a_tokens_vested_cum','team_a_tokens_vested_cum','reserve_a_tokens_vested_cum'], 1)
        else:
            self.simulation_output = "Simulation encountered an error."
            print(result.stderr.decode('utf-8'))



    @param.depends('plot_results', watch=True)
    def _on_plot_results(self):
        self.plotting_output = "Plotting Results..."
        plot_results('timestep', ['seed_a_tokens_vested_cum','angle_a_tokens_vested_cum','team_a_tokens_vested_cum','reserve_a_tokens_vested_cum','presale_1_a_tokens_vested_cum'], 1)
        self.plotting_output = "Plotting completed."

    def panel(self):
        return pn.Row(
            pn.Column(
                "## QTM File Upload",
                "Using the original Excel file, upload only the input file as a CSV.",
                self.param.uploaded_file,
                self.param.run_simulation,
                self.param.plot_results,
            ),
            pn.Column(
                self.param.simulation_output,
                self.param.plotting_output,
            )
        )

app = MyApp()
app.panel().servable()
