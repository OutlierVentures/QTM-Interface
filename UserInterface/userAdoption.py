import streamlit as st
import numpy as np
from datetime import datetime, timedelta
import time

#NEW IMPORTS
from UserInterface.helpers import *
from Model.parts.utils import *


def userAdoptionInput(sys_param, tav_return_dict):
    with st.expander("**User Adoption**"):
        st.markdown("### User Adoption")
        # adoption style choice | user numbers | revenues
        adoption_style_choices = ['Weak', 'Medium', 'Strong', 'Custom']
        adoption_style = st.radio('Adoption Assumption',tuple(adoption_style_choices), index=adoption_style_choices.index(sys_param['adoption_style'][0]) if 'adoption_style' in sys_param else 0, help='The adoption style determines the scaling velocity for the product revenue and token demand. Moreover it influences the average agent sentiment in terms of selling and utility adoption behavior.')
        show_full_adoption_table = st.toggle('Show Full Table', value=False, help="Show the full adoption parameter set.")

        adoption_dict = {
            "Weak" : {
                "initial_product_users": 250,
                "initial_token_holders": 250,
                "avg_product_user_growth_rate" : 0.5,
                "avg_token_holder_growth_rate" : 0.5,
                "product_adoption_velocity" : 0.5,
                "token_adoption_velocity" : 0.5,
                "one_time_product_revenue_per_user" : 0.0,
                "regular_product_revenue_per_user" : 0.5,
                "one_time_token_buy_per_user" : 0.0,
                "regular_token_buy_per_user" : 0.5,
                "avg_token_utility_allocation" : 20.0,
                "avg_token_selling_allocation" : 70.0,
                "avg_token_holding_allocation" : 10.0,
                "avg_token_utility_removal" : 10.0,

            },
            "Medium" : {
                "initial_product_users": 350,
                "initial_token_holders": 350,
                "avg_product_user_growth_rate" : 3.5,
                "avg_token_holder_growth_rate" : 3.5,
                "product_adoption_velocity" : 1.5,
                "token_adoption_velocity" : 1.5,
                "one_time_product_revenue_per_user" : 0.0,
                "regular_product_revenue_per_user" : 2.0,
                "one_time_token_buy_per_user" : 0.0,
                "regular_token_buy_per_user" : 2.0,
                "avg_token_utility_allocation" : 60.0,
                "avg_token_selling_allocation" : 30.0,
                "avg_token_holding_allocation" : 10.0,
                "avg_token_utility_removal" : 6.0,

            },
            "Strong" : {
                "initial_product_users": 500,
                "initial_token_holders": 500, 
                "avg_product_user_growth_rate" : 8.0,
                "avg_token_holder_growth_rate" : 8.0,
                "product_adoption_velocity" : 2.5,
                "token_adoption_velocity" : 2.5,
                "one_time_product_revenue_per_user" : 0.0,
                "regular_product_revenue_per_user" : 6.0,
                "one_time_token_buy_per_user" : 0.0,
                "regular_token_buy_per_user" : 6.0,
                "avg_token_utility_allocation" : 75.0,
                "avg_token_selling_allocation" : 20.0,
                "avg_token_holding_allocation" : 5.0,
                "avg_token_utility_removal" : 3.0,
            }
        }

        if adoption_style == 'Custom' or show_full_adoption_table:
            
            col71, col72 = st.columns(2)
            col73, col74 = st.columns(2)

            with col73:
                incentive_ua = st.toggle('Incentive-based Product Adoption', value = False, help="This feature allows you to link your *Product Users Growth Rate* to the incentives you provide in your economy. You can think of the *Incentive USD per User Target* set below as your customer acquisition cost for new users. As long as the USD incentives per user are higher than this value, your user adoption increases, and vice versa.") 
                if incentive_ua:
                    st.warning("⚠️ This is an advanced feature. When activated, the *Product User Growth Rate* will depend on incentive target defined below and the above fixed growth rate no longer applies.")
                    # incentivisation_rev_share = float(sys_param['incentivisation_rev_share'][0]) if 'incentivisation_rev_share' in sys_param else 0.0
                    if tav_return_dict['incentivisation_allocation'] > 0.0 or tav_return_dict['airdrop_allocation'] > 0.0: # incentivisation_rev_share > 0.0 condition cannot be checked as defined in subsequent section, thus warning message instead of error message.
                        # add user adoption boost per incentivisation (in USD)
                        user_adoption_target = st.number_input('Incentive USD per User Target / $', label_visibility="visible", min_value=0.0, value=[float(sys_param['user_adoption_target'][0]) if 'user_adoption_target' in sys_param else 550.0][0], disabled=False, key="user_adoption_target", help="Target incentivisation to onboard one more product users. A value of 0 disables this feature!")
                    else:
                        st.warning("⚠️ Some incentivization is needed to use this feature. Please make sure you selected one of the following:\n1. Token allocation for incentivization\n2. Token allocation for airdrops\n3. Incentivization Revenue Share (see Rev. Share in Business Assumptions section below)")
                        user_adoption_target = st.number_input('Incentive USD per User Target / $', label_visibility="visible", min_value=0.0, value=[float(sys_param['user_adoption_target'][0]) if 'user_adoption_target' in sys_param else 550.0][0], disabled=False, key="user_adoption_target", help="Target incentivisation to onboard one more product users. A value of 0 disables this feature!")
                else:
                    user_adoption_target = [float(sys_param['user_adoption_target'][0]) if 'user_adoption_target' in sys_param else 550.0][0]

            with col71:
                st.write(f"**Product Adoption**")
                initial_product_users = st.number_input('Initial Product Users', label_visibility="visible", min_value=0, value=[int(sys_param['initial_product_users'][0]) if adoption_style == 'Custom' else adoption_dict[adoption_style]['initial_product_users']][0], disabled=False, key="initial_product_users", help="The initial product users generating revenue in diverse assets -> $.")
                avg_product_user_growth_rate = st.number_input('Avg. Product Users Growth Rate / %', label_visibility="visible", min_value=0.0, value=0.0 if incentive_ua else [((float(sys_param['product_users_after_10y'][0]) / float(sys_param['initial_product_users'][0]))**(1/120.0)-1)*100 if adoption_style == 'Custom' else adoption_dict[adoption_style]['avg_product_user_growth_rate']][0], disabled=incentive_ua, key="product_users_growth_rate", help="The average monthly growth rate of product users.")
                # Token velocity selector
                product_velocity_options = [0.5, 1.5, 2.5]
                # Determine the default selection based on sys_param
                default_velocity = [float(product_velocity_options[1]) if adoption_style == 'Custom' else adoption_dict[adoption_style]['product_adoption_velocity']][0]
                # Find the index of this value in the options list
                default_index = product_velocity_options.index(default_velocity)
                # Token velocity radio button
                product_adoption_velocity = st.radio(
                    'Product Adoption Velocity',
                    options=product_velocity_options,
                    index= default_index,
                    help="Select the velocity of product adoption. The higher the velocity, the faster the product adoption in the early years towards market saturation.",
                    horizontal=True
                )

                if not incentive_ua:
                    product_users_after_10y = initial_product_users * (1 + avg_product_user_growth_rate/100)**120
                    st.write(f"*Projected Product Users (10y): {int(np.ceil(product_users_after_10y)):+,}*")
                    regular_product_revenue_per_user = st.number_input('Regular Product Revenue / $', label_visibility="visible", min_value=0.0, value=[float(sys_param['regular_product_revenue_per_user'][0]) if adoption_style == 'Custom' else adoption_dict[adoption_style]['regular_product_revenue_per_user']][0], disabled=False, key="regular_product_revenue_per_user", help="The average regular monthly product revenue per user. This will accrue to the different revenue share buckets.")                
                    with st.spinner("Please wait while the adoption chart is loading..."):
                        user_adoption_series, revenue_series = calculate_user_adoption_series(initial_product_users, product_users_after_10y, product_adoption_velocity, regular_product_revenue_per_user) 
                        product_chart = plot_user_adoption_and_revenue(user_adoption_series, revenue_series)
                        st.plotly_chart(product_chart, use_container_width=True)
                else:
                    st.write("*Projected Product Users (10y): N/A*")
                    product_users_after_10y = 0
                    regular_product_revenue_per_user = st.number_input('Regular Product Revenue / $', label_visibility="visible", min_value=0.0, value=[float(sys_param['regular_product_revenue_per_user'][0]) if adoption_style == 'Custom' else adoption_dict[adoption_style]['regular_product_revenue_per_user']][0], disabled=False, key="regular_product_revenue_per_user", help="The average regular monthly product revenue per user. This will accrue to the different revenue share buckets.")                
                    # Display the above chart with only revenues and a message: "adoption growth is now based on incentives"

            with col74:
                switch = st.toggle('Market-based Token Adoption', value = False, help="This section allows you to link Token Adoption (i.e. how many people buy your token) to simulated market returns. In its current configuration, the number of users purchasing the token will increase or decrease based on these simulated returns. For example, if the market shows positive returns, token purchases will increase accordingly, and vice versa. You can select the token you want to use to represent the market in your simulation (i.e. market beta). The simulation utilizes Brownian Motion.") 
                if switch:
                    st.warning("⚠️ This is an advanced feature. When activated, the *Token Buys* will be adjusted based on simulated market returns.")
                    st.markdown("##### Market Simulation")
                    # Choose token to use as proxy for market sentiment
                    token_choice_predefined = ['bitcoin', 'ethereum']
                    token_choice = st.radio("###### Select Token", tuple(token_choice_predefined))
                    
                    # Checks
                    today = datetime.today().date()
                    default_start_date = today - timedelta(days=365)
                    
                    # Define the start and end date inputs 
                    sim_start_date = st.date_input(
                        "Start Date",
                        value=default_start_date,
                        max_value=today,  
                        help="Select the start date for the simulation. This start date should be at least 180 days before the end date to ensure sufficient data for inferring the parameters used to simulate market returns."
                    )

                    sim_end_date = st.date_input(
                        "End Date",
                        value=today,
                        min_value=sim_start_date,  
                        max_value=today,
                        help="Select the end date for the simulation. The end date must be at least 180 days after the start date to ensure sufficient data for inferring the parameters used to simulate market returns."
                    )

                    # Button to trigger the simulation
                    simulate_button = st.button("Simulate Returns & Market Adoption")

                    # Initialize variables with a default value
                    start_date_unix = int(time.mktime(sim_start_date.timetuple()))
                    end_date_unix = int(time.mktime(sim_end_date.timetuple()))
                    active = 1

                    if simulate_button:
                        # Check if the dates meet the conditions
                        if sim_start_date > sim_end_date - timedelta(days=180):
                            st.warning("To run the simulation, please adjust the dates to include at least 6 months of historical price data. The selected date range is currently too short.", icon="⚠️")

                        else:
                            # Display spinner and perform computations only if conditions are met
                            with st.spinner("Please wait while the simulation chart is loading..."):

                                # Fetch and simulate market returns
                                result = simulate_market_returns(token_choice, start_date_unix, end_date_unix)
                                simulation_df = result['market']

                                # Plotting and displaying the figure in Streamlit
                                fig = plot_simulation_results(simulation_df, token_choice) 
                                st.plotly_chart(fig, use_container_width=True)

                                # Plotting new token adoption and Buy Pressure
                                ### Insert Code ###

                else:
                    token_choice = 0
                    start_date_unix = 0
                    end_date_unix = 0
                    active = 0 

            with col72:
                st.write(f"**Token Adoption**")
                initial_token_holders = st.number_input('Initial Token Holders', label_visibility="visible", min_value=0, value=[int(sys_param['initial_token_holders'][0]) if adoption_style == 'Custom' else adoption_dict[adoption_style]['initial_token_holders']][0], disabled=False, key="initial_token_holders", help="Initial token holders that regularly buy tokens from the DEX liquidity pool.")
                avg_token_holder_growth_rate = st.number_input('Avg. Token Holder Growth Rate / %', label_visibility="visible", min_value=0.0, value=[((float(sys_param['token_holders_after_10y'][0]) / float(sys_param['initial_token_holders'][0]))**(1/120.0)-1)*100 if adoption_style == 'Custom' else adoption_dict[adoption_style]['avg_token_holder_growth_rate']][0], disabled=False, key="avg_token_holder_growth_rate", help="The average monthly growth rate of token holders.")
                # Token velocity selector
                token_velocity_options = [0.5, 1.5, 2.5]
                # Determine the default selection based on sys_param
                default_velocity = [float(token_velocity_options[1]) if adoption_style == 'Custom' else adoption_dict[adoption_style]['token_adoption_velocity']][0]
                # Find the index of this value in the options list
                default_index = token_velocity_options.index(default_velocity)
                # Token velocity radio button
                token_adoption_velocity = st.radio(
                    'Token Adoption Velocity',
                    options=token_velocity_options,
                    index=default_index,
                    help="Select the velocity of token adoption. The higher the velocity, the faster the token adoption in the early years towards market saturation.",
                    horizontal=True
                )
                
                token_holders_after_10y = initial_token_holders * (1 + avg_token_holder_growth_rate/100)**120
                st.write(f"*Projected Token Holders (10y): {int(np.ceil(token_holders_after_10y)):+,}*")
                regular_token_buy_per_user = st.number_input('Regular Token Buy / $', label_visibility="visible", min_value=0.0, value=[float(sys_param['regular_token_buy_per_user'][0]) if adoption_style == 'Custom' else adoption_dict[adoption_style]['regular_token_buy_per_user']][0], disabled=False, key="regular_token_buy_per_user", help="The average regular monthly token buy per token holder. This will accrue directly to the token via buys from the DEX liquidity pool.")
                with st.spinner("Please wait while the token adoption chart is loading..."):
                    token_adoption_series, buy_pressure_series = calculate_token_adoption_series(initial_token_holders, token_holders_after_10y, token_adoption_velocity, regular_token_buy_per_user)
                    token_chart = plot_token_adoption_and_buy_pressure(token_adoption_series, buy_pressure_series)
                    st.plotly_chart(token_chart, use_container_width=True)
        
        else:
            initial_product_users = adoption_dict[adoption_style]['initial_product_users']
            initial_token_holders = adoption_dict[adoption_style]['initial_token_holders']
            avg_product_user_growth_rate = adoption_dict[adoption_style]['avg_product_user_growth_rate']
            product_users_after_10y = initial_product_users * (1 + avg_product_user_growth_rate/100)**120
            avg_token_holder_growth_rate = adoption_dict[adoption_style]['avg_token_holder_growth_rate']
            token_holders_after_10y = initial_token_holders * (1 + avg_token_holder_growth_rate/100)**120
            product_adoption_velocity = adoption_dict[adoption_style]['product_adoption_velocity']
            token_adoption_velocity = adoption_dict[adoption_style]['token_adoption_velocity']
            regular_product_revenue_per_user = adoption_dict[adoption_style]['regular_product_revenue_per_user']
            regular_token_buy_per_user = adoption_dict[adoption_style]['regular_token_buy_per_user']
            user_adoption_target = 0.0
            token_choice = 0
            start_date_unix = 0
            end_date_unix = 0
            active = 0 
            incentive_ua = False


    ua_return_dict = {
        "adoption_style" : adoption_style,
        "show_full_adoption_table" : show_full_adoption_table,
        "initial_product_users" : initial_product_users,
        "initial_token_holders" : initial_token_holders,
        "avg_product_user_growth_rate" : avg_product_user_growth_rate,
        "product_users_after_10y" : product_users_after_10y,
        "product_adoption_velocity" : product_adoption_velocity,
        "regular_product_revenue_per_user" : regular_product_revenue_per_user,
        "avg_token_holder_growth_rate" : avg_token_holder_growth_rate,
        "token_holders_after_10y" : token_holders_after_10y,
        "token_adoption_velocity" : token_adoption_velocity,
        "regular_token_buy_per_user" : regular_token_buy_per_user,
        "adoption_dict" : adoption_dict,
        "user_adoption_target": user_adoption_target,
        "token": token_choice,
        "sim_start": start_date_unix,
        "sim_end": end_date_unix,
        "market": active,
        "incentive_ua": incentive_ua
    }

    return ua_return_dict
