import streamlit as st
import numpy as np
from Model.parts.utils import months_difference, calculate_raised_capital
from datetime import datetime

def businessAssumptionsInput(sys_param, ua_return_dict, tav_return_dict, token_launch_date, incentivisation_toggle, staking_vesting_toggle):
    """
    This function creates the business assumptions section of the UI.
    """
    with st.expander("**Business Assumptions**"):
        st.markdown("### Business Assumptions")
        # income | expenditures | buybacks | burns
        
        # st.write("**Financial Streams**")
        # col81, col82, col83 = st.columns(3)
        # with col81:
        #     show_full_business_table = st.toggle('Use Full Custom Table', value=False, help="Show the full financial stream parameter set. Note that all income streams from the table will be added on top of the adoption product revenue.")
        #     if not show_full_business_table:
        #         income = st.number_input('Additional income per month / $k', label_visibility="visible", min_value=0.0, value=float(sys_param['royalty_income_per_month'][0] + sys_param['other_income_per_month'][0] + sys_param['treasury_income_per_month'][0])/1e3, disabled=False, key="income", help="The monthly income for the business on top of the product revenue, defined in the user adoption section.")
        #         expenditures = st.number_input('Expenditures per month / $k', label_visibility="visible", min_value=0.0, value=float(sys_param['salaries_per_month'][0] + sys_param['license_costs_per_month'][0] + sys_param['other_monthly_costs'][0] + (sys_param['one_time_payments_1'][0]+ sys_param['one_time_payments_2'][0])/120)/1e3, disabled=False, key="expenditures", help="The monthly expenditures for the business.")
        #     else:
        #         income = 0.0
        #         expenditures = 0.0
        # if show_full_business_table:
        #     with col82:
        #         st.write("**Income**")
        #         royalty_income_per_month = st.number_input('Royalty income per month / $k', label_visibility="visible", min_value=0.0, value=[float(sys_param['royalty_income_per_month'][0])/1e3 if show_full_business_table else 0.0][0], disabled=False, key="royalty_income_per_month", help="The monthly royalty income for the business.")
        #         treasury_income_per_month = st.number_input('Treasury income per month / $k', label_visibility="visible", min_value=0.0, value=[float(sys_param['treasury_income_per_month'][0])/1e3 if show_full_business_table else 0.0][0], disabled=False, key="treasury_income_per_month", help="The monthly income for the business from treasury investments yields.")
        #         other_income_per_month = st.number_input('Other income per month / $k', label_visibility="visible", min_value=0.0, value=[float(sys_param['other_income_per_month'][0])/1e3 if show_full_business_table else 0.0][0], disabled=False, key="other_income_per_month", help="The monthly income for the business from other sources.")
        #     with col83:
        #         st.write("**Expenditures**")
        #         one_time_payments_1 = st.number_input('One-time payments / $k', label_visibility="visible", min_value=0.0, value=[float(sys_param['one_time_payments_1'][0] + sys_param['one_time_payments_2'][0])/1e3 if show_full_business_table else 0.0][0], disabled=False, key="one_time_payments_1", help="The one-time payments for the business at launch (e.g. any back payment of liabilities or treasury investments).")
        #         salaries_per_month = st.number_input('Salaries per month / $k', label_visibility="visible", min_value=0.0, value=[float(sys_param['salaries_per_month'][0])/1e3 if show_full_business_table else 0.0][0], disabled=False, key="salaries_per_month", help="The monthly salaries paid by the business.")
        #         license_costs_per_month = st.number_input('License costs per month / $k', label_visibility="visible", min_value=0.0, value=[float(sys_param['license_costs_per_month'][0])/1e3 if show_full_business_table else 0.0][0], disabled=False, key="license_costs_per_month", help="The monthly license costs paid by the business.")
        #         other_monthly_costs = st.number_input('Other monthly costs / $k', label_visibility="visible", min_value=0.0, value=[float(sys_param['other_monthly_costs'][0])/1e3 if show_full_business_table else 0.0][0], disabled=False, key="other_monthly_costs", help="The monthly costs paid by the business for other purposes.")
        # else:
        #     royalty_income_per_month = [float(sys_param['royalty_income_per_month'][0])/1e3 if income == 0.0 else 0.0][0]
        #     treasury_income_per_month = [float(sys_param['treasury_income_per_month'][0])/1e3 if income == 0.0 else 0.0][0]
        #     other_income_per_month = [float(sys_param['other_income_per_month'][0])/1e3 if income == 0.0 else income][0]
        #     one_time_payments_1 = [float(sys_param['one_time_payments_1'][0] + sys_param['one_time_payments_2'][0])/1e3 if expenditures == 0.0 else 0.0][0]
        #     salaries_per_month = [float(sys_param['salaries_per_month'][0])/1e3 if expenditures == 0.0 else 0.0][0]
        #     license_costs_per_month = [float(sys_param['license_costs_per_month'][0])/1e3 if expenditures == 0.0 else 0.0][0]
        #     other_monthly_costs = [float(sys_param['other_monthly_costs'][0])/1e3 if expenditures == 0.0 else expenditures][0]
        
        # if not token_launch:
        #     months_since_launch = np.abs(int(months_difference(token_launch_date, datetime.today())))
        #     projected_cash_balance = raised_funds*1e3 - one_time_payments_1 + (royalty_income_per_month + treasury_income_per_month + other_income_per_month - salaries_per_month - license_costs_per_month - other_monthly_costs) * months_since_launch
        #     initial_cash_balance = st.number_input('Financial Reserves / $k', label_visibility="visible", min_value=0.0, value=float(sys_param['initial_cash_balance'][0])/1e3 if 'initial_cash_balance' in sys_param else projected_cash_balance if projected_cash_balance > 0 else 0.0, format="%.5f", disabled=False, key="initial_cash_balance", help="The financial reserves of the business today. The financial reserves determine the runway of the business.")
        #     if initial_cash_balance == 0 and (royalty_income_per_month + treasury_income_per_month + other_income_per_month + initial_product_users * (regular_product_revenue_per_user if adoption_style == 'Custom' or show_full_adoption_table else adoption_dict[adoption_style]['regular_product_revenue_per_user']) - salaries_per_month - license_costs_per_month - other_monthly_costs) < 0:
        #         st.error(f"The financial reserves are 0 and the monthly expenditures are greater than the revenues. Increase the initial cash reserves to achieve a proper financial runway!", icon="⚠️")
        # else:
        #     initial_cash_balance = 0.0

        col81, col82 = st.columns(2)
        with col81:
            st.write("**Income**")
            income = st.number_input('Additional fixed income per month / $k', label_visibility="visible", min_value=0.0, value=float(sys_param['royalty_income_per_month'][0] + sys_param['other_income_per_month'][0] + sys_param['treasury_income_per_month'][0])/1e3, disabled=False, key="income", help="The monthly income for the business on top of the product revenue, defined in the user adoption section.")

        with col82:
            st.write("**Expenditures**")
            expenditures = st.number_input('Fixed expenditures per month / $k', label_visibility="visible", min_value=0.0, value=float(sys_param['salaries_per_month'][0] + sys_param['license_costs_per_month'][0] + sys_param['other_monthly_costs'][0] + (sys_param['one_time_payments_1'][0]+ sys_param['one_time_payments_2'][0])/120)/1e3, disabled=False, key="expenditures", help="The monthly expenditures for the business.")

        st.write("#### Revenue Share")
        # revenue share settings
        st.write("**Distribution**")
        col82a, col82b, col82c, col82d = st.columns(4)
        with col82a:
            business_rev_share = st.number_input('Business Revenue Share / %', label_visibility="visible", min_value=0.0, max_value=100.0, value=[float(sys_param['business_rev_share'][0]) if 'business_rev_share' in sys_param else 75.0][0], disabled=False, key="business_rev_share", help="The share of revenue that will accrue to the business funds.")
        with col82b:
            staker_rev_share = st.number_input('Staker Revenue Share / %', label_visibility="visible", min_value=0.0, max_value=100.0, value=[float(sys_param['staker_rev_share'][0]) if 'staker_rev_share' in sys_param else 25.0][0],  disabled=False, key="staker_rev_share", help="The share of revenue that will accrue to token stakers. This requires staking to be one of the token utilities.")
            if staker_rev_share > 0.0:
                staker_rev_share_buyback = st.checkbox('Buyback Tokens', value=[float(sys_param['staker_rev_share_buyback'][0]) if 'staker_rev_share_buyback' in sys_param else False][0], key="staker_rev_share_buyback", help="Check this box if the staker revenue share should be used to buy back tokens from the market (DEX liquidity pool) and distribute them instead of the revenue in diverse assets. Diverse assets are any assets that will be collected as revenue and depend on the product. They can be any assets apart from the token itself.")
            else:
                staker_rev_share_buyback = False
        with col82c:
            service_provider_rev_share = st.number_input('Service Provider Revenue Share / %', label_visibility="visible", min_value=0.0, max_value=100.0, value=[float(sys_param['service_provider_rev_share'][0]) if 'service_provider_rev_share' in sys_param else 0.0][0], disabled=False, key="service_provider_rev_share", help="The share of revenue that will accrue to service providers.")
        with col82d:
            incentivisation_rev_share = st.number_input('Incentivisation Revenue Share / %', label_visibility="visible", min_value=0.0, max_value=100.0, value=[float(sys_param['incentivisation_rev_share'][0]) if 'incentivisation_rev_share' in sys_param else 0.0][0], disabled=False, key="incentivisation_rev_share", help="The share of revenue that will be used to incentivise the ecosystem.")
            if incentivisation_rev_share > 0.0:
                incentivisation_rev_share_buyback = st.checkbox('Buyback Tokens', value=[float(sys_param['incentivisation_rev_share_buyback'][0]) if 'incentivisation_rev_share_buyback' in sys_param else False][0], key="incentivisation_rev_share_buyback", help="Check this box if the incentivisation revenue share should be used to buy back tokens from the market (DEX liquidity pool) and distribute them instead of the revenue in diverse assets. Diverse assets are any assets that will be collected as revenue and depend on the product. They can be any assets apart from the token itself.")
            else:
                incentivisation_rev_share_buyback = False
            if ua_return_dict["incentive_ua"] and ua_return_dict["user_adoption_target"] > 0.0 and incentivisation_rev_share == 0.0 and tav_return_dict['incentivisation_allocation'] == 0.0 and tav_return_dict['airdrop_allocation'] == 0.0:
               st.error(f"You're currently using an *Incentive-based User Adoption* but you didn't allocate any tokens for incentivization purposes. Please increase the *Incentivization Rev. Share %* or assign some tokens for *Incentivization Vesting* or *Airdrops* in the Token Allocation & Vesting section.", icon="⚠️")

        rev_share_sum = business_rev_share + staker_rev_share + service_provider_rev_share + incentivisation_rev_share
        if rev_share_sum != 100.0:
            st.error(f"The revenue shares must sum up to 100%. Currently they sum up to {rev_share_sum}%.", icon="⚠️")


        st.write("#### Buybacks and Burns")
        col91, col92 = st.columns(2)
        with col91:
            st.write("**Buybacks**")
            enable_protocol_buybacks = st.toggle('Enable Protocol Token Buybacks', value=float(sys_param['buyback_perc_per_month'][0]) != 0 or float(sys_param['buyback_fixed_per_month'][0]) != 0, help="Enable the buyback of tokens to refill a protocol bucket.")
            if enable_protocol_buybacks:
                buyback_type = st.radio('Buyback Type',('Fixed', 'Percentage'), index=0, help='The buyback type determines the buyback behavior of the business. A fixed buyback means that the business buys back a fixed USD worth amount of tokens per month. A percentage buyback means that the business buys back a percentage USD worth amount of tokens per month, depending on the business funds.')
                if buyback_type == 'Fixed':
                    buyback_fixed_per_month = st.number_input('Buyback per month / $k', label_visibility="visible", value=[float(sys_param['buyback_fixed_per_month'][0])/1e3 if enable_protocol_buybacks else 0.0][0], disabled=False, key="buyback_fixed_per_month", help="The fixed USD worth amount of tokens bought back by the business per month.")
                    buyback_perc_per_month = 0.0
                elif buyback_type == 'Percentage':
                    buyback_perc_per_month = st.number_input('Buyback per month / %', label_visibility="visible", value=[float(sys_param['buyback_perc_per_month'][0]) if enable_protocol_buybacks else 0.0][0], disabled=False, key="buyback_perc_per_month", help="The USD worth of tokens bought back by the business per month as percentage of the current business funds.")
                    buyback_fixed_per_month = 0.0
                
                buyback_buckets = ['Reserve', 'Community', 'Foundation', 'Incentivisation', 'Staking Vesting']
                if not incentivisation_toggle:
                    buyback_buckets.pop(buyback_buckets.index('Incentivisation'))
                if not staking_vesting_toggle:
                    buyback_buckets.pop(buyback_buckets.index('Staking Vesting'))
                buyback_bucket = st.radio('Buyback Bucket',tuple(buyback_buckets), index=buyback_buckets.index(sys_param['buyback_bucket'][0]), help='The buyback bucket determines the destination of the bought back tokens.')
                buyback_start = st.date_input("Buybacks Start", min_value=token_launch_date, value=datetime.strptime(sys_param['buyback_start'][0], "%d.%m.%Y"), help="The date when monthly buybacks should start.")
                buyback_end = st.date_input("Buybacks End", min_value=buyback_start, value=datetime.strptime(sys_param['buyback_end'][0], "%d.%m.%Y") if datetime(buyback_start.year, buyback_start.month, buyback_start.day) <= datetime.strptime(sys_param['buyback_end'][0], "%d.%m.%Y") else datetime(buyback_start.year, buyback_start.month, buyback_start.day), help="The date when monthly buybacks should end.")

            else:
                buyback_perc_per_month = [float(sys_param['buyback_perc_per_month'][0]) if enable_protocol_buybacks else 0.0][0]
                buyback_fixed_per_month = [float(sys_param['buyback_fixed_per_month'][0])/1e3 if enable_protocol_buybacks else 0.0][0]
                buyback_bucket = [sys_param['buyback_bucket'][0] if enable_protocol_buybacks else 'Reserve'][0]
                buyback_start = [datetime.strptime(sys_param['buyback_start'][0], "%d.%m.%Y") if enable_protocol_buybacks else token_launch_date][0]
                buyback_end = [datetime.strptime(sys_param['buyback_end'][0], "%d.%m.%Y") if enable_protocol_buybacks else token_launch_date][0]
        with col92:
            st.write("**Burning**")
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
        "income": income,
        "expenditures": expenditures,
        "business_rev_share": business_rev_share,
        "staker_rev_share": staker_rev_share,
        "service_provider_rev_share": service_provider_rev_share,
        "incentivisation_rev_share": incentivisation_rev_share,
        "rev_share_sum": rev_share_sum,
        "staker_rev_share_buyback": staker_rev_share_buyback,
        "incentivisation_rev_share_buyback": incentivisation_rev_share_buyback,
        "enable_protocol_buybacks": enable_protocol_buybacks,
        "buyback_type": buyback_type,
        "buyback_perc_per_month": buyback_perc_per_month,
        "buyback_fixed_per_month": buyback_fixed_per_month,
        "buyback_bucket": buyback_bucket,
        "buyback_start": buyback_start,
        "buyback_end": buyback_end,
        "enable_protocol_burning": enable_protocol_burning,
        "burn_per_month": burn_per_month,
        "burn_bucket": burn_bucket,
        "burn_start": burn_start,
        "burn_end": burn_end,
    }

    return ba_return_dict
