import matplotlib.pyplot as plt
import pandas as pd
import streamlit as st
import numpy as np
import sys, os
import sqlite3
import plotly.figure_factory as ff
import plotly.express as px
import plotly.graph_objects as go
from Model.sys_params import *


def customize_plotly_figure(fig, x_title=None, y_title=None, info_box=None, plot_title=None):
    # Set the axes titles
    if x_title:
        fig.update_xaxes(title_text=x_title)
    if y_title:
        fig.update_yaxes(title_text=y_title)


    # Add a plot title
    if plot_title:
        fig.update_layout(title_text=plot_title, title_x=0)  # Adjust title_x as needed

     # Add an info box with a white background and black text at the bottom right
    if info_box:
        # Calculate the safe position for the info box
        box_width = len(info_box) * 8  # Adjust the width as needed
        x_coord = 0.98 - box_width / 1200  # Adjust the divisor as needed
        y_coord = 0.02  # Adjust the y-coordinate to place it at the bottom
        
        fig.add_annotation(
            text=info_box,
            align='left',
            showarrow=False,
            xref='paper',
            yref='paper',
            x=x_coord,
            y=y_coord,
            bordercolor='black',
            bgcolor='white',
            borderwidth=1,
            font=dict(color='black')
        )

def format_column_name(column_name):
    """
    This function takes a column name as input, replaces underscores with spaces,
    and capitalizes the first letter of each word.

    Parameters:
    - column_name (str): The input string that needs to be formatted.

    Returns:
    str: The formatted string with spaces instead of underscores and capitalized words.
    """
    # Replacing underscores with spaces
    name_with_spaces = column_name.replace('_a_', ' ').replace('_token_effective','').replace('_token_allocation','').replace('ua_','').replace('ba_','').replace('te_','').replace('lp_tokens', 'Liquidity Pool').replace('lp_valuation','Liquidity Pool').replace('_supply','').replace('tokens','').replace('lp_','').replace('u_','').replace('_cum','').replace('allocation','').replace('_', ' ')
    
    # Capitalizing the first letter of each word
    user_friendly_name = name_with_spaces.title()
    
    return user_friendly_name

def drop_zero_columns(df):
    """
    This function drops all columns that only contain zeros.

    Parameters:
    - df (DataFrame): The input DataFrame.

    Returns:
    DataFrame: The DataFrame with all zero columns removed.
    """
    # Drop all columns that only contain zeros
    df = df.loc[:, (df != 0).any(axis=0)]
    
    return df



def get_simulation_data(db, dataset_name):
    # Connect to the SQLite database
    conn = sqlite3.connect(db)
    # Read the data from the SQLite table into a DataFrame
    df = pd.read_sql(f'SELECT * FROM {dataset_name}', conn)

    # Close the connection
    conn.close()
    return df

def area_plot_stakeholder_meta_allocations(param_id, stakeholder1_raw, max_months, percentage_area):
    df = get_simulation_data('simulationData.db', 'simulation_data_'+param_id)
    df = df[['timestep', stakeholder1_raw+'_a_utility_tokens', stakeholder1_raw+'_a_selling_tokens', stakeholder1_raw+'_a_holding_tokens'
             , stakeholder1_raw+'_a_utility_from_holding_tokens', stakeholder1_raw+'_a_selling_from_holding_tokens', stakeholder1_raw+'_a_holding_from_holding_tokens']].copy()
    df = df[df['timestep'].astype(float) <= max_months]

    # Format the column names
    formatted_columns = [format_column_name(col) for col in ['timestep' if not st.session_state['date_conversion'] else 'date', stakeholder1_raw+'_a_utility_tokens', stakeholder1_raw+'_a_selling_tokens', stakeholder1_raw+'_a_holding_tokens',
                                                             stakeholder1_raw+'_a_utility_from_holding_tokens', stakeholder1_raw+'_a_selling_from_holding_tokens', stakeholder1_raw+'_a_holding_from_holding_tokens']]
    
    # Format the column names
    formatted_columns = [col + ' From Vesting' if ('timestep' if not st.session_state['date_conversion'] else 'date' not in col and 'From Holding' not in col) else col for col in formatted_columns ]
    
    df.columns = formatted_columns

    plotly_colors = px.colors.qualitative.Plotly
    color_map = {}
    for i, value in enumerate(df[formatted_columns[1:]]):
        try:
            color_map[value] = plotly_colors[i]
        except:
            color_map[value] = plotly_colors[i-len(plotly_colors)]

    if percentage_area:
        fig = px.area(df, x=formatted_columns[0], y=formatted_columns[1:], color_discrete_map=color_map, groupnorm='fraction')
        fig.update_layout(yaxis_tickformat='.0%') # Convert the y-axis to percentages
    else:
        fig = px.area(df, x=formatted_columns[0], y=formatted_columns[1:], color_discrete_map=color_map)

    customize_plotly_figure(fig, x_title="Months", y_title="Tokens")

    st.plotly_chart(fig, use_container_width=True)

def plot_results_plotly(x, y_columns, run, param_id, max_months, calcColumns=[], x_title=None, y_title=None, info_box=None, plot_title=None, logy=False):

    df = get_simulation_data('simulationData.db', 'simulation_data_'+param_id)

    # structure calcColumns = {'col': {'sign': sign, 'firstCol': firstCol, 'secondCol': secondCol}}
    if len(calcColumns) > 0:
        for key, col in calcColumns.items():
            if col['sign'] == '+':
                df[key] = df[col['firstCol']].astype(float) + df[col['secondCol']].astype(float)
            elif col['sign'] == '-':
                df[key] = df[col['firstCol']].astype(float) - df[col['secondCol']].astype(float)
            elif col['sign'] == '*':
                df[key] = df[col['firstCol']].astype(float) * df[col['secondCol']].astype(float)
            elif col['sign'] == '/':
                df[key] = df[col['firstCol']].astype(float) / df[col['secondCol']].astype(float)

    # reduce df to max_months
    df = df[df['timestep'].astype(float) <= max_months]

    # example for Monte Carlo plots
    #monte_carlo_plot_st(df,'timestep','timestep','seed_a_tokens_vested_cum',3)

    # example for line plots of different outputs in one figure
    new_max_months = line_plot_plotly(df,x, y_columns, run, param_id, x_title=x_title, y_title=y_title, info_box=info_box, plot_title=plot_title ,logy=logy)
    return new_max_months

