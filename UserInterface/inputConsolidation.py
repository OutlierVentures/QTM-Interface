import streamlit as st
from UserInterface.plots import *
from Model.parts.utils import *
import pandas as pd
import random
from . import basicTokenInformation as bti
from . import fundraising as fr
from . import tokenAllocationsAndVesting as tav
from . import userAdoption as ua
from . import agentBehavior as ab
from . import businessAssumptions as ba
from . import utilities as ut
from . import tokenInMarketInitialization as timi
from . import consistencyChecks as cc


def model_ui_inputs(input_file_path, uploaded_file, parameter_list, col01):
    if 'param_id' in st.session_state:
        parameter_id_choice = st.session_state['param_id']
    else:
        parameter_id_choice = ""

    # Adjusting Parameters
    if parameter_id_choice == "":
        sys_param = compose_initial_parameters(pd.read_csv(input_file_path), parameter_list)
        sys_param['avg_token_utility_allocation'] = [sys_param['avg_token_utility_allocation'][0] / 100]
        sys_param['avg_token_holding_allocation'] = [sys_param['avg_token_holding_allocation'][0] / 100]
        sys_param['avg_token_selling_allocation'] = [sys_param['avg_token_selling_allocation'][0] / 100]
        sys_param['avg_token_utility_removal'] = [sys_param['avg_token_utility_removal'][0] / 100]
    else:
        sys_param_df = get_simulation_data('simulationData.db', 'sys_param')
        if len(sys_param_df[sys_param_df['id'] == parameter_id_choice])<1:
            sys_param = compose_initial_parameters(pd.read_csv(input_file_path), parameter_list)
        else:
            sys_param = {k:[v] for k, v in sys_param_df[sys_param_df['id'] == parameter_id_choice].to_dict('index')[list(sys_param_df[sys_param_df['id'] == parameter_id_choice].to_dict('index').keys())[0]].items()}

    with col01:
        token_launch_date = st.date_input("Token Launch Date", value=datetime.strptime(sys_param['launch_date'][0], "%d.%m.%Y"), help="The token launch date is the time when the token becomes liquid to be traded and at which the vesting conditions start to apply. Defining a date before today's date means that the token has already been launched and therefore requires additional information about the current token distribution and valuations in the parameter definitions below.")
        token_launch_date = datetime(token_launch_date.year, token_launch_date.month, token_launch_date.day)
        if token_launch_date > datetime.today():
            token_launch = True
        else:
            token_launch = False


    ##############################################
    # Basic Token Information
    ##############################################

    bti_return_dict = bti.basicTokenInformationInput(sys_param)


    ##############################################
    # Fundraising
    ##############################################
    
    fr_return_dict = fr.fundraisingInput(sys_param, bti_return_dict["equity_investments"], bti_return_dict["equity_perc"], bti_return_dict["public_sale_supply"], bti_return_dict["launch_valuation"], bti_return_dict["initial_supply"], uploaded_file)

    ##############################################
    # Token Allocations and Vesting
    ##############################################

    tav_return_dict = tav.tokenAllocationsAndVestingInput(sys_param, bti_return_dict["equity_perc"], fr_return_dict["seed_raised"], fr_return_dict["presale_1_raised"], fr_return_dict["presale_2_raised"], fr_return_dict["public_sale_raised"], fr_return_dict["raised_funds"], bti_return_dict["launch_valuation"], fr_return_dict["seed_valuation"], fr_return_dict["presale_1_valuation"], fr_return_dict["presale_2_valuation"], bti_return_dict["initial_supply"], token_launch_date, token_launch)


    ##############################################
    # User Adoption
    ##############################################

    ua_return_dict = ua.userAdoptionInput(sys_param, tav_return_dict)


    ##############################################
    # Agent Behavior
    ##############################################

    ab_return_dict = ab.agentBehaviorInput(sys_param, ua_return_dict["adoption_style"], ua_return_dict["adoption_dict"])


    ##############################################
    # Business Assumptions
    ##############################################

    ba_return_dict = ba.businessAssumptionsInput(sys_param, ua_return_dict["adoption_dict"], token_launch_date, fr_return_dict["raised_funds"], token_launch, tav_return_dict["incentivisation_toggle"], tav_return_dict["staking_vesting_toggle"], ua_return_dict["adoption_style"], ua_return_dict["regular_product_revenue_per_user"], ua_return_dict["initial_product_users"], ua_return_dict["show_full_adoption_table"])


    ##############################################
    # Utilities
    ##############################################

    ut_return_dict = ut.utilitiesInput(sys_param, tav_return_dict, ab_return_dict, ua_return_dict)


    ##############################################
    # Token In-Market Initialization
    ##############################################

    timi_return_dict = timi.tokenInMarketInitializationInput(token_launch_date, token_launch, bti_return_dict, ut_return_dict, ab_return_dict, tav_return_dict, sys_param)


    ##############################################
    # Parameter Assignments
    ##############################################

    # Map new parameters to model input parameters
    new_params = {
        'usermail': st.session_state["authenticator"].credentials["usernames"][st.session_state["username"]]["email"],
        'token_launch': token_launch,
        'launch_date': token_launch_date.strftime("%d.%m.%Y").split(" ")[0],
        'equity_external_shareholders_perc': bti_return_dict['equity_perc'],
        'initial_total_supply': bti_return_dict['initial_supply']*1e6,
        'public_sale_supply_perc': bti_return_dict['public_sale_supply'],
        'public_sale_valuation': bti_return_dict['launch_valuation'] * 1e6,
        'angel_raised': bti_return_dict['equity_investments'] * 1e6,
        'fundraising_style': fr_return_dict["fundraising_style"],
        'seed_raised': fr_return_dict["seed_raised"]* 1e6,
        'presale_1_raised': fr_return_dict["presale_1_raised"]* 1e6,
        'presale_2_raised': fr_return_dict["presale_2_raised"]* 1e6,
        'public_sale_raised': fr_return_dict["public_sale_raised"]* 1e6,
        'seed_valuation': fr_return_dict["seed_valuation"]* 1e6,
        'presale_1_valuation': fr_return_dict["presale_1_valuation"]* 1e6,
        'presale_2_valuation': fr_return_dict["presale_2_valuation"]* 1e6,
        'vesting_style': tav_return_dict['vesting_style'],
        'angel_initial_vesting': tav_return_dict['angel_initial_vesting'],
        'angel_cliff': tav_return_dict['angel_cliff'],
        'angel_vesting_duration': tav_return_dict['angel_duration'],
        'seed_initial_vesting': tav_return_dict['seed_initial_vesting'],
        'seed_cliff': tav_return_dict['seed_cliff'],
        'seed_vesting_duration': tav_return_dict['seed_duration'],
        'presale_1_initial_vesting': tav_return_dict['presale_1_initial_vesting'],
        'presale_1_cliff': tav_return_dict['presale_1_cliff'],
        'presale_1_vesting_duration': tav_return_dict['presale_1_duration'],
        'presale_2_initial_vesting': tav_return_dict['presale_2_initial_vesting'],
        'presale_2_cliff': tav_return_dict['presale_2_cliff'],
        'presale_2_vesting_duration': tav_return_dict['presale_2_duration'],
        'public_sale_initial_vesting': tav_return_dict['public_sale_initial_vesting'],
        'public_sale_cliff': tav_return_dict['public_sale_cliff'],
        'public_sale_vesting_duration': tav_return_dict['public_sale_duration'],
        'team_allocation': tav_return_dict['team_allocation'],
        'team_initial_vesting': tav_return_dict['team_initial_vesting'],
        'team_cliff': tav_return_dict['team_cliff'],
        'team_vesting_duration': tav_return_dict['team_duration'],
        'ov_allocation': 0,
        'ov_initial_vesting': 0,
        'ov_cliff': 0,
        'ov_vesting_duration': 0,
        'advisor_allocation': tav_return_dict['ov_advisor_allocation'],
        'advisor_initial_vesting': tav_return_dict['advisor_initial_vesting'],
        'advisor_cliff': tav_return_dict['advisor_cliff'],
        'advisor_vesting_duration': tav_return_dict['advisor_duration'],
        'strategic_partners_allocation': tav_return_dict['strategic_partners_allocation'],
        'strategic_partners_initial_vesting': tav_return_dict['strategic_partners_initial_vesting'],
        'strategic_partners_cliff': tav_return_dict['strategic_partners_cliff'],
        'strategic_partners_vesting_duration': tav_return_dict['strategic_partners_duration'],
        'reserve_allocation': tav_return_dict['reserve_allocation'],
        'reserve_initial_vesting': tav_return_dict['reserve_initial_vesting'],
        'reserve_cliff': tav_return_dict['reserve_cliff'],
        'reserve_vesting_duration': tav_return_dict['reserve_duration'],
        'community_allocation': tav_return_dict['community_allocation'],
        'community_initial_vesting': tav_return_dict['community_initial_vesting'],
        'community_cliff': tav_return_dict['community_cliff'],
        'community_vesting_duration': tav_return_dict['community_duration'],
        'foundation_allocation': tav_return_dict['foundation_allocation'],
        'foundation_initial_vesting': tav_return_dict['foundation_initial_vesting'],
        'foundation_cliff': tav_return_dict['foundation_cliff'],
        'foundation_vesting_duration': tav_return_dict['foundation_duration'],
        'incentivisation_allocation': tav_return_dict['incentivisation_allocation'],
        'incentivisation_initial_vesting': tav_return_dict['incentivisation_initial_vesting'],
        'incentivisation_cliff': tav_return_dict['incentivisation_cliff'],
        'incentivisation_vesting_duration': tav_return_dict['incentivisation_duration'],
        'staking_vesting_allocation': tav_return_dict['staking_vesting_allocation'],
        'staking_vesting_initial_vesting': tav_return_dict['staking_vesting_initial_vesting'],
        'staking_vesting_cliff': tav_return_dict['staking_vesting_cliff'],
        'staking_vesting_vesting_duration': tav_return_dict['staking_vesting_duration'],
        'airdrop_allocation': tav_return_dict['airdrop_allocation'],
        'airdrop_date1': [tav_return_dict['airdrop_date1'].strftime('%d.%m.%Y') if tav_return_dict['airdrop_toggle'] else sys_param['airdrop_date1'][0]][0],
        'airdrop_amount1': [tav_return_dict['airdrop_amount1'] if tav_return_dict['airdrop_toggle'] else sys_param['airdrop_amount1'][0]][0],
        'airdrop_date2': [tav_return_dict['airdrop_date2'].strftime('%d.%m.%Y') if tav_return_dict['airdrop_toggle'] else sys_param['airdrop_date2'][0]][0],
        'airdrop_amount2': [tav_return_dict['airdrop_amount2'] if tav_return_dict['airdrop_toggle'] else sys_param['airdrop_amount2'][0]][0],
        'airdrop_date3': [tav_return_dict['airdrop_date3'].strftime('%d.%m.%Y') if tav_return_dict['airdrop_toggle'] else sys_param['airdrop_date3'][0]][0],
        'airdrop_amount3': [tav_return_dict['airdrop_amount3'] if tav_return_dict['airdrop_toggle'] else sys_param['airdrop_amount3'][0]][0],
        'adoption_style': ua_return_dict["adoption_style"] if not ua_return_dict["show_full_adoption_table"] else 'Custom',
        'initial_product_users': ua_return_dict["initial_product_users"],
        'initial_token_holders': ua_return_dict["initial_token_holders"],
        'product_users_after_10y': ua_return_dict["product_users_after_10y"],
        'token_holders_after_10y': ua_return_dict["token_holders_after_10y"],
        'product_adoption_velocity': ua_return_dict["product_adoption_velocity"],
        'token_adoption_velocity': ua_return_dict["token_adoption_velocity"],
        'regular_product_revenue_per_user': ua_return_dict["regular_product_revenue_per_user"],
        'regular_token_buy_per_user': ua_return_dict["regular_token_buy_per_user"],
        'agent_behavior': ab_return_dict["agent_behavior"],
        'avg_token_utility_allocation': ab_return_dict["avg_token_utility_allocation"],
        'avg_token_selling_allocation': ab_return_dict["avg_token_selling_allocation"],
        'avg_token_holding_allocation': ab_return_dict["avg_token_holding_allocation"],
        'avg_token_utility_removal': ab_return_dict["avg_token_utility_removal"] if (ua_return_dict["adoption_style"] == 'Custom' or ua_return_dict["show_full_adoption_table"]) and ab_return_dict["agent_behavior"] == 'static' else ua_return_dict["adoption_dict"][ua_return_dict["adoption_style"]]['avg_token_utility_removal'] if ab_return_dict["agent_behavior"] == 'static' else 0,
        'royalty_income_per_month': ba_return_dict["royalty_income_per_month"] *1e3,
        'treasury_income_per_month': ba_return_dict["treasury_income_per_month"] *1e3,
        'other_income_per_month': ba_return_dict["other_income_per_month"]*1e3,
        'one_time_payments_1': ba_return_dict["one_time_payments_1"]*1e3,
        'salaries_per_month': ba_return_dict["salaries_per_month"]*1e3,
        'license_costs_per_month': ba_return_dict["license_costs_per_month"]*1e3,
        'other_monthly_costs': ba_return_dict["other_monthly_costs"]*1e3,
        'buyback_perc_per_month': ba_return_dict["buyback_perc_per_month"],
        'buyback_fixed_per_month': ba_return_dict["buyback_fixed_per_month"]*1e3,
        'buyback_bucket': ba_return_dict["buyback_bucket"],
        'buyback_start': ba_return_dict["buyback_start"].strftime('%d.%m.%Y'),
        'buyback_end': ba_return_dict["buyback_end"].strftime('%d.%m.%Y'),
        'burn_per_month': ba_return_dict["burn_per_month"],
        'burn_bucket': ba_return_dict["burn_bucket"],
        'burn_start': ba_return_dict["burn_start"].strftime('%d.%m.%Y'),
        'burn_end': ba_return_dict["burn_end"].strftime('%d.%m.%Y'),
        'business_rev_share' : ua_return_dict["business_rev_share"],
        'service_provider_rev_share' : ua_return_dict["service_provider_rev_share"],
        'incentivisation_rev_share' : ua_return_dict["incentivisation_rev_share"],
        'staker_rev_share_buyback' : ua_return_dict["staker_rev_share_buyback"],
        'incentivisation_rev_share_buyback' : ua_return_dict["incentivisation_rev_share_buyback"],
        'user_adoption_target': ua_return_dict["user_adoption_target"],
    }

    # add utility parameters to new_params
    new_params.update(ut_return_dict["utility_parameter_choice"])

    # add random seed to new_params
    if ab_return_dict["agent_behavior"] == 'simple':
        new_params['random_seed'] = ab_return_dict["random_seed"]
        new_params['S_B'] = ab_return_dict["S_B"]
        new_params['S_e'] = ab_return_dict["S_e"]
        new_params['S_0'] = ab_return_dict["S_0"]

    # add in-market initialization parameters to new_params
    if not token_launch:
        new_params['initial_total_supply'] = timi_return_dict["current_initial_supply"]*1e6
        new_params.update({
            'token_fdv': timi_return_dict["token_fdv"]*1e6,
            'token_holding_ratio_share': timi_return_dict["token_holding_ratio_share"],
            'lp_allocation_tokens': timi_return_dict["lp_allocation_tokens"]*1e6
        })
        # add current_holdings, current_staked, and vested_dict dict entries to new_params
        for stakeholder in timi_return_dict["vested_dict"]:
            if tav_return_dict['vesting_dict'][stakeholder]['allocation'] > 0:
                new_params.update({
                    f'{stakeholder if stakeholder is not "incentivisation" else "incentivisation_receivers"}_current_holdings': timi_return_dict["current_holdings"][stakeholder if stakeholder is not 'incentivisation' else 'incentivisation_receivers']*1e6,
                    f'{stakeholder if stakeholder is not "incentivisation" else "incentivisation_receivers"}_current_staked': timi_return_dict["current_staked"][stakeholder if stakeholder is not 'incentivisation' else 'incentivisation_receivers']*1e6,
                    f'{stakeholder}_vested_init': timi_return_dict["vested_dict"][stakeholder]*1e6,
                })
        # add airdrop receivers to new_params
        if tav_return_dict['airdrop_toggle']:
            new_params.update({
                'airdrop_receivers_current_holdings': timi_return_dict["current_holdings"]['airdrop_receivers']*1e6,
                'airdrop_receivers_current_staked': timi_return_dict["current_staked"]['airdrop_receivers']*1e6,
                'airdrop_receivers_vested_init': 0,
            })

        # add market investors to new_params
        new_params.update({
            'market_investors_current_holdings': timi_return_dict["current_holdings"]['market_investors']*1e6,
            'market_investors_current_staked': timi_return_dict["current_staked"]['market_investors']*1e6,
            'market_investors_vested_init': timi_return_dict["current_holdings"]['market_investors']*1e6 + timi_return_dict["current_staked"]['market_investors']*1e6,
        })
        new_params['initial_cash_balance'] = ba_return_dict["initial_cash_balance"]*1e3

    ##############################################
    # Consistency Checks
    ##############################################

    cc.consistencyChecksInfo(token_launch, token_launch_date, tav_return_dict, ab_return_dict, ut_return_dict, ba_return_dict, ua_return_dict, timi_return_dict, fr_return_dict)

    col111, col112, col113, col114, col115 = st.columns(5)
    with col111:
        simulation_duration = st.number_input('Simulation Duration / Months', label_visibility="visible", min_value=1, value=int(sys_param['simulation_duration'][0]) if 'simulation_duration' in sys_param else 60, disabled=False, key="simulation_duration", help="The duration of the simulation in months. Note that longer simulation times require more computation time.")
        new_params.update({'simulation_duration': simulation_duration})

    return new_params