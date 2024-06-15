from datetime import datetime
from io import BytesIO
from pyxlsb import open_workbook as open_xlsb
import pandas as pd
import streamlit as st
import sqlite3
import numpy as np
import os
from PIL import Image
import time
import yaml
from brownian_motion_generator import brownian_motion_generator as bmg
import yfinance as yf

from Model.parts.utils import *
from UserInterface.plots import *
from UserInterface.persist import persist, load_widget_state



def delete_parameter_and_simulation_data(param_id):
    # delete current selected parameter set and simulation data from database
    conn = sqlite3.connect('simulationData.db')
    cur = conn.cursor()
    try:
        cur.execute(''' DELETE FROM simulation_data_{param_id} '''.format(param_id=param_id))
    except:
        pass
    try:
        cur.execute(''' DELETE FROM sys_param WHERE id = ? ''', (param_id,))
    except:
        pass
    conn.commit()
    conn.close()

def calc_vested_tokens_for_stakeholder(token_launch_date, initial_supply, vesting_dict):
    vested_supply_sum = 0
    vested_dict = {}
    
    # use the vesting dictionary to calculate the vested supply for each stakeholder considering the current date, the token_launch_date, the initial vesting, the cliff and the vesting duration
    passed_months = np.abs(int(months_difference(token_launch_date, datetime.today())))
    
    for stakeholder in vesting_dict:
        allocation = vesting_dict[stakeholder]['allocation']
        initial_vesting = vesting_dict[stakeholder]['initial_vesting']
        cliff = vesting_dict[stakeholder]['cliff']
        duration = vesting_dict[stakeholder]['duration']
        if passed_months <= cliff:
            vested_supply = initial_vesting/100 * allocation/100 * initial_supply
        elif passed_months <= duration + cliff:
            vested_supply = initial_vesting/100 * allocation/100 * initial_supply + ((passed_months - cliff) / duration) * (allocation/100 * (1-initial_vesting/100)) * initial_supply
        else:
            vested_supply = allocation/100 * initial_supply
        vested_supply_sum += vested_supply
        vested_dict[stakeholder] = vested_supply
    
    return vested_dict, vested_supply_sum

def calc_airdropped_tokens(token_launch_date, initial_supply, airdrop_allocation, airdrop_dict):
    airdropped_supply_sum = 0

    for airdrop in airdrop_dict:
        amount = airdrop_dict[airdrop]['amount']
        date = datetime.strptime(airdrop_dict[airdrop]['date'], "%d.%m.%Y")
        if date > token_launch_date and date < datetime.today():
            airdropped_supply_sum += amount/100 * airdrop_allocation/100 * initial_supply

    remaining_airdrop_supply = initial_supply * airdrop_allocation / 100 - airdropped_supply_sum
    
    return airdropped_supply_sum, remaining_airdrop_supply

def to_excel(df):
    output = BytesIO()
    writer = pd.ExcelWriter(output, engine='xlsxwriter')
    df.to_excel(writer, index=False, sheet_name='Sheet1')
    workbook = writer.book
    worksheet = writer.sheets['Sheet1']
    format1 = workbook.add_format({'num_format': '0.00'}) 
    worksheet.set_column('A:A', None, format1)  
    writer.save()
    processed_data = output.getvalue()
    return processed_data

def ui_base(return_db_sorted=False):
    load_widget_state()
    # get all existing scenario names
    try:
        db_sorted_original = get_simulation_data('simulationData.db', 'sys_param').sort_values('project_name', ascending=True)
        # suppose that the 'usermail' field can contain multiple mail addresses, separated by a comma. Now we want to filter the database by the current usermail
        db_sorted = db_sorted_original.copy()
        db_sorted['usermail'] = db_sorted['usermail'].str.split(',')
        db_sorted = db_sorted.explode('usermail')
        db_sorted = db_sorted[db_sorted['usermail'] == st.session_state["authenticator"].credentials["usernames"][st.session_state["username"]]["email"]] if st.session_state["username"] != 'admin' else db_sorted
        project_names = db_sorted['project_name'] if st.session_state["username"] != 'admin' else db_sorted_original['project_name']
        project_names = project_names.to_list()
        project_names.append('')
    except:
        db_sorted = pd.DataFrame()
        project_names = ['']
    if 'project_name' not in st.session_state:
        st.session_state['project_name'] = ''


    if 'project_name' in st.session_state and 'param_id' in st.session_state and len(db_sorted) > 0:
        try:
            st.session_state['project_name'] = st.sidebar.selectbox('Scenario Name', tuple(project_names), key=persist('ProjectName'))
        except:
            st.sidebar.info("Please refresh the page and login again to get access to the project menu.", icon="ℹ️")
        try:
            st.session_state['param_id'] = db_sorted[db_sorted['project_name']==st.session_state['project_name']]['id'].iloc[0]      
        except:
            st.session_state['param_id'] = ''
        try:
            # add button to open up a rename field to rename the current project
            if st.session_state['project_name'] != '':
                if st.sidebar.button('Rename Scenario'):
                    st.session_state['rename_scenario_button_clicked'] = True
                if 'rename_scenario_button_clicked' in st.session_state and st.session_state['rename_scenario_button_clicked']:
                    new_project_name = st.sidebar.text_input('New Scenario Name', st.session_state['project_name'])
                    if st.sidebar.button('Save'):
                        # check if the new project name is already in the database
                        if new_project_name in project_names:
                            st.sidebar.warning(f'⚠️The scenario name {new_project_name} already exists.')
                        else:
                            conn = sqlite3.connect('simulationData.db')
                            cur = conn.cursor()
                            cur.execute(''' UPDATE sys_param SET project_name = ? WHERE id = ? ''', (new_project_name, st.session_state['param_id']))
                            conn.commit()
                            conn.close()
                            st.session_state['project_name'] = new_project_name
                            st.session_state['rename_scenario_button_clicked'] = False
                            st.sidebar.success(f'Scenario name changed to {new_project_name} ✅.')
                            st.experimental_rerun()
        except:
            pass
    else:
        try:
            st.session_state['project_name'] = st.sidebar.selectbox('Scenario Name', tuple(project_names), index=len(project_names)-1, key=persist('ProjectName'))
        except:
            st.sidebar.info("Please refresh the page and login again to get access to the project menu.", icon="ℹ️")
        
        st.session_state['param_id'] = ''

    if 'project_name' in st.session_state and 'param_id' in st.session_state and len(db_sorted) > 0:
        newMailAccess = st.sidebar.text_input('Share Dataset with Email', "")
        st.sidebar.button('Share Dataset', on_click=shareDataSet, args=(newMailAccess,))
    
    if return_db_sorted:
        return db_sorted

