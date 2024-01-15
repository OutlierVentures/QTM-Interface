import streamlit as st
import numpy as np

def userAdoptionInput(sys_param):
    with st.expander("**User Adoption**"):
        st.markdown("### User Adoption")
        # adoption style choice | user numbers | revenues
        col61, col62, col63 = st.columns(3)
        with col61:
            adoption_style_choices = ['Weak', 'Medium', 'Strong', 'Custom']
            adoption_style = st.radio('Adoption Assumption',tuple(adoption_style_choices), index=adoption_style_choices.index(sys_param['adoption_style'][0]) if 'adoption_style' in sys_param else 0, help='The adoption style determines the scaling velocity for the product revenue and token demand. Moreover it influences the average agent sentiment in terms of selling and utility adoption behavior.')
            show_full_adoption_table = st.toggle('Show Full Table', value=False, help="Show the full adoption parameter set.")
        with col62:
            product_token_ratio = st.slider('Product / Token Weight', min_value=-1.0, max_value=1.0, step=0.1, value=(-float(sys_param['initial_product_users'][0]) + float(sys_param['initial_token_holders'][0])), format="%.2f", help="The weight of product users to token holders. -1 means there are no token holders, but only product users. 1 means the opposite and 0 means that there are as many product users as token holders.")
            initial_users = st.number_input('Initial Users', label_visibility="visible", min_value=0, value=int(sys_param['initial_product_users'][0]) + int(sys_param['initial_token_holders'][0]), disabled=False, key="initial_users", help="Initial amount of users to be divided between product users and token holders according to the Product / Token Weight.")
            initial_product_users = initial_users * (1 - (product_token_ratio)) / 2
            initial_token_holders = initial_users - initial_product_users

        with col63:
            st.write(f"Initial Token Holders: {int(np.ceil(initial_token_holders)):+,}")
            st.write(f"Initial Product Users: {int(np.ceil(initial_product_users)):+,}")

        adoption_dict = {
            "Weak" : {
                "avg_product_user_growth_rate" : 2.0,
                "avg_token_holder_growth_rate" : 2.0,
                "product_adoption_velocity" : 0.5,
                "token_adoption_velocity" : 0.5,
                "one_time_product_revenue_per_user" : 0.0,
                "regular_product_revenue_per_user" : 8.0,
                "one_time_token_buy_per_user" : 0.0,
                "regular_token_buy_per_user" : 8.0,
                "avg_token_utility_allocation" : 20.0,
                "avg_token_selling_allocation" : 70.0,
                "avg_token_holding_allocation" : 10.0,
                "avg_token_utility_removal" : 10.0,

            },
            "Medium" : {
                "avg_product_user_growth_rate" : 4.0,
                "avg_token_holder_growth_rate" : 4.0,
                "product_adoption_velocity" : 1.5,
                "token_adoption_velocity" : 1.5,
                "one_time_product_revenue_per_user" : 0.0,
                "regular_product_revenue_per_user" : 10.0,
                "one_time_token_buy_per_user" : 0.0,
                "regular_token_buy_per_user" : 18.0,
                "avg_token_utility_allocation" : 60.0,
                "avg_token_selling_allocation" : 30.0,
                "avg_token_holding_allocation" : 10.0,
                "avg_token_utility_removal" : 6.0,

            },
            "Strong" : {
                "avg_product_user_growth_rate" : 5.0,
                "avg_token_holder_growth_rate" : 5.0,
                "product_adoption_velocity" : 2.5,
                "token_adoption_velocity" : 2.5,
                "one_time_product_revenue_per_user" : 0.0,
                "regular_product_revenue_per_user" : 12.5,
                "one_time_token_buy_per_user" : 0.0,
                "regular_token_buy_per_user" : 25.0,
                "avg_token_utility_allocation" : 75.0,
                "avg_token_selling_allocation" : 20.0,
                "avg_token_holding_allocation" : 5.0,
                "avg_token_utility_removal" : 3.0,
            }
        }

        if adoption_style == 'Custom' or show_full_adoption_table:
            col71, col72 = st.columns(2)
            with col71:
                avg_product_user_growth_rate = st.number_input('Avg. Product Users Growth Rate / %', label_visibility="visible", min_value=0.0, value=[((float(sys_param['product_users_after_10y'][0]) / float(sys_param['initial_product_users'][0]))**(1/120.0)-1)*100 if adoption_style == 'Custom' else adoption_dict[adoption_style]['avg_product_user_growth_rate']][0], disabled=False, key="product_users_growth_rate", help="The average monthly growth rate of product users.")
                product_users_after_10y = initial_product_users * (1 + avg_product_user_growth_rate/100)**120
                st.write(f"Projected Product Users (10y): {int(np.ceil(product_users_after_10y)):+,}")
                product_adoption_velocity = st.number_input('Product Adoption Velocity', label_visibility="visible", min_value=0.1, value=[float(sys_param['product_adoption_velocity'][0]) if adoption_style == 'Custom' else adoption_dict[adoption_style]['product_adoption_velocity']][0], disabled=False, key="product_adoption_velocity", help="The velocity of product adoption. The higher the velocity, the faster the product adoption in the early years towards market saturation.")
                regular_product_revenue_per_user = st.number_input('Regular Product Revenue / $', label_visibility="visible", min_value=0.0, value=[float(sys_param['regular_product_revenue_per_user'][0]) if adoption_style == 'Custom' else adoption_dict[adoption_style]['regular_product_revenue_per_user']][0], disabled=False, key="regular_product_revenue_per_user", help="The average regular monthly product revenue per user. This will accrue directly to the business funds.")
            with col72:
                avg_token_holder_growth_rate = st.number_input('Avg. Token Holder Growth Rate / %', label_visibility="visible", min_value=0.0, value=[((float(sys_param['token_holders_after_10y'][0]) / float(sys_param['initial_token_holders'][0]))**(1/120.0)-1)*100 if adoption_style == 'Custom' else adoption_dict[adoption_style]['avg_token_holder_growth_rate']][0], disabled=False, key="avg_token_holder_growth_rate", help="The average monthly growth rate of token holders.")
                token_holders_after_10y = initial_token_holders * (1 + avg_token_holder_growth_rate/100)**120
                st.write(f"Projected Token Holders (10y): {int(np.ceil(token_holders_after_10y)):+,}")
                token_adoption_velocity = st.number_input('Token Adoption Velocity', label_visibility="visible", min_value=0.1, value=[float(sys_param['token_adoption_velocity'][0]) if adoption_style == 'Custom' else adoption_dict[adoption_style]['token_adoption_velocity']][0], disabled=False, key="token_adoption_velocity", help="The velocity of token adoption. The higher the velocity, the faster the token adoption in the early years towards market saturation.")
                regular_token_buy_per_user = st.number_input('Regular Token Buy / $', label_visibility="visible", min_value=0.0, value=[float(sys_param['regular_token_buy_per_user'][0]) if adoption_style == 'Custom' else adoption_dict[adoption_style]['regular_token_buy_per_user']][0], disabled=False, key="regular_token_buy_per_user", help="The average regular monthly token buy per token holder. This will accrue directly to the token via buys from the DEX liquidity pool.")
        else:
            avg_product_user_growth_rate = adoption_dict[adoption_style]['avg_product_user_growth_rate']
            product_users_after_10y = initial_product_users * (1 + avg_product_user_growth_rate/100)**120
            avg_token_holder_growth_rate = adoption_dict[adoption_style]['avg_token_holder_growth_rate']
            token_holders_after_10y = initial_token_holders * (1 + avg_token_holder_growth_rate/100)**120
    
    product_adoption_velocity = [product_adoption_velocity if adoption_style == 'Custom' or show_full_adoption_table else adoption_dict[adoption_style]['product_adoption_velocity']][0]
    token_adoption_velocity = [token_adoption_velocity if adoption_style == 'Custom' or show_full_adoption_table else adoption_dict[adoption_style]['token_adoption_velocity']][0]
    regular_product_revenue_per_user = [regular_product_revenue_per_user if adoption_style == 'Custom' or show_full_adoption_table else adoption_dict[adoption_style]['regular_product_revenue_per_user']][0]
    regular_token_buy_per_user = [regular_token_buy_per_user if adoption_style == 'Custom' or show_full_adoption_table else adoption_dict[adoption_style]['regular_token_buy_per_user']][0]

    ua_return_dict = {
        "adoption_style" : adoption_style,
        "show_full_adoption_table" : show_full_adoption_table,
        "product_token_ratio" : product_token_ratio,
        "initial_users" : initial_users,
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
        "adoption_dict" : adoption_dict
    }

    return ua_return_dict
