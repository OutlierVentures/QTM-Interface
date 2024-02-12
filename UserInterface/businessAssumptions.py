import streamlit as st
import numpy as np
from Model.parts.utils import months_difference
from datetime import datetime

def businessAssumptionsInput(sys_param, adoption_dict, token_launch_date, raised_funds, token_launch, incentivisation_toggle, staking_vesting_toggle, adoption_style, regular_product_revenue_per_user, initial_product_users, show_full_adoption_table):
    """
    This function creates the business assumptions section of the UI.
    """
    with st.expander("**Business Assumptions**"):
        st.markdown("### Business Assumptions")
        # income | expenditures | buybacks | burns
        st.write("**Financial Streams**")
        col81, col82, col83 = st.columns(3)
        with col81:
            show_full_business_table = st.toggle('Use Full Custom Table', value=False, help="Show the full financial stream parameter set. Note that all income streams from the table will be added on top of the adoption product revenue.")
            if not show_full_business_table:
                income = st.number_input('Additional income per month / $k', label_visibility="visible", min_value=0.0, value=float(sys_param['royalty_income_per_month'][0] + sys_param['other_income_per_month'][0] + sys_param['treasury_income_per_month'][0])/1e3, disabled=False, key="income", help="The monthly income for the business on top of the product revenue, defined in the user adoption section.")
                expenditures = st.number_input('Expenditures per month / $k', label_visibility="visible", min_value=0.0, value=float(sys_param['salaries_per_month'][0] + sys_param['license_costs_per_month'][0] + sys_param['other_monthly_costs'][0] + (sys_param['one_time_payments_1'][0]+ sys_param['one_time_payments_2'][0])/120)/1e3, disabled=False, key="expenditures", help="The monthly expenditures for the business.")
            else:
                income = 0.0
                expenditures = 0.0
        if show_full_business_table:
            with col82:
                st.write("**Income**")
                royalty_income_per_month = st.number_input('Royalty income per month / $k', label_visibility="visible", min_value=0.0, value=[float(sys_param['royalty_income_per_month'][0])/1e3 if show_full_business_table else 0.0][0], disabled=False, key="royalty_income_per_month", help="The monthly royalty income for the business.")
                treasury_income_per_month = st.number_input('Treasury income per month / $k', label_visibility="visible", min_value=0.0, value=[float(sys_param['treasury_income_per_month'][0])/1e3 if show_full_business_table else 0.0][0], disabled=False, key="treasury_income_per_month", help="The monthly income for the business from treasury investments yields.")
                other_income_per_month = st.number_input('Other income per month / $k', label_visibility="visible", min_value=0.0, value=[float(sys_param['other_income_per_month'][0])/1e3 if show_full_business_table else 0.0][0], disabled=False, key="other_income_per_month", help="The monthly income for the business from other sources.")
            with col83:
                st.write("**Expenditures**")
                one_time_payments_1 = st.number_input('One-time payments / $k', label_visibility="visible", min_value=0.0, value=[float(sys_param['one_time_payments_1'][0] + sys_param['one_time_payments_2'][0])/1e3 if show_full_business_table else 0.0][0], disabled=False, key="one_time_payments_1", help="The one-time payments for the business at launch (e.g. any back payment of liabilities or treasury investments).")
                salaries_per_month = st.number_input('Salaries per month / $k', label_visibility="visible", min_value=0.0, value=[float(sys_param['salaries_per_month'][0])/1e3 if show_full_business_table else 0.0][0], disabled=False, key="salaries_per_month", help="The monthly salaries paid by the business.")
                license_costs_per_month = st.number_input('License costs per month / $k', label_visibility="visible", min_value=0.0, value=[float(sys_param['license_costs_per_month'][0])/1e3 if show_full_business_table else 0.0][0], disabled=False, key="license_costs_per_month", help="The monthly license costs paid by the business.")
                other_monthly_costs = st.number_input('Other monthly costs / $k', label_visibility="visible", min_value=0.0, value=[float(sys_param['other_monthly_costs'][0])/1e3 if show_full_business_table else 0.0][0], disabled=False, key="other_monthly_costs", help="The monthly costs paid by the business for other purposes.")
        else:
            royalty_income_per_month = [float(sys_param['royalty_income_per_month'][0])/1e3 if income == 0.0 else 0.0][0]
            treasury_income_per_month = [float(sys_param['treasury_income_per_month'][0])/1e3 if income == 0.0 else 0.0][0]
            other_income_per_month = [float(sys_param['other_income_per_month'][0])/1e3 if income == 0.0 else income][0]
            one_time_payments_1 = [float(sys_param['one_time_payments_1'][0] + sys_param['one_time_payments_2'][0])/1e3 if expenditures == 0.0 else 0.0][0]
            salaries_per_month = [float(sys_param['salaries_per_month'][0])/1e3 if expenditures == 0.0 else 0.0][0]
            license_costs_per_month = [float(sys_param['license_costs_per_month'][0])/1e3 if expenditures == 0.0 else 0.0][0]
            other_monthly_costs = [float(sys_param['other_monthly_costs'][0])/1e3 if expenditures == 0.0 else expenditures][0]
        
        if not token_launch:
            months_since_launch = np.abs(int(months_difference(token_launch_date, datetime.today())))
            projected_cash_balance = raised_funds*1e3 - one_time_payments_1 + (royalty_income_per_month + treasury_income_per_month + other_income_per_month - salaries_per_month - license_costs_per_month - other_monthly_costs) * months_since_launch
            initial_cash_balance = st.number_input('Financial Reserves / $k', label_visibility="visible", min_value=0.0, value=float(sys_param['initial_cash_balance'][0])/1e3 if 'initial_cash_balance' in sys_param else projected_cash_balance if projected_cash_balance > 0 else 0.0, format="%.5f", disabled=False, key="initial_cash_balance", help="The financial reserves of the business today. The financial reserves determine the runway of the business.")
            if initial_cash_balance == 0 and (royalty_income_per_month + treasury_income_per_month + other_income_per_month + initial_product_users * (regular_product_revenue_per_user if adoption_style == 'Custom' or show_full_adoption_table else adoption_dict[adoption_style]['regular_product_revenue_per_user']) - salaries_per_month - license_costs_per_month - other_monthly_costs) < 0:
                st.error(f"The financial reserves are 0 and the monthly expenditures are greater than the revenues. Increase the initial cash reserves to achieve a proper financial runway!", icon="⚠️")
        else:
            initial_cash_balance = 0.0


        st.write("**Buybacks and Burns**")
        col91, col92 = st.columns(2)
        with col91:
            enable_protocol_buybacks = st.toggle('Enable Protocol Token Buybacks', value=float(sys_param['buyback_perc_per_month'][0]) > 0 or float(sys_param['buyback_fixed_per_month'][0]) > 0, help="Enable the buyback of tokens to refill a protocol bucket.")
            if enable_protocol_buybacks:
                buyback_type = st.radio('Buyback Type',('Fixed', 'Percentage'), index=0, help='The buyback type determines the buyback behavior of the business. A fixed buyback means that the business buys back a fixed USD worth amount of tokens per month. A percentage buyback means that the business buys back a percentage USD worth amount of tokens per month, depending on the business funds.')
                if buyback_type == 'Fixed':
                    buyback_fixed_per_month = st.number_input('Buyback per month / $k', label_visibility="visible", value=[float(sys_param['buyback_fixed_per_month'][0])/1e3 if enable_protocol_buybacks else 0.0][0], disabled=False, key="buyback_fixed_per_month", help="The fixed USD worth amount of tokens bought back by the business per month.")
                    buyback_perc_per_month = 0.0
                elif buyback_type == 'Percentage':
                    buyback_perc_per_month = st.number_input('Buyback per month / %', label_visibility="visible", min_value=0.0, value=[float(sys_param['buyback_perc_per_month'][0]) if enable_protocol_buybacks else 0.0][0], disabled=False, key="buyback_perc_per_month", help="The USD worth of tokens bought back by the business per month as percentage of the current business funds.")
                    buyback_fixed_per_month = 0.0
                
                buyback_buckets = ['Reserve', 'Community', 'Foundation', 'Incentivisation', 'Staking Vesting']
                if not incentivisation_toggle:
                    buyback_buckets.pop(buyback_buckets.index('Incentivisation'))
                if not staking_vesting_toggle:
                    buyback_buckets.pop(buyback_buckets.index('Staking Vesting'))
                buyback_bucket = st.radio('Buyback Bucket',tuple(buyback_buckets), index=0, help='The buyback bucket determines the destination of the bought back tokens.')
                buyback_start = st.date_input("Buybacks Start", min_value=token_launch_date, value=datetime.strptime(sys_param['buyback_start'][0], "%d.%m.%Y"), help="The date when monthly buybacks should start.")
                buyback_end = st.date_input("Buybacks End", min_value=buyback_start, value=datetime.strptime(sys_param['buyback_end'][0], "%d.%m.%Y") if datetime(buyback_start.year, buyback_start.month, buyback_start.day) <= datetime.strptime(sys_param['buyback_end'][0], "%d.%m.%Y") else datetime(buyback_start.year, buyback_start.month, buyback_start.day), help="The date when monthly buybacks should end.")

            else:
                buyback_perc_per_month = [float(sys_param['buyback_perc_per_month'][0]) if enable_protocol_buybacks else 0.0][0]
                buyback_fixed_per_month = [float(sys_param['buyback_fixed_per_month'][0])/1e3 if enable_protocol_buybacks else 0.0][0]
                buyback_bucket = [sys_param['buyback_bucket'][0] if enable_protocol_buybacks else 'Reserve'][0]
                buyback_start = [datetime.strptime(sys_param['buyback_start'][0], "%d.%m.%Y") if enable_protocol_buybacks else token_launch_date][0]
                buyback_end = [datetime.strptime(sys_param['buyback_end'][0], "%d.%m.%Y") if enable_protocol_buybacks else token_launch_date][0]
        with col92:
            enable_protocol_burning = st.toggle('Enable Protocol Token Burning', value=float(sys_param['burn_per_month'][0]) > 0, help=" Enable the burning of tokens from a protocol bucket.")
            if enable_protocol_burning:
                burn_per_month = st.number_input('Burn per month / %', label_visibility="visible", min_value=0.0, value=[float(sys_param['burn_per_month'][0]) if enable_protocol_burning else 0.0][0], disabled=False, key="burn_per_month", help="The total supply percentage of tokens being burned from the determined protocol bucket per month.")
                burn_start = st.date_input("Burning Start", min_value=token_launch_date, value=datetime.strptime(sys_param['burn_start'][0], "%d.%m.%Y"), help="The date when monthly burning should start.")
                burn_end = st.date_input("Burning End", min_value=burn_start, value=datetime.strptime(sys_param['burn_end'][0], "%d.%m.%Y") if datetime(burn_start.year, burn_start.month, burn_start.day) <= datetime.strptime(sys_param['burn_end'][0], "%d.%m.%Y") else datetime(burn_start.year, burn_start.month, burn_start.day), help="The date when monthly burning should end.")
                burn_buckets = ['Reserve', 'Community', 'Foundation']
                burn_bucket = st.radio('Burn Bucket',tuple(burn_buckets), index=0, help='The burn bucket determines the protocol bucket origin of the burned tokens.')
            else:
                burn_per_month = [float(sys_param['burn_per_month'][0]) if enable_protocol_burning else 0.0][0]
                burn_bucket = [sys_param['burn_bucket'][0] if enable_protocol_burning else 'Reserve'][0]
                burn_start = [datetime.strptime(sys_param['burn_start'][0], "%d.%m.%Y") if enable_protocol_burning else token_launch_date][0]
                burn_end = [datetime.strptime(sys_param['burn_end'][0], "%d.%m.%Y") if enable_protocol_burning else token_launch_date][0]

        buyback_start = datetime(buyback_start.year, buyback_start.month, buyback_start.day)
        buyback_end = datetime(buyback_end.year, buyback_end.month, buyback_end.day)
        burn_start = datetime(burn_start.year, burn_start.month, burn_start.day)
        burn_end = datetime(burn_end.year, burn_end.month, burn_end.day)

        if enable_protocol_buybacks:
            if buyback_start < token_launch_date:
                st.error(f"The buyback starting date ({buyback_start.strftime('%d.%m.%Y')}) is before the launch date ({token_launch_date}). Please adjust the buyback starting date!", icon="⚠️")
        if enable_protocol_burning:
            if burn_start < token_launch_date:
                st.error(f"The burn starting date ({burn_start.strftime('%d.%m.%Y')}) is before the launch date ({token_launch_date}). Please adjust the burn starting date!", icon="⚠️")
    
    buyback_type = buyback_type if enable_protocol_buybacks else 'Fixed'
    buyback_perc_per_month = buyback_perc_per_month if enable_protocol_buybacks else 0.0
    buyback_fixed_per_month = buyback_fixed_per_month if enable_protocol_buybacks else 0.0
    buyback_bucket = buyback_bucket if enable_protocol_buybacks else 'Reserve'
    buyback_start = buyback_start if enable_protocol_buybacks else token_launch_date
    buyback_end = buyback_end if enable_protocol_buybacks else token_launch_date
    burn_per_month = burn_per_month if enable_protocol_burning else 0.0
    burn_bucket = burn_bucket if enable_protocol_burning else 'Reserve'
    burn_start = burn_start if enable_protocol_burning else token_launch_date
    burn_end = burn_end if enable_protocol_burning else token_launch_date

    ba_return_dict = {
        "income" : income,
        "expenditures" : expenditures,
        "royalty_income_per_month" : royalty_income_per_month,
        "treasury_income_per_month" : treasury_income_per_month,
        "other_income_per_month" : other_income_per_month,
        "one_time_payments_1" : one_time_payments_1,
        "salaries_per_month" : salaries_per_month,
        "license_costs_per_month" : license_costs_per_month,
        "other_monthly_costs" : other_monthly_costs,
        "initial_cash_balance" : initial_cash_balance,
        "enable_protocol_buybacks" : enable_protocol_buybacks,
        "buyback_type" : buyback_type,
        "buyback_perc_per_month" : buyback_perc_per_month,
        "buyback_fixed_per_month" : buyback_fixed_per_month,
        "buyback_bucket" : buyback_bucket,
        "buyback_start" : buyback_start,
        "buyback_end" : buyback_end,
        "enable_protocol_burning" : enable_protocol_burning,
        "burn_per_month" : burn_per_month,
        "burn_bucket" : burn_bucket,
        "burn_start" : burn_start,
        "burn_end" : burn_end,
        "show_full_business_table" : show_full_business_table
    }

    return ba_return_dict
