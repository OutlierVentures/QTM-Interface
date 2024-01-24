from Model.parts.utils import *
import pandas as pd
import sqlite3
import streamlit as st
from collections import Counter
import sys
import os

# Get the current directory
current_dir = os.path.dirname(os.path.abspath(__file__))

# Go up one folder
parent_dir = os.path.abspath(os.path.join(current_dir, os.pardir))

# Append the parent directory to sys.path
sys.path.append(parent_dir)
from data.not_iterable_variables import parameter_list

def get_stakeholders():
    # calculating the initial values for the different agents
    stakeholder_names = [
        'angel',
        'seed',
        'presale_1',
        'presale_2',
        'public_sale',
        'team',
        'ov',
        'advisor',
        'strategic_partners',
        'reserve',
        'community',
        'foundation',
        'incentivisation',
        'staking_vesting',
        'market_investors',
        'airdrop_receivers',
        'incentivisation_receivers'
    ]

    # defining the mapping between the stakeholder names and their type categories
    stakeholder_name_mapping = {
        'angel': 'early_investor',
        'seed': 'early_investor',
        'presale_1': 'early_investor',
        'presale_2': 'early_investor',
        'public_sale': 'early_investor',
        'team': 'team',
        'ov': 'early_investor',
        'advisor': 'early_investor',
        'strategic_partners': 'early_investor',
        'reserve': 'protocol_bucket',
        'community': 'protocol_bucket',
        'foundation': 'protocol_bucket',
        'incentivisation': 'protocol_bucket',
        'staking_vesting': 'protocol_bucket',
        'market_investors': 'market_investors',
        'airdrop_receivers': 'airdrop_receivers',
        'incentivisation_receivers': 'incentivisation_receivers',
    }
    return stakeholder_names, stakeholder_name_mapping

