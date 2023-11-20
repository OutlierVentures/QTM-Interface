import matplotlib.pyplot as plt
import pandas as pd
import streamlit as st
import numpy as np
import sys, os
import sqlite3
import plotly.figure_factory as ff
import plotly.express as px
import plotly.graph_objects as go





def customize_plotly_figure(fig, x_title=None, y_title=None, info_box=None, plot_title=None):
    # Set the axes titles
    if x_title:
        fig.update_xaxes(title_text=x_title)
    if y_title:
        fig.update_yaxes(title_text=y_title)


    # Add a plot title
    if plot_title:
        fig.update_layout(title_text=plot_title, title_x=0.5)  # Adjust title_x as needed

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
    name_with_spaces = column_name.replace('_a_', ' ').replace('tokens_vested_cum', '').replace('_token_effective','').replace('_token_allocation','').replace('ua_','').replace('ba_','').replace('te_','').replace('lp_tokens', 'Liquidity Pool').replace('lp_valuation','Liquidity Pool').replace('_supply','').replace('tokens','').replace('lp_','').replace('u_','').replace('_cum','').replace('allocation','').replace('_', ' ')
    
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

def plot_results_plotly(x, y_columns, run, param_id, max_months, x_title=None, y_title=None, info_box=None, plot_title=None, logy=False):

    df = get_simulation_data('simulationData.db', 'simulation_data_'+param_id)

    # reduce df to max_months
    df = df[df['timestep'].astype(float) <= max_months]

    # example for Monte Carlo plots
    #monte_carlo_plot_st(df,'timestep','timestep','seed_a_tokens_vested_cum',3)

    # example for line plots of different outputs in one figure
    new_max_months = line_plot_plotly(df,x, y_columns, run, x_title=x_title, y_title=y_title, info_box=info_box, plot_title=plot_title ,logy=logy)
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


def line_plot_plotly(df,x,y_series,run, x_title=None, y_title=None, info_box=None, plot_title=None, logy=False):
    '''
    A function that generates a line plot from a series of data series in a frame in streamlit
    '''
    chart_data = pd.DataFrame(np.asarray(df[[x]+y_series], float), columns=[x]+y_series)
    y_series_updated = [col for col in y_series if chart_data[col].sum() != 0]
    chart_data = drop_zero_columns(chart_data)

    # cut plot data until the point where ba_cash_balance runs below zero
    if 'ba_cash_balance' in y_series_updated:
        chart_data = chart_data[chart_data['ba_cash_balance'] > 0]
        if len(chart_data) < 120:
            st.error(f"The simulation stopped after {len(chart_data)} months, because the business ran out of funds.", icon="⚠️")
    
    if 'reserve_a_tokens' in y_series_updated:
        if len(chart_data[chart_data['reserve_a_tokens'] > 0]) < len(chart_data):
            st.error(f"The simulation stopped after {len(chart_data[chart_data['reserve_a_tokens'] > 0])} months, because the token economy reserve tokens ran to 0.", icon="⚠️")
        chart_data = chart_data[chart_data['reserve_a_tokens'] > 0]
    
    if 'community_a_tokens' in y_series_updated:
        if len(chart_data[chart_data['community_a_tokens'] > 0]) < len(chart_data):
            st.error(f"The simulation stopped after {len(chart_data[chart_data['community_a_tokens'] > 0])} months, because the token economy community tokens ran to 0.", icon="⚠️")
        chart_data = chart_data[chart_data['community_a_tokens'] > 0]
    
    if 'foundation_a_tokens' in y_series_updated:
        if len(chart_data[chart_data['foundation_a_tokens'] > 0]) < len(chart_data):
            st.error(f"The simulation stopped after {len(chart_data[chart_data['foundation_a_tokens'] > 0])} months, because the token economy foundation tokens ran to 0.", icon="⚠️")
        chart_data = chart_data[chart_data['foundation_a_tokens'] > 0]
    
    if 'lp_tokens' in y_series_updated:
        if len(chart_data[chart_data['lp_tokens'] > 0]) < len(chart_data):
            st.error(f"The simulation stopped after {len(chart_data[chart_data['lp_tokens'] > 0])} months, because the token economy liquidity pool tokens ran to 0.", icon="⚠️")
        chart_data = chart_data[chart_data['lp_tokens'] > 0]
    
    if 'te_holding_supply' in y_series_updated:
        if len(chart_data[chart_data['te_holding_supply'] > 0]) < len(chart_data):
            st.error(f"The simulation stopped after {len(chart_data[chart_data['te_holding_supply'] > 0])} months, because the token economy holding supply tokens ran to 0.", icon="⚠️")
        chart_data = chart_data[chart_data['te_holding_supply'] > 0]
        
    
    # Format the column names
    formatted_columns = [format_column_name(col) for col in [x] + y_series_updated]
    chart_data.columns = formatted_columns
    
    fig = px.line(chart_data, x=formatted_columns[0], y=formatted_columns[1:], log_y=logy)

    customize_plotly_figure(fig, x_title, y_title, info_box, plot_title)

    st.plotly_chart(fig, use_container_width=True)

    return len(chart_data)

