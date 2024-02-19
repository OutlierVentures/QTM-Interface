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

from Model.parts.utils import *
from UserInterface.plots import *

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

def ui_base(parent_dir, return_db_sorted=False):
    # get all existing project names
    try:
        db_sorted = get_simulation_data('simulationData.db', 'sys_param').sort_values('project_name', ascending=True)
        # suppose that the 'usermail' field can contain multiple mail addresses, separated by a comma. Now we want to filter the database by the current usermail
        db_sorted['usermail'] = db_sorted['usermail'].str.split(',')
        db_sorted = db_sorted.explode('usermail')
        db_sorted = db_sorted[db_sorted['usermail'] == st.session_state["authenticator"].credentials["usernames"][st.session_state["username"]]["email"]] if st.session_state["username"] != 'admin' else db_sorted
        project_names = db_sorted['project_name']
        project_names = project_names.to_list()
        project_names.append('')
    except:
        db_sorted = pd.DataFrame()
        project_names = ['']
    if 'project_name' not in st.session_state:
        st.session_state['project_name'] = ''

    if 'project_name' in st.session_state and 'param_id' in st.session_state and len(db_sorted) > 0:
        st.session_state['project_name'] = st.sidebar.selectbox('Project Name', tuple(project_names), index=[db_sorted['id'].to_list().index(st.session_state['param_id']) if st.session_state['param_id'] in db_sorted['id'].to_list() else len(project_names)-1][0])
        st.session_state['param_id'] = st.sidebar.text_input('Parameter ID',[db_sorted[db_sorted['project_name']==st.session_state['project_name']]['id'].iloc[0] if st.session_state['project_name'] in db_sorted['project_name'].to_list() else ""][0])
    else:
        st.session_state['project_name'] = st.sidebar.selectbox('Project Name', tuple(project_names), index=len(project_names)-1)
        st.session_state['param_id'] = st.sidebar.text_input('Parameter ID', "")

    try:
        if st.session_state['param_id'] not in get_simulation_data('simulationData.db', 'sys_param')['id'].to_list():
            st.sidebar.markdown(f"Parameter ID: {st.session_state['param_id']} does not exist. Please enter a valid parameter ID or run the simulation with your parameter set to get a parameter ID.")
        else:
            st.sidebar.markdown(f"This is a valid parameter ID ✅")
    except:
        pass

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