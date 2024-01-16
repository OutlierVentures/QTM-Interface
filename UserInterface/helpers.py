from datetime import datetime
from Model.parts.utils import *
from io import BytesIO
from pyxlsb import open_workbook as open_xlsb
import pandas as pd

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