def vesting_cum_plot_plotly(df,x,y_series,run, param_id, x_title=None, y_title=None, info_box=None, plot_title=None):
    '''
    A function that generates a area plot from vesting series of data series in a frame in streamlit
    '''

    chart_data = pd.DataFrame(np.asarray(df[[x]+y_series], float), columns=[x]+y_series)
    
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
    vesting_cum_plot_results_plotly('timestep', ['angel_a_tokens_vested_cum',
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
    max_months = 120   
    max_months = plot_results_plotly('timestep', ['ba_cash_balance'], 1, param_id, max_months, plot_title="Business Cash Balance", x_title="Months", y_title="USD")
    max_months = plot_results_plotly('timestep', ['ua_product_users','ua_token_holders'], 1, param_id, max_months, plot_title="User Adoption", x_title="Months", y_title="Count")
    pcol21, pcol22 = st.columns(2)
    with pcol21:
        max_months = plot_results_plotly('timestep', ['ua_product_revenue'], 1, param_id, max_months, plot_title="Product Revenue", x_title="Months", y_title="Revenue per Month / USD")
    with pcol22:
        max_months = plot_results_plotly('timestep', ['ua_token_buys'], 1, param_id, max_months, plot_title="Token Buy Pressure", x_title="Months", y_title="Token Buy Pressure per Month / USD")
    
    return max_months

def plot_token_economy(param_id, max_months):
    ##ANALYSIS TAB
    log_scale_toggle_buckets = st.toggle('Log Scale - Protocol Buckets', value=False)
    max_months = plot_results_plotly('timestep', ['reserve_a_tokens','community_a_tokens','foundation_a_tokens',
                        'incentivisation_a_tokens','staking_vesting_a_tokens','lp_tokens','te_holding_supply',
                        'te_unvested_supply','te_circulating_supply'], 1, param_id, max_months
                        , plot_title="Token Supply Buckets", x_title="Months", y_title="Tokens", logy=log_scale_toggle_buckets)
    
    pcol31, pcol32 = st.columns(2)
    with pcol31:
        log_scale_toggle_lp_token_price = st.toggle('Log Scale - Token Price', value=True)
        max_months = plot_results_plotly('timestep', ['lp_token_price'], 1, param_id, max_months
                            , plot_title="Token Price", x_title="Months", y_title="USD", logy=log_scale_toggle_lp_token_price)
    with pcol32:
        log_scale_toggle_valuations = st.toggle('Log Scale - Valuations', value=True)
        max_months = plot_results_plotly('timestep', ['lp_valuation','te_MC','te_FDV_MC'], 1, param_id, max_months
                            , plot_title="Valuations", x_title="Months", y_title="USD", logy=log_scale_toggle_valuations)
    
    pie_plot_plotly(['staking_share','liquidity_mining_share','burning_share',
                     'holding_share','transfer_share'], param_id, plot_title="Token Utility Share")
    
    pcol41, pcol42 = st.columns(2)
    with pcol41:
        log_scale_toggle_utility_alloc = st.toggle('Log Scale - Utility Allocations', value=True)
        max_months = plot_results_plotly('timestep', ['u_staking_allocation',
                                        'u_liquidity_mining_allocation','u_burning_allocation','u_transfer_allocation','te_incentivised_tokens',
                                        'te_airdrop_tokens','te_holding_allocation'], 1, param_id, max_months
                                        , plot_title="Token Allocations By Utilities", x_title="Months", y_title="Tokens", logy=log_scale_toggle_utility_alloc)
    with pcol42:
        log_scale_toggle_utility_alloc_cum = st.toggle('Log Scale - Utility Allocations Cum.', value=True)
        max_months = plot_results_plotly('timestep', ['u_staking_allocation_cum', 'u_liquidity_mining_allocation_cum',
                                        'u_burning_allocation_cum','u_transfer_allocation_cum','te_incentivised_tokens_cum','te_airdrop_tokens_cum',
                                        'te_holding_allocation_cum'], 1, param_id, max_months
                                        , plot_title="Cumulative Token Allocations By Utilities", x_title="Months", y_title="Tokens", logy=log_scale_toggle_utility_alloc_cum)
    
    log_scale_toggle_staking_apr = st.toggle('Log Scale - Staking APR', value=True)
    max_months = plot_results_plotly('timestep', ['te_staking_apr'], 1, param_id, max_months
                                        , plot_title="Staking APR / %", x_title="Months", y_title="APR / %", logy=log_scale_toggle_staking_apr)

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