def vesting_cum_plot_results_plotly(x, y_columns, run, param_id, x_title=None, y_title=None, info_box=None, plot_title=None):

    df = get_simulation_data('simulationData.db', 'simulation_data_'+param_id)

    # example for Monte Carlo plots
    #monte_carlo_plot_st(df,'timestep','timestep','seed_a_tokens_vested_cum',3)

    # example for line plots of different outputs in one figure
    vesting_cum_plot_plotly(df,x, y_columns, run, param_id, x_title=x_title, y_title=y_title, info_box=info_box, plot_title=plot_title)



def aggregate_runs(df,aggregate_dimension,x,y):
    '''
    Function to aggregate the monte carlo runs along a single dimension.

    Parameters:
    df: dataframe name
    aggregate_dimension: the dimension you would like to aggregate on, the standard one is timestep.

    Example run:
    mean_df,median_df,std_df,min_df = aggregate_runs(df,'timestep')
    '''
    df = df[[x,y]].copy()
    mean_df = df.astype(float).groupby(aggregate_dimension).mean().reset_index()
    median_df = df.astype(float).groupby(aggregate_dimension).median().reset_index()
    std_df = df.astype(float).groupby(aggregate_dimension).std().reset_index()
    min_df = df.astype(float).groupby(aggregate_dimension).min().reset_index()

    return mean_df,median_df,std_df,min_df

# 
def monte_carlo_plot(df,aggregate_dimension,x,y,runs):
    '''
    A function that generates timeseries plot of Monte Carlo runs.

    Parameters:
    df: dataframe name
    aggregate_dimension: the dimension you would like to aggregate on, the standard one is timestep.
    x = x axis variable for plotting
    y = y axis variable for plotting
    run_count = the number of monte carlo simulations

    Example run:
    monte_carlo_plot(df,'timestep','timestep','revenue',run_count=100)
    '''
    mean_df,median_df,std_df,min_df = aggregate_runs(df,aggregate_dimension,x,y)

    plt.figure(figsize=(10,6))
    for r in range(1,runs+1):
        legend_name = 'Run ' + str(r)
        plt.plot(df[df.run==r].timestep, df[df.run==r][y], label = legend_name )
    
    plt.plot(mean_df[x], mean_df[y], label = 'Mean', color = 'black')
    plt.legend(bbox_to_anchor=(1.05, 1), loc=2, borderaxespad=0.)
    plt.xlabel(x)
    plt.ylabel(y)
    title_text = 'Performance of ' + y + ' over ' + str(runs) + ' Monte Carlo Runs'
    plt.title(title_text)

def monte_carlo_plot_st(df,aggregate_dimension,x,y,runs):
    '''
    A function that generates timeseries plot of Monte Carlo runs.

    Parameters:
    df: dataframe name
    aggregate_dimension: the dimension you would like to aggregate on, the standard one is timestep.
    x = x axis variable for plotting
    y = y axis variable for plotting
    run_count = the number of monte carlo simulations

    Example run:
    monte_carlo_plot(df,'timestep','timestep','revenue',run_count=100)
    '''
    fig = plt.figure(figsize=(10,6))
    if runs > 1:
        for r in range(1,runs+1):
            legend_name = 'Run ' + str(r)
            plt.plot(np.asarray(df[df['run'].astype(int)==r].timestep, float), np.asarray(df[df['run'].astype(int)==r][y], float), label = legend_name )
        mean_df,median_df,std_df,min_df = aggregate_runs(df,aggregate_dimension,x,y)
        plt.plot(np.asarray(mean_df[x], float), np.asarray(mean_df[y], float), label = 'Mean', color = 'black')
        plt.legend(bbox_to_anchor=(1.05, 1), loc=2, borderaxespad=0.)
    
    else:
        plt.plot(np.asarray(df[df['run'].astype(int)==1].timestep, float), np.asarray(df[df['run'].astype(int)==1][y], float))
    plt.xlabel(x)
    plt.ylabel(y)
    title_text = 'Performance of ' + y + ' over ' + str(runs) + ' Monte Carlo Runs'
    plt.title(title_text)

    st.pyplot(fig)