def returnToStart():
    st.write("You are not logged in. Please log in on the Welcome page to access this page.")

def shareDataSet(newMailAccess):
    # add the new mail address to the list of mail addresses in the "usermail" column of the database by adding a comma behind the last entered one
    conn = sqlite3.connect('simulationData.db')
    cur = conn.cursor()
    cur.execute(''' SELECT usermail FROM sys_param WHERE id = ? ''', (st.session_state['param_id'],))
    usermail = cur.fetchone()[0]
    st.sidebar.info(f"Current shared mail addresses of this dataset: {usermail}", icon="ℹ️")
    st.sidebar.info(f"Try to add: {newMailAccess}", icon="ℹ️")
    if newMailAccess in usermail:
        st.sidebar.warning(f'⚠️The dataset has already been shared with {newMailAccess}.')
        return
    if not '@' in newMailAccess:
        st.sidebar.warning(f'⚠️Please enter a valid mail address to share the dataset.')
        return
    usermail = usermail + ',' + newMailAccess
    cur.execute(''' UPDATE sys_param SET usermail = ? WHERE id = ? ''', (usermail, st.session_state['param_id']))
    conn.commit()
    conn.close()
    st.sidebar.success(f'Dataset shared with {newMailAccess} ✅. The user needs to create an account with that mail address and log in to access the dataset.')

def header(basePath):
    hcol1, hcol2 = st.columns([10,2])
    with hcol1:
        image = Image.open(f'{basePath}/images/ov_logo.jpg')
        st.image(image, width=125)
        st.title('Quantitative Token Model')
    with hcol2:
        if "authentication_status" in st.session_state:
            if st.session_state["authentication_status"]:
                st.session_state["authenticator"].logout('Logout', 'main', key='unique_key')
                st.write(f'✅ *{st.session_state["name"]}*')
                    

def safeToYaml(config):
    # safe to yaml file
    with open('./config.yaml', 'w') as file:
        yaml.dump(config, file, default_flow_style=False)


def simulate_market_returns(coin, start_date, end_date, runs=1): 

    # Map input string to compatible token symbol for the data fetching
    coin_mapping = {'bitcoin': 'BTC', 'ethereum': 'ETH'}

    # Convert the input coin string to the corresponding API symbol
    coin = coin_mapping.get(coin.lower())

    # Retrieve selected timestep in main UI page
    timesteps = st.session_state.get('simulation_duration') 

    # Fetch asset price data using the yfinance library
    ticker = yf.Ticker(f'{coin}-USD') 
    data = ticker.history(start=start_date, end=end_date, interval="1mo")["Close"]
    
    # Check if data is empty
    if data.empty:
        print("Failed to fetch data or no data available for the given range and asset.")
        return 

    # Convert Series to DataFrame and rename column for easier manipulation
    df = data.to_frame(name='Close Price')

    # Calculate monthly log returns for better mathematical operations 
    df['Log returns'] = np.log(df['Close Price'] / df['Close Price'].shift(1))
    df = df.dropna(how='any')

    # Approximate the distribution parameters of each series
    # Here we will use a custom distribution for each: other options include 'normal' or 'laplace'
    OU_params = bmg.estimate_OU_params(df['Log returns'].values, distribution_type='custom')

    # Since only one process and one run, we don't need a tuple for parameters or correlations
    OU_procs = bmg.simulate_corr_OU_procs(timesteps, (OU_params,), runs, rho=None)

    # runs, timesteps, data = OU_procs.shape
    OU_procs_arr = np.column_stack((np.repeat(np.arange(runs), timesteps), OU_procs.reshape(runs * timesteps, -1)))
    walks = pd.DataFrame(OU_procs_arr, columns=['run', 'Log returns'])
    walks['run'] = walks['run'].astype(int) + 1
    walks['timestep'] = walks.groupby('run').cumcount() + 1

    return {'market': walks} 