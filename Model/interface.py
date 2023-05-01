from flask import Flask, render_template, request
import plotly.graph_objs as go
import pandas as pd


app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        # get the form data
        data = request.form['data']
        timestep_column = request.form['timestep_column']
        investor_column = request.form['investor_column']
        allocation_column = request.form['allocation_column']

        # create a dataframe from the form data
        df = pd.read_json(data)

        # plot the stacked area graph
        fig = go.Figure()
        for investor in df[investor_column].unique():
            fig.add_trace(go.Scatter(x=df[timestep_column], y=df[df[investor_column] == investor][allocation_column],
                                     mode='lines', name=investor))
        fig.update_layout(title='Investor Allocation Over Time', xaxis_title='Time Step', yaxis_title='Token Allocation')

        # generate the HTML for the plotly graph
        plot_html = fig.to_html(full_html=False)

        # render the template with the plotly graph
        return render_template('index.html', plot_html=plot_html)

    # render the form template on a GET request
    return render_template('index.html')

if __name__ == '__main__':
    app.run(debug=True)