def get_sys_param(input_file, adjusted_params):

    QTM_inputs = pd.read_csv(input_file)

    # System parameters
    sys_param = compose_initial_parameters(QTM_inputs, parameter_list)

    # adjusting parameters w.r.t. adjusted_params dictionary
    if len(adjusted_params) > 0:
        for key, value in adjusted_params.items():
            print("Changed parameter: " + key + " to " + str(value))
            sys_param[key] = [value]

    # calculating the token allocations for different agents
    agent_token_allocation = {
        'angel_token_allocation': [x/100 * (y/100 / (1-x/100)) for x in sys_param['equity_external_shareholders_perc'] for y in sys_param['team_allocation']],
        'seed_token_allocation' : calculate_investor_allocation(sys_param, "seed"),
        'presale_1_token_allocation' : calculate_investor_allocation(sys_param, "presale_1"),
        'presale_2_token_allocation' : calculate_investor_allocation(sys_param, "presale_2"),
        'public_sale_token_allocation' : [(x/100)for x in sys_param['public_sale_supply_perc']],
        'team_token_allocation' : [x / 100 for x in sys_param['team_allocation']],
        'ov_token_allocation' : [x / 100 for x in sys_param['ov_allocation']],
        'advisor_token_allocation' : [x / 100 for x in sys_param['advisor_allocation']],
        'strategic_partners_token_allocation' : [x / 100 for x in sys_param['strategic_partners_allocation']],
        'reserve_token_allocation' : [x / 100 for x in sys_param['reserve_allocation']],
        'community_token_allocation' : [x / 100 for x in sys_param['community_allocation']],
        'foundation_token_allocation' : [x / 100 for x in sys_param['foundation_allocation']],
        'incentivisation_token_allocation' : [x / 100 for x in sys_param['incentivisation_allocation']],
        'staking_vesting_token_allocation' : [x / 100 for x in sys_param['staking_vesting_allocation']],
        'airdrop_token_allocation' : [x / 100 for x in sys_param['airdrop_allocation']],
        'market_token_allocation' : [0],
        'airdrop_receivers_token_allocation' : [0],
        'incentivisation_receivers_token_allocation' : [0]
    }

    sys_param.update(agent_token_allocation)

    # calculating the initial values for the liquidity pool
    if 'token_launch' in sys_param.keys() and not sys_param['token_launch'][0]:
        initial_lp_token_allocation = [sys_param['lp_allocation_tokens'][0]]
        token_fdv = sys_param['token_fdv'][0]
        initial_total_supply = sys_param['initial_total_supply'][0]
        initial_required_usdc = [token_fdv / initial_total_supply * initial_lp_token_allocation[0]]
    else:
        initial_lp_token_allocation = calc_initial_lp_tokens(agent_token_allocation, sys_param)
        initial_required_usdc = [x * y for x in initial_lp_token_allocation for y in [x / y for x in sys_param['public_sale_valuation'] for y in sys_param['initial_total_supply']]]
    
    liquidity_pool_initial_values = {
        'initial_token_price': [x / y for x in sys_param['public_sale_valuation'] for y in sys_param['initial_total_supply']],
        'initial_lp_token_allocation': initial_lp_token_allocation,
        'initial_required_usdc': initial_required_usdc
    }
    sys_param.update(liquidity_pool_initial_values)

    stakeholder_names, stakeholder_name_mapping = get_stakeholders()

    # setting initial values for user adoption
    user_adoption_initial_values = {
        'initial_product_users' : [x for x in sys_param['initial_product_users']],
        'product_users_after_10y' : [x for x in sys_param['product_users_after_10y']],
        'product_adoption_velocity' : [x for x in sys_param['product_adoption_velocity']],
        'one_time_product_revenue_per_user' : [x for x in sys_param['one_time_product_revenue_per_user']],
        'regular_product_revenue_per_user' : [x for x in sys_param['regular_product_revenue_per_user']],
        'initial_token_holders' : [x for x in sys_param['initial_token_holders']],
        'token_holders_after_10y' : [x for x in sys_param['token_holders_after_10y']],
        'token_adoption_velocity' : [x for x in sys_param['token_adoption_velocity']],
        'one_time_token_buy_per_user' : [x for x in sys_param['one_time_token_buy_per_user']],
        'regular_token_buy_per_user' : [x for x in sys_param['regular_token_buy_per_user']],
        'avg_token_utility_allocation' : [x / 100 for x in sys_param['avg_token_utility_allocation']],
        'avg_token_holding_allocation' : [x / 100 for x in sys_param['avg_token_holding_allocation']],
        'avg_token_selling_allocation' : [x / 100 for x in sys_param['avg_token_selling_allocation']],
        'avg_token_utility_removal' : [x / 100 for x in sys_param['avg_token_utility_removal']]

    }

    # updating parameters with user adoption data
    sys_param.update(user_adoption_initial_values)

    # setting nitial values for business assumptions
    business_assumptions_initial_values = {
        'product_income_per_month': [x for x in sys_param['product_income_per_month']],
        'royalty_income_per_month': [x for x in sys_param['royalty_income_per_month']],
        'other_income_per_month': [x for x in sys_param['other_income_per_month']],
        'treasury_income_per_month': [x for x in sys_param['treasury_income_per_month']],
        'regular_income_sum': [x for x in sys_param['regular_income_sum']],
        'one_time_payments_1': [x for x in sys_param['one_time_payments_1']],
        'one_time_payments_2': [x for x in sys_param['one_time_payments_2']],
        'salaries_per_month': [x for x in sys_param['salaries_per_month']],
        'license_costs_per_month': [x for x in sys_param['license_costs_per_month']],
        'other_monthly_costs': [x for x in sys_param['other_monthly_costs']],
        'buyback_type': [x for x in sys_param['buyback_type']],
        'buyback_perc_per_month': [x for x in sys_param['buyback_perc_per_month']],
        'buyback_fixed_per_month': [x for x in sys_param['buyback_fixed_per_month']],
        'buyback_bucket': [x for x in sys_param['buyback_bucket']],
        'buyback_start': [x for x in sys_param['buyback_start']],
        'buyback_end': [x for x in sys_param['buyback_end']],
        'burn_per_month': [x for x in sys_param['burn_per_month']],
        'burn_start': [x for x in sys_param['burn_start']],
        'burn_end': [x for x in sys_param['burn_end']],
        'burn_project_bucket': [x for x in sys_param['burn_project_bucket']]
    }

    # updating business assumptions parameters
    sys_param.update(business_assumptions_initial_values)

    # setting initial values for utility parameters
    utility_initial_values = {
        'staking_share': [x for x in sys_param['staking_share']],
        'liquidity_mining_share': [x for x in sys_param['liquidity_mining_share']],
        'burning_share': [x for x in sys_param['burning_share']],
        'holding_share': [x for x in sys_param['holding_share']],
        'transfer_share': [x for x in sys_param['transfer_share']],
        'staker_rev_share': [x for x in sys_param['staker_rev_share']],
        'mint_burn_ratio' : [x for x in sys_param['mint_burn_ratio']],
        'liquidity_mining_apr': [x for x in sys_param['liquidity_mining_apr']],
        'liquidity_mining_payout_source': [x for x in sys_param['liquidity_mining_payout_source']],
        'holding_apr': [x for x in sys_param['holding_apr']],
        'holding_payout_source': [x for x in sys_param['holding_payout_source']],
        'transfer_destination': [x for x in sys_param['transfer_destination']],
        'incentivisation_payout_source': [x for x in sys_param['incentivisation_payout_source']]
    }

    # updating utility parameters
    sys_param.update(utility_initial_values)

    agent_effective_price = {
        'angel_token_effective': [x/100 for x in sys_param['equity_external_shareholders_perc']],
        'seed_token_effective' : calculate_investor_effective_token_price(sys_param, "seed"),
        'presale_1_token_effective' : calculate_investor_effective_token_price(sys_param, "presale_1"),
        'presale_2_token_effective' : calculate_investor_effective_token_price(sys_param, "presale_2"),
        'public_token_effective' : [x / y for x in sys_param["public_sale_valuation"] for y in sys_param["initial_total_supply"]]
    }

    sys_param.update(agent_effective_price)
    
    execute_sim = True
    # save parameter to sqlite db
    conn = sqlite3.connect('simulationData.db')
    # Save the sys_param DataFrame to a new SQLite table if these parameter combination does not exist yet
    # check if sys_param table exists
    cur = conn.cursor()
    listOfTables = cur.execute(''' SELECT count(name) FROM sqlite_master WHERE type='table' AND name='sys_param' ''')
    if listOfTables.fetchall()[0][0] == 0:
        # create unique identifier for this parameter set
        param_id = str(uuid.uuid4()).replace("-", "")
        sys_param['id'] = [param_id]
        if 'project_name' in sys_param.keys():
            if sys_param['project_name'][0] in ["", " ", "  ", "   ", "    ", "     "]:
                st.error(f"Please provide a project name before running the simulation!", icon="⚠️")
                execute_sim = False
        if execute_sim:
            sys_param_df = pd.DataFrame(sys_param)
            sys_param_df.to_sql('sys_param', conn, if_exists='replace', index=False)
            print("Create new table!")
    else:
        print("Get parameter data from table..")
        df = pd.read_sql(f'SELECT * FROM sys_param', conn)
        df_old = df.loc[:, df.columns != 'id']
        df_new = pd.DataFrame(sys_param)

        # comparing dataframes
        if not df_new[df_new.columns].values[0].tolist() in df_old[df_old.columns].values[:].tolist():
            print("New parameter set detected!")
            param_id = str(uuid.uuid4()).replace("-", "")
            sys_param['id'] = [param_id]
            if 'project_name' in sys_param.keys() and 'project_name' in df.columns:
                if sys_param['project_name'][0] in df['project_name'].to_list():
                    st.warning(f"Project name {sys_param['project_name'][0]} already exists in database. Please choose a different project name and run the simulation again.", icon="⚠️")
                    execute_sim = False
                if sys_param['project_name'][0] in ["", " ", "  ", "   ", "    ", "     "]:
                    st.error(f"Please provide a project name before running the simulation!", icon="⚠️")
                    execute_sim = False
            if execute_sim:
                sys_param_df = pd.concat([df, pd.DataFrame(sys_param)])
                sys_param_df.to_sql('sys_param', conn, if_exists='replace', index=False)
        else:
            print("Already existing parameter set detected! Getting its id..")
            # get id of already existing parameter set that equals to the current one
            same_row_idx = [i for i, x in enumerate(list(df_old[df_old.columns].values[:])) if Counter(x) == Counter(list(df_new[df_new.columns].values[0]))][0]
            param_id = df.iloc[same_row_idx]['id']

    print("Parameter ID of current simulation: ", param_id)

    return sys_param, stakeholder_name_mapping, stakeholder_names, conn, cur, param_id, execute_sim

    