def line_plot_plotly(df,x,y_series,run,param_id, x_title=None, y_title=None, info_box=None, plot_title=None, logy=False):
    '''
    A function that generates a line plot from a series of data series in a frame in streamlit
    '''
    chart_datay = pd.DataFrame(np.asarray(df[y_series], float), columns=y_series)
    chart_data = pd.concat([df[x], chart_datay], axis=1)
    y_series_updated = [col for col in y_series if chart_data[col].sum() != 0]
    chart_data = drop_zero_columns(chart_data)

    sys_param_df = get_simulation_data('simulationData.db', 'sys_param')
    sys_param = sys_param_df[sys_param_df['id'] == param_id]

    # cut plot data until the point where ba_cash_balance runs below zero
    if 'ba_cash_balance' in y_series_updated:
        chart_data = chart_data[(chart_data['ba_cash_balance'] > 0) | (chart_data['timestep' if not st.session_state['date_conversion'] else 'date'] == 0)]
        if len(chart_data) < sys_param['simulation_duration'].iloc[0]:
            st.warning(f"The simulation stopped after {len(chart_data)} months, because the business ran out of funds.", icon="⚠️")
    
    if 'reserve_a_tokens' in y_series_updated:
        if len(chart_data[(chart_data['reserve_a_tokens'] > 0) | (chart_data['timestep' if not st.session_state['date_conversion'] else 'date'] == 0)]) < len(chart_data):
            st.warning(f"The simulation stopped after {len(chart_data[chart_data['reserve_a_tokens'] > 0])} months, because the token economy reserve tokens ran to 0.", icon="⚠️")
        chart_data = chart_data[(chart_data['reserve_a_tokens'] > 0) | (chart_data['timestep' if not st.session_state['date_conversion'] else 'date'] == 0)]
    
    if 'community_a_tokens' in y_series_updated:
        if len(chart_data[(chart_data['community_a_tokens'] > 0) | (chart_data['timestep' if not st.session_state['date_conversion'] else 'date'] == 0)]) < len(chart_data):
            st.warning(f"The simulation stopped after {len(chart_data[chart_data['community_a_tokens'] > 0])} months, because the token economy community tokens ran to 0.", icon="⚠️")
        chart_data = chart_data[(chart_data['community_a_tokens'] > 0) | (chart_data['timestep' if not st.session_state['date_conversion'] else 'date'] == 0)]
    
    if 'foundation_a_tokens' in y_series_updated:
        if len(chart_data[(chart_data['foundation_a_tokens'] > 0) | (chart_data['timestep' if not st.session_state['date_conversion'] else 'date'] == 0)]) < len(chart_data):
            st.warning(f"The simulation stopped after {len(chart_data[chart_data['foundation_a_tokens'] > 0])} months, because the token economy foundation tokens ran to 0.", icon="⚠️")
        chart_data = chart_data[(chart_data['foundation_a_tokens'] > 0) | (chart_data['timestep' if not st.session_state['date_conversion'] else 'date'] == 0)]
    
    if 'lp_tokens' in y_series_updated:
        if len(chart_data[(chart_data['lp_tokens'] > 0) | (chart_data['timestep' if not st.session_state['date_conversion'] else 'date'] == 0)]) < len(chart_data):
            st.warning(f"The simulation stopped after {len(chart_data[chart_data['lp_tokens'] > 0])} months, because the token economy liquidity pool tokens ran to 0.", icon="⚠️")
        chart_data = chart_data[(chart_data['lp_tokens'] > 0) | (chart_data['timestep' if not st.session_state['date_conversion'] else 'date'] == 0)]
    
    if 'te_holding_supply' in y_series_updated:
        if len(chart_data[(chart_data['te_holding_supply'] > 0) | (chart_data['timestep' if not st.session_state['date_conversion'] else 'date'] == 0)]) < len(chart_data):
            st.warning(f"The simulation stopped after {len(chart_data[chart_data['te_holding_supply'] > 0])} months, because the token economy holding supply tokens ran to 0.", icon="⚠️")
        chart_data = chart_data[(chart_data['te_holding_supply'] > 0) | (chart_data['timestep' if not st.session_state['date_conversion'] else 'date'] == 0)]
        
    
    # Format the column names
    formatted_columns = [format_column_name(col) for col in [x] + y_series_updated]
    chart_data.columns = formatted_columns
    
    fig = px.line(chart_data, x=format_column_name(x), y=formatted_columns[1:], log_y=logy)

    customize_plotly_figure(fig, x_title, y_title, info_box, plot_title)

    st.plotly_chart(fig, use_container_width=True)

    return len(chart_data)

def vesting_cum_plot_plotly(df,x,y_series,run, param_id, x_title=None, y_title=None, info_box=None, plot_title=None):
    '''
    A function that generates a area plot from vesting series of data series in a frame in streamlit
    '''

    chart_datay = pd.DataFrame(np.asarray(df[y_series], float), columns=y_series)
    chart_data = pd.concat([df[x], chart_datay], axis=1)
    
    y_series_updated = [col for col in y_series if chart_data[col].sum() != 0]
    chart_data = drop_zero_columns(chart_data)

    # Format the column names
    formatted_columns = [format_column_name(col) for col in [x] + y_series_updated]
    chart_data.columns = formatted_columns

    sys_param_df = get_simulation_data('simulationData.db', 'sys_param')
    init_lp_token_alloc = sys_param_df[sys_param_df['id'] == param_id]['initial_lp_token_allocation']
    
    chart_data['Liquidity Pool'] = init_lp_token_alloc.to_list()*len(chart_data)
    chart_data['Liquidity Pool'] = chart_data['Liquidity Pool'].astype(float)

    
    plotly_colors = px.colors.qualitative.Plotly
    color_map = {}
    for i, value in enumerate(chart_data[formatted_columns[1:]+['Liquidity Pool']]):
        try:
            color_map[value] = plotly_colors[i]
        except:
            color_map[value] = plotly_colors[i-len(plotly_colors)]

    fig = px.area(chart_data, x=formatted_columns[0], y=formatted_columns[1:]+['Liquidity Pool'], color_discrete_map=color_map)

    customize_plotly_figure(fig, x_title, y_title, info_box, plot_title)

    st.plotly_chart(fig, use_container_width=True)


def bar_plot_plotly(values_list, param_id, x_title=None, y_title=None, info_box=None, plot_title=None):
    # Check if the values in values_list exist in the DataFrame
    
    sys_param_df = get_simulation_data('simulationData.db', 'sys_param')
    sys_param = sys_param_df[sys_param_df['id'] == param_id]

    df = sys_param[values_list].sum().to_frame(name='Value').reset_index().rename(columns={'index':'Parameter'})
    
    df = df[df['Value'] != 0]

    # Format the 'Parameter' column
    df['Parameter'] = df['Parameter'].apply(format_column_name)

    fig = px.bar(df, x='Parameter', y='Value')

    customize_plotly_figure(fig, x_title, y_title, info_box, plot_title)

    st.plotly_chart(fig, use_container_width=True)

def bar_plot_plotly_from_variables(value_dict, x_title, y_title, info_box=None, plot_title=None):
    # Check if the values in values_list exist in the DataFrame
    
    df = pd.DataFrame.from_dict(value_dict)

    plotly_colors = px.colors.qualitative.Plotly
    color_map = {}
    for i, value in enumerate(df[x_title]):
        try:
            color_map[value] = plotly_colors[i]
        except:
            color_map[value] = plotly_colors[i-len(plotly_colors)]

    fig = px.bar(df, x=x_title, y=y_title, color_discrete_map=color_map)

    customize_plotly_figure(fig, x_title, y_title, info_box, plot_title)

    st.plotly_chart(fig, use_container_width=True)


def pie_plot_plotly(values_list, param_id, x_title=None, y_title=None, info_box=None, plot_title=None):
    # Check if the values in values_list exist in the DataFrame
    
    sys_param_df = get_simulation_data('simulationData.db', 'sys_param')
    sys_param = sys_param_df[sys_param_df['id'] == param_id]

    new_sys_param = sys_param[values_list].copy()
    if 'initial_lp_token_allocation' in values_list:
        new_sys_param['initial_lp_token_allocation'] = float(sys_param['initial_lp_token_allocation']) / float(sys_param['initial_total_supply'])

    df = new_sys_param[values_list].sum().to_frame(name='Value').reset_index().rename(columns={'index':'Parameter'})

    df = drop_zero_columns(df)

    # Format the 'Parameter' column
    df['Parameter'] = df['Parameter'].apply(format_column_name)

    # drop zero parameters
    df = df[df['Value'] != 0]

    plotly_colors = px.colors.qualitative.Plotly
    color_map = {}
    for i, value in enumerate(df['Parameter']):
        try:
            color_map[value] = plotly_colors[i]
        except:
            color_map[value] = plotly_colors[i-len(plotly_colors)]

    fig = px.pie(df, values='Value', names='Parameter', color='Parameter', color_discrete_map=color_map)

    customize_plotly_figure(fig, x_title, y_title, info_box, plot_title)

    st.plotly_chart(fig, use_container_width=True)



def plot_fundraising(param_id):    
    ##FUNDRAISING TAB
    st.session_state['date_conversion'] = st.toggle('Dates Time', value=st.session_state['date_conversion'] if 'date_conversion' in st.session_state else False, help="Use dates as time axis instead of months after token launch.")

    st.markdown('---')
    vesting_cum_plot_results_plotly('timestep' if not st.session_state['date_conversion'] else 'date', ['angel_a_tokens_vested_cum',
                                                 'seed_a_tokens_vested_cum',
                                                 'presale_1_a_tokens_vested_cum',
                                                 'presale_2_a_tokens_vested_cum',
                                                 'public_sale_a_tokens_vested_cum',
                                                 'team_a_tokens_vested_cum',
                                                 'ov_a_tokens_vested_cum',
                                                 'advisor_a_tokens_vested_cum',
                                                 'strategic_partners_a_tokens_vested_cum',
                                                 'reserve_a_tokens_vested_cum',
                                                 'community_a_tokens_vested_cum',
                                                 'foundation_a_tokens_vested_cum',
                                                 'incentivisation_a_tokens_vested_cum',
                                                 'staking_vesting_a_tokens_vested_cum',
                                                 'te_airdrop_tokens_cum'], 1, param_id,
                                                 plot_title="Cumulative Token Vesting", x_title="Months", y_title="Tokens")
    
    st.markdown('---')
    pcol11, pcol12 = st.columns(2)
    with pcol11:
        ##EFFECTIVE TOKEN PRICE
        bar_plot_plotly([
            'angel_token_effective',
            'seed_token_effective',
            'presale_1_token_effective',
            'presale_2_token_effective',
            'public_token_effective'
        ], param_id, plot_title="Effective Token Price for Investors", x_title="Investors", y_title="USD")
    with pcol12:
        ##rrPIE CHART OF INITIAL ALLOCATION
        pie_plot_plotly([
            'angel_token_allocation',
            'seed_token_allocation',
            'presale_1_token_allocation',
            'presale_2_token_allocation',
            'public_sale_token_allocation',
            'team_token_allocation',
            'ov_token_allocation',
            'advisor_token_allocation',
            'strategic_partners_token_allocation',
            'reserve_token_allocation',
            'community_token_allocation',
            'foundation_token_allocation',
            'incentivisation_token_allocation',
            'staking_vesting_token_allocation',
            'airdrop_token_allocation',
            'initial_lp_token_allocation'
        ], param_id, plot_title="Token Allocations")

def plot_business(param_id):    
    ##INPUTS TAB
    st.session_state['date_conversion'] = st.toggle('Dates Time', value=st.session_state['date_conversion'] if 'date_conversion' in st.session_state else False, help="Use dates as time axis instead of months after token launch.")
    sys_param_df = get_simulation_data('simulationData.db', 'sys_param')
    sys_param = sys_param_df[sys_param_df['id'] == param_id]
    max_months = sys_param['simulation_duration'].iloc[0]   
    st.markdown('---')
    max_months = plot_results_plotly('timestep' if not st.session_state['date_conversion'] else 'date', ['ba_cash_balance'], 1, param_id, max_months, plot_title="Business Cash Balance", x_title="Months", y_title="USD")
    st.markdown('---')
    max_months = plot_results_plotly('timestep' if not st.session_state['date_conversion'] else 'date', ['ua_product_users','ua_token_holders'], 1, param_id, max_months, plot_title="User Adoption", x_title="Months", y_title="Count")
    st.markdown('---')
    pcol21, pcol22 = st.columns(2)
    with pcol21:
        max_months = plot_results_plotly('timestep' if not st.session_state['date_conversion'] else 'date', ['ua_product_revenue'], 1, param_id, max_months, plot_title="Product Revenue", x_title="Months", y_title="Revenue per Month / USD")
    with pcol22:
        max_months = plot_results_plotly('timestep' if not st.session_state['date_conversion'] else 'date', ['ua_token_buys'], 1, param_id, max_months, plot_title="Token Buy Pressure", x_title="Months", y_title="Token Buy Pressure per Month / USD")
    st.markdown('---')
    max_months = plot_results_plotly('timestep' if not st.session_state['date_conversion'] else 'date', ['ba_buybacks_usd'], 1, param_id, max_months, plot_title="Token Buybacks", x_title="Months", y_title="Buybacks / USD")
    
    return max_months

def plot_token_economy(param_id, max_months):
    ##ANALYSIS TAB
    st.session_state['date_conversion'] = st.toggle('Dates Time', value=st.session_state['date_conversion'] if 'date_conversion' in st.session_state else False, help="Use dates as time axis instead of months after token launch.")
    # plot token protocol and economy supply buckets
    st.markdown('---')
    with st.expander("**Token Economy and Protocol Buckets**", expanded=True):
        log_scale_toggle_buckets = st.toggle('Log Scale - Protocol Buckets', value=False)
        max_months = plot_results_plotly('timestep' if not st.session_state['date_conversion'] else 'date', ['reserve_a_tokens','community_a_tokens','foundation_a_tokens',
                            'incentivisation_a_tokens','staking_vesting_a_tokens','lp_tokens','te_holding_supply',
                            'te_unvested_supply','te_circulating_supply','te_total_supply'], 1, param_id, max_months
                            , plot_title="Token Supply Buckets", x_title="Months", y_title="Tokens", logy=log_scale_toggle_buckets)
    
    st.markdown('---')
    with st.expander("**Stakeholder Behavior**"):
        pcol31, pcol32 = st.columns(2)
        with pcol31:
            # plot stakeholder holdings
            log_scale_toggle_stakeholder_holdings = st.toggle('Log Scale - Stakeholder Holdings', value=False)
            max_months = plot_results_plotly('timestep' if not st.session_state['date_conversion'] else 'date', ['angel_a_tokens','seed_a_tokens','presale_1_a_tokens',
                                'presale_2_a_tokens','public_sale_a_tokens','team_a_tokens', 'ov_a_tokens',
                                'advisor_a_tokens', 'strategic_partners_a_tokens', 'reserve_a_tokens', 'community_a_tokens', 
                                'foundation_a_tokens', 'market_investors_a_tokens', 'airdrop_receivers_a_tokens',
                                'incentivisation_receivers_a_tokens'], 1, param_id, max_months
                                , plot_title="Stakeholder Holdings", x_title="Months", y_title="Tokens", logy=log_scale_toggle_stakeholder_holdings)
        
        with pcol32:
            # plot stakeholder staked tokens
            log_scale_toggle_stakeholder_staked = st.toggle('Log Scale - Stakeholder Staked Tokens', value=False)
            max_months = plot_results_plotly('timestep' if not st.session_state['date_conversion'] else 'date', ['angel_a_tokens_staked_cum','seed_a_tokens_staked_cum','presale_1_a_tokens_staked_cum',
                                'presale_2_a_tokens_staked_cum','public_sale_a_tokens_staked_cum','team_a_tokens_staked_cum', 'ov_a_tokens_staked_cum',
                                'advisor_a_tokens_staked_cum', 'strategic_partners_a_tokens_staked_cum', 'reserve_a_tokens_staked_cum',
                                'community_a_tokens_staked_cum', 'foundation_a_tokens_staked_cum', 'market_investors_a_tokens_staked_cum',
                                'airdrop_receivers_a_tokens_staked_cum', 'incentivisation_receivers_a_tokens_staked_cum'], 1, param_id, max_months
                                , plot_title="Stakeholder Staked Tokens", x_title="Months", y_title="Tokens", logy=log_scale_toggle_stakeholder_staked)

        
        # plot meta bucket allocations of agents        
        pcol31a, pcol32a = st.columns(2)
        with pcol31a:
            log_scale_toggle_meta_alloc_utility = st.toggle('Log Scale - Utility Meta Bucket Allocations', value=False)
            max_months = plot_results_plotly('timestep' if not st.session_state['date_conversion'] else 'date', ['angel_a_utility_tokens','seed_a_utility_tokens','presale_1_a_utility_tokens',
                                'presale_2_a_utility_tokens','public_sale_a_utility_tokens','team_a_utility_tokens', 'ov_a_utility_tokens',
                                'advisor_a_utility_tokens', 'strategic_partners_a_utility_tokens', 'market_investors_a_utility_tokens',
                                'airdrop_receivers_a_utility_tokens', 'incentivisation_receivers_a_utility_tokens'], 1, param_id, max_months
                                , plot_title="Meta Utility Allocations Tokens per Month From Vesting", x_title="Months", y_title="Tokens", logy=log_scale_toggle_meta_alloc_utility)
        with pcol32a:
            log_scale_toggle_meta_alloc_utility_from_holding = st.toggle('Log Scale - Utility Meta Bucket Allocations From Holding', value=False)
            max_months = plot_results_plotly('timestep' if not st.session_state['date_conversion'] else 'date', ['angel_a_utility_from_holding_tokens','seed_a_utility_from_holding_tokens','presale_1_a_utility_from_holding_tokens',
                                'presale_2_a_utility_from_holding_tokens','public_sale_a_utility_from_holding_tokens','team_a_utility_from_holding_tokens', 'ov_a_utility_from_holding_tokens',
                                'advisor_a_utility_from_holding_tokens', 'strategic_partners_a_utility_from_holding_tokens', 'market_investors_a_utility_from_holding_tokens',
                                'airdrop_receivers_a_utility_from_holding_tokens', 'incentivisation_receivers_a_utility_from_holding_tokens'], 1, param_id, max_months
                                , plot_title="Meta Utility Allocations Tokens per Month From Holding", x_title="Months", y_title="Tokens", logy=log_scale_toggle_meta_alloc_utility_from_holding)

        # plot from holding meta bucket allocations of all agents
        pcol31b, pcol32b = st.columns(2)
        with pcol31b:
            log_scale_toggle_meta_alloc_selling = st.toggle('Log Scale - Selling Meta Bucket Allocations', value=False)
            max_months = plot_results_plotly('timestep' if not st.session_state['date_conversion'] else 'date', ['angel_a_selling_tokens','seed_a_selling_tokens','presale_1_a_selling_tokens',
                                'presale_2_a_selling_tokens','public_sale_a_selling_tokens','team_a_selling_tokens', 'ov_a_selling_tokens',
                                'advisor_a_selling_tokens', 'strategic_partners_a_selling_tokens', 'market_investors_a_selling_tokens',
                                'airdrop_receivers_a_selling_tokens', 'incentivisation_receivers_a_selling_tokens'], 1, param_id, max_months
                                , plot_title="Meta Selling Allocations Tokens per Month From Vesting", x_title="Months", y_title="Tokens", logy=log_scale_toggle_meta_alloc_selling)
        with pcol32b:
            log_scale_toggle_meta_alloc_selling_from_holding = st.toggle('Log Scale - Selling Meta Bucket Allocations From Holding', value=False)
            max_months = plot_results_plotly('timestep' if not st.session_state['date_conversion'] else 'date', ['angel_a_selling_from_holding_tokens','seed_a_selling_from_holding_tokens','presale_1_a_selling_from_holding_tokens',
                                'presale_2_a_selling_from_holding_tokens','public_sale_a_selling_from_holding_tokens','team_a_selling_from_holding_tokens', 'ov_a_selling_from_holding_tokens',
                                'advisor_a_selling_from_holding_tokens', 'strategic_partners_a_selling_from_holding_tokens', 'market_investors_a_selling_from_holding_tokens',
                                'airdrop_receivers_a_selling_from_holding_tokens', 'incentivisation_receivers_a_selling_from_holding_tokens'], 1, param_id, max_months
                                , plot_title="Meta Selling Allocations Tokens per Month From Holding", x_title="Months", y_title="Tokens", logy=log_scale_toggle_meta_alloc_selling_from_holding)

        pcol31c, pcol32c = st.columns(2)
        with pcol31c:
            log_scale_toggle_meta_alloc_holding = st.toggle('Log Scale - Holding Meta Bucket Allocations', value=False)
            max_months = plot_results_plotly('timestep' if not st.session_state['date_conversion'] else 'date', ['angel_a_holding_tokens','seed_a_holding_tokens','presale_1_a_holding_tokens',
                                'presale_2_a_holding_tokens','public_sale_a_holding_tokens','team_a_holding_tokens', 'ov_a_holding_tokens',
                                'advisor_a_holding_tokens', 'strategic_partners_a_holding_tokens', 'market_investors_a_holding_tokens',
                                'airdrop_receivers_a_holding_tokens', 'incentivisation_receivers_a_holding_tokens'], 1, param_id, max_months
                                , plot_title="Meta Holding Allocations Tokens per Month From Vesting", x_title="Months", y_title="Tokens", logy=log_scale_toggle_meta_alloc_holding)
        with pcol32c:
            log_scale_toggle_meta_alloc_holding_from_holding = st.toggle('Log Scale - Holding Meta Bucket Allocations From Holding', value=False)
            max_months = plot_results_plotly('timestep' if not st.session_state['date_conversion'] else 'date', ['angel_a_holding_from_holding_tokens','seed_a_holding_from_holding_tokens','presale_1_a_holding_from_holding_tokens',
                                'presale_2_a_holding_from_holding_tokens','public_sale_a_holding_from_holding_tokens','team_a_holding_from_holding_tokens', 'ov_a_holding_from_holding_tokens',
                                'advisor_a_holding_from_holding_tokens', 'strategic_partners_a_holding_from_holding_tokens', 'market_investors_a_holding_from_holding_tokens',
                                'airdrop_receivers_a_holding_from_holding_tokens', 'incentivisation_receivers_a_holding_from_holding_tokens'], 1, param_id, max_months
                                , plot_title="Meta Holding Allocations Tokens per Month From Holding", x_title="Months", y_title="Tokens", logy=log_scale_toggle_meta_alloc_holding_from_holding)
    
            # plot individual agent meta bucket behavior
        stakeholder_names, stakeholder_mapping = get_stakeholders()
        pcol31d, pcol32d = st.columns(2)
        with pcol31d:
            st.write('**Select Stakeholder 1**')
            pcol31d1, pcol31d2 = st.columns(2)
            with pcol31d1:
                # pick agent
                
                stakeholder1 = st.selectbox('Select Stakeholder 1', [format_column_name(name) for name in stakeholder_names], index=0, label_visibility='collapsed')
                stakeholder1_raw = stakeholder1.replace(' ', '_').lower()
            with pcol31d2:
                # pick meta bucket
                percentage_area1 = st.toggle('Percentage Area 1', value=False)

            area_plot_stakeholder_meta_allocations(param_id, stakeholder1_raw, max_months, percentage_area1)
            max_months = plot_results_plotly('timestep' if not st.session_state['date_conversion'] else 'date', [f'{stakeholder1_raw}_a_tokens_vested_cum', f'{stakeholder1_raw}_a_tokens_airdropped_cum',
                                                          f'{stakeholder1_raw}_a_tokens_incentivised_cum', f'{stakeholder1_raw}_a_tokens_staking_buyback_rewards_cum',
                                                          f'{stakeholder1_raw}_a_tokens_staking_vesting_rewards_cum', f'{stakeholder1_raw}_a_tokens_staking_minting_rewards_cum',
                                                          f'{stakeholder1_raw}_a_tokens_liquidity_mining_rewards_cum'], 1, param_id, max_months
                                , plot_title="Received Tokens Cum.", x_title="Months", y_title="Tokens", logy=False)
            
            max_months = plot_results_plotly('timestep' if not st.session_state['date_conversion'] else 'date', [f'{stakeholder1_raw}_a_tokens_staked_cum', f'{stakeholder1_raw}_a_tokens_liquidity_mining_cum',
                                                          f'{stakeholder1_raw}_a_tokens_transferred_cum', f'{stakeholder1_raw}_a_tokens_burned_cum'], 1, param_id, max_months
                                , plot_title="Allocated Tokens Cum.", x_title="Months", y_title="Tokens", logy=False)
        
        with pcol32d:
            st.write('**Select Stakeholder 2**')
            pcol32d1, pcol32d2 = st.columns(2)
            with pcol32d1:
                # pick agent
                stakeholder2 = st.selectbox('Select Stakeholder 2', [format_column_name(name) for name in stakeholder_names], index=1, label_visibility='collapsed')
                stakeholder2_raw = stakeholder2.replace(' ', '_').lower()
            with pcol32d2:
                # pick meta bucket
                percentage_area2 = st.toggle('Percentage Area 2', value=False)

            area_plot_stakeholder_meta_allocations(param_id, stakeholder2_raw, max_months, percentage_area2)
            max_months = plot_results_plotly('timestep' if not st.session_state['date_conversion'] else 'date', [f'{stakeholder2_raw}_a_tokens_vested_cum', f'{stakeholder2_raw}_a_tokens_airdropped_cum',
                                                          f'{stakeholder2_raw}_a_tokens_incentivised_cum', f'{stakeholder2_raw}_a_tokens_staking_buyback_rewards_cum',
                                                          f'{stakeholder2_raw}_a_tokens_staking_vesting_rewards_cum', f'{stakeholder2_raw}_a_tokens_staking_minting_rewards_cum',
                                                          f'{stakeholder2_raw}_a_tokens_liquidity_mining_rewards_cum'], 1, param_id, max_months
                                , plot_title="Received Tokens Cum.", x_title="Months", y_title="Tokens", logy=False)
            
            max_months = plot_results_plotly('timestep' if not st.session_state['date_conversion'] else 'date', [f'{stakeholder2_raw}_a_tokens_staked_cum', f'{stakeholder2_raw}_a_tokens_liquidity_mining_cum',
                                                          f'{stakeholder2_raw}_a_tokens_transferred_cum', f'{stakeholder2_raw}_a_tokens_burned_cum'], 1, param_id, max_months
                                , plot_title="Allocated Tokens Cum.", x_title="Months", y_title="Tokens", logy=False)

    st.markdown('---')
    with st.expander("**Utility Allocations**"):
        pie_plot_plotly(['staking_share','liquidity_mining_share','burning_share',
                        'holding_share','transfer_share'], param_id, plot_title="Token Utility Share")
        
        pcol51, pcol52 = st.columns(2)
        with pcol51:
            pcol51a, pcol52a = st.columns(2)
            with pcol51a:
                log_scale_toggle_utility_alloc = st.toggle('Log Scale - Utility Allocations', value=False)
            with pcol52a:
                toggle_usd_utility_alloc = st.toggle('Convert to USD - Utility Allocations', value=False)
            if toggle_usd_utility_alloc:
                max_months = plot_results_plotly('timestep' if not st.session_state['date_conversion'] else 'date', ['u_staking_allocation_usd',
                                'u_liquidity_mining_allocation_usd','u_burning_allocation_usd','u_transfer_allocation_usd','te_incentivised_tokens_usd',
                                'te_airdrop_tokens_usd'], 1, param_id, max_months
                                , calcColumns= {'u_staking_allocation_usd': {'sign': '*', 'firstCol': 'u_staking_allocation', 'secondCol': 'lp_token_price'},
                                                'u_liquidity_mining_allocation_usd': {'sign': '*', 'firstCol': 'u_liquidity_mining_allocation', 'secondCol': 'lp_token_price'},
                                                'u_burning_allocation_usd': {'sign': '*', 'firstCol': 'u_burning_allocation', 'secondCol': 'lp_token_price'},
                                                'u_transfer_allocation_usd': {'sign': '*', 'firstCol': 'u_transfer_allocation', 'secondCol': 'lp_token_price'},
                                                'te_incentivised_tokens_usd': {'sign': '*', 'firstCol': 'te_incentivised_tokens', 'secondCol': 'lp_token_price'},
                                                'te_airdrop_tokens_usd': {'sign': '*', 'firstCol': 'te_airdrop_tokens', 'secondCol': 'lp_token_price'}}
                                , plot_title="Token Allocations By Utilities", x_title="Months", y_title="USD", logy=log_scale_toggle_utility_alloc)
            else:
                max_months = plot_results_plotly('timestep' if not st.session_state['date_conversion'] else 'date', ['u_staking_allocation',
                                                'u_liquidity_mining_allocation','u_burning_allocation','u_transfer_allocation','te_incentivised_tokens',
                                                'te_airdrop_tokens'], 1, param_id, max_months
                                                , plot_title="Token Allocations By Utilities", x_title="Months", y_title="Tokens", logy=log_scale_toggle_utility_alloc)
        with pcol52:
            pcol51b, pcol52b = st.columns(2)
            with pcol51b:
                log_scale_toggle_utility_alloc_cum = st.toggle('Log Scale - Utility Allocations Cum.', value=False)
            with pcol52b:
                toggle_usd_utility_alloc_cum = st.toggle('Convert to USD - Utility Allocations Cum.', value=False)
            if toggle_usd_utility_alloc_cum:
                max_months = plot_results_plotly('timestep' if not st.session_state['date_conversion'] else 'date', ['u_staking_allocation_usd_cum', 'u_liquidity_mining_allocation_usd_cum',
                                'u_burning_allocation_usd_cum','u_transfer_allocation_usd_cum','te_incentivised_tokens_usd_cum','te_airdrop_tokens_usd_cum'], 1, param_id, max_months
                                , calcColumns= {'u_staking_allocation_usd_cum': {'sign': '*', 'firstCol': 'u_staking_allocation_cum', 'secondCol': 'lp_token_price'},
                                                'u_liquidity_mining_allocation_usd_cum': {'sign': '*', 'firstCol': 'u_liquidity_mining_allocation_cum', 'secondCol': 'lp_token_price'},
                                                'u_burning_allocation_usd_cum': {'sign': '*', 'firstCol': 'u_burning_allocation_cum', 'secondCol': 'lp_token_price'},
                                                'u_transfer_allocation_usd_cum': {'sign': '*', 'firstCol': 'u_transfer_allocation_cum', 'secondCol': 'lp_token_price'},
                                                'te_incentivised_tokens_usd_cum': {'sign': '*', 'firstCol': 'te_incentivised_tokens_cum', 'secondCol': 'lp_token_price'},
                                                'te_airdrop_tokens_usd_cum': {'sign': '*', 'firstCol': 'te_airdrop_tokens_cum', 'secondCol': 'lp_token_price'}}
                                , plot_title="Cumulative Token Allocations By Utilities", x_title="Months", y_title="USD", logy=log_scale_toggle_utility_alloc_cum)
            else:
                max_months = plot_results_plotly('timestep' if not st.session_state['date_conversion'] else 'date', ['u_staking_allocation_cum', 'u_liquidity_mining_allocation_cum',
                                                'u_burning_allocation_cum','u_transfer_allocation_cum','te_incentivised_tokens_cum','te_airdrop_tokens_cum'], 1, param_id, max_months
                                                , plot_title="Cumulative Token Allocations By Utilities", x_title="Months", y_title="Tokens", logy=log_scale_toggle_utility_alloc_cum)


    st.markdown('---')
    with st.expander("**Token Incentives**"):
        pcol61, pcol62 = st.columns(2)
        with pcol61:
            pcol61a, pcol62a = st.columns(2)
            with pcol61a:
                log_scale_toggle_token_incentives = st.toggle('Log Scale - Token Incentives', value=True)
            with pcol62a:
                toggle_usd_token_incentives = st.toggle('Convert to USD - Token Incentives', value=False)
            if toggle_usd_token_incentives:
                max_months = plot_results_plotly('timestep' if not st.session_state['date_conversion'] else 'date', ['u_staking_revenue_share_rewards_usd', 'u_staking_vesting_rewards_usd', 'u_staking_minting_rewards_usd', 'u_liquidity_mining_rewards_usd'], 1, param_id, max_months
                                                , calcColumns={'u_staking_revenue_share_rewards_usd': {'sign': '*', 'firstCol': 'u_staking_revenue_share_rewards', 'secondCol': 'lp_token_price'},
                                                                'u_staking_vesting_rewards_usd': {'sign': '*', 'firstCol': 'u_staking_vesting_rewards', 'secondCol': 'lp_token_price'},
                                                                'u_staking_minting_rewards_usd': {'sign': '*', 'firstCol': 'u_staking_minting_rewards', 'secondCol': 'lp_token_price'},
                                                                'u_liquidity_mining_rewards_usd': {'sign': '*', 'firstCol': 'u_liquidity_mining_rewards', 'secondCol': 'lp_token_price'}}
                                                , plot_title="USD Token Incentives", x_title="Months", y_title="USD", logy=log_scale_toggle_token_incentives)
            else:
                max_months = plot_results_plotly('timestep' if not st.session_state['date_conversion'] else 'date', ['u_staking_revenue_share_rewards', 'u_staking_vesting_rewards', 'u_staking_minting_rewards', 'u_liquidity_mining_rewards'], 1, param_id, max_months
                                , plot_title="Token Incentives", x_title="Months", y_title="Tokens", logy=log_scale_toggle_token_incentives)
        with pcol62:
            log_scale_toggle_staking_apr = st.toggle('Log Scale - Staking APR', value=True)
            max_months = plot_results_plotly('timestep' if not st.session_state['date_conversion'] else 'date', ['te_staking_apr'], 1, param_id, max_months
                                        , plot_title="Staking APR / %", x_title="Months", y_title="APR / %", logy=log_scale_toggle_staking_apr)
            
    st.markdown('---')
    with st.expander("**Token Valuations**"):
        pcol41, pcol42 = st.columns(2)
        with pcol41:
            log_scale_toggle_lp_token_price = st.toggle('Log Scale - Token Price', value=True)
            max_months = plot_results_plotly('timestep' if not st.session_state['date_conversion'] else 'date', ['lp_token_price'], 1, param_id, max_months
                                , plot_title="Token Price", x_title="Months", y_title="USD", logy=log_scale_toggle_lp_token_price)
        with pcol42:
            log_scale_toggle_valuations = st.toggle('Log Scale - Valuations', value=True)
            max_months = plot_results_plotly('timestep' if not st.session_state['date_conversion'] else 'date', ['lp_valuation','te_MC','te_FDV_MC'], 1, param_id, max_months
                                , plot_title="Valuations", x_title="Months", y_title="USD", logy=log_scale_toggle_valuations)

def utility_pie_plot(utility_shares, utility_values):

    df = pd.DataFrame.from_dict(utility_shares, orient='index', columns=['Share / %']).reset_index().rename(columns={'index':'Utility'})

    plotly_colors = px.colors.qualitative.Plotly
    color_map = {}
    for i, value in enumerate(df['Utility']):
        try:
            color_map[value] = plotly_colors[i]
        except:
            color_map[value] = plotly_colors[i-len(plotly_colors)]

    fig = px.pie(df, values='Share / %', names='Utility', color='Utility', color_discrete_map=color_map)

    st.plotly_chart(fig, use_container_width=True)

