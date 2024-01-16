import streamlit as st
import numpy as np
from . import plots as plts

def fundraisingInput(sys_param, equity_investments, equity_perc, public_sale_supply, launch_valuation, initial_supply, uploaded_file):
    fundraising_style_map = {
        'Moderate': 2,
        'Medium': 5,
        'Aggressive': 8
    }
    with st.expander("**Fundraising**"):
        st.markdown("### Fundraising")
        col21, col22, col23, col24 = st.columns(4)
        with col21:
            fundraising_style_choices = ['Moderate', 'Medium', 'Aggressive','Custom']
            fundraising_style = st.radio('Fundraising Style',tuple(fundraising_style_choices), index=fundraising_style_choices.index(sys_param['fundraising_style'][0]) if 'fundraising_style' in sys_param else 0, help=f"The more aggressive the fundraising style, the more advantageous it is to be an early investor: **Moderate** / **Medium** / **Aggressive** : **{fundraising_style_map['Moderate']}x** / **{fundraising_style_map['Medium']}x** / **{fundraising_style_map['Aggressive']}x** public sale to seed round valuation ratio.")
            if fundraising_style != 'Custom':
                show_full_fund_table = st.toggle('Show Full Table', value=False, help="Show the full token fundraising table.")
            else:
                show_full_fund_table = False
            if fundraising_style != 'Custom':
                target_raise = st.number_input('Overall Capital Raise Target / $m', min_value=0.1, value=float(sys_param['raised_capital_sum'][0])/1e6, help="The overall capital raise target. This is the amount of money raised that will partially be used to seed the DEX liquidity and as a buffer for the financial runway.")
                left_over_raise = target_raise - equity_investments - launch_valuation * (public_sale_supply/100)
        with col23:
            if fundraising_style != 'Custom' and not show_full_fund_table:
                seed_valuation = np.linspace(launch_valuation/fundraising_style_map[fundraising_style], launch_valuation, 4)[0]
                presale_1_valuation = np.linspace(launch_valuation/fundraising_style_map[fundraising_style], launch_valuation, 4)[1]
                presale_2_valuation = np.linspace(launch_valuation/fundraising_style_map[fundraising_style], launch_valuation, 4)[2]
            else:
                seed_valuation = st.number_input('Seed Valuation / $m', min_value=0.01, value=float([np.linspace(launch_valuation/fundraising_style_map[fundraising_style], launch_valuation, 4)[0] if uploaded_file is None and fundraising_style != 'Custom' else float(sys_param['seed_valuation'][0]/1e6)][0]), help="The valuation of the seed round.")
                presale_1_valuation = st.number_input('Presale 1 Valuation / $m', min_value=0.01, value=float([np.linspace(launch_valuation/fundraising_style_map[fundraising_style], launch_valuation, 4)[1] if uploaded_file is None and fundraising_style != 'Custom' else float(sys_param['presale_1_valuation'][0]/1e6)][0]), help="The valuation of the first presale.")
                presale_2_valuation = st.number_input('Presale 2 Valuation / $m', min_value=0.01, value=float([np.linspace(launch_valuation/fundraising_style_map[fundraising_style], launch_valuation, 4)[2] if uploaded_file is None and fundraising_style != 'Custom' else float(sys_param['presale_2_valuation'][0]/1e6)][0]), help="The valuation of the second presale.")
                st.number_input("Public Sale Valuation / $m", disabled=True, value=launch_valuation, help="The valuation of the public sale defined in the Basic Token Information section.")

        with col22:
            valuation_weights = {
                "seed" : seed_valuation / launch_valuation,
                "presale_1" : presale_1_valuation / launch_valuation,
                "presale_2" : presale_2_valuation / launch_valuation
            }
            valuation_weights_sum = sum(valuation_weights.values())
            if fundraising_style != 'Custom' and not show_full_fund_table:
                seed_raised = float(valuation_weights["seed"]/valuation_weights_sum * left_over_raise)
                presale_1_raised = float(valuation_weights["presale_1"]/valuation_weights_sum * left_over_raise)
                presale_2_raised = float(valuation_weights["presale_2"]/valuation_weights_sum * left_over_raise)
                public_sale_raised = launch_valuation * (public_sale_supply/100)
                raised_funds = equity_investments + seed_raised + presale_1_raised + presale_2_raised + public_sale_raised
            else:
                seed_raised = st.number_input('Seed Raises / $m', min_value=0.0, value=float([valuation_weights["seed"]/valuation_weights_sum * left_over_raise if uploaded_file is None and fundraising_style != 'Custom' else float(sys_param['seed_raised'][0]/1e6)][0]), help="The amount of money raised in the seed round.")
                presale_1_raised = st.number_input('Presale 1 Raises / $m', min_value=0.0, value=float([valuation_weights["presale_1"]/valuation_weights_sum * left_over_raise if uploaded_file is None and fundraising_style != 'Custom' else float(sys_param['presale_1_raised'][0]/1e6)][0]), help="The amount of money raised in the first presale.")
                presale_2_raised = st.number_input('Presale 2 Raises / $m', min_value=0.0, value=float([valuation_weights["presale_2"]/valuation_weights_sum * left_over_raise if uploaded_file is None and fundraising_style != 'Custom' else float(sys_param['presale_2_raised'][0]/1e6)][0]), help="The amount of money raised in the second presale.")
                public_sale_raised = st.number_input('Public Sale Raises / $m', min_value=0.0, value=float([launch_valuation * (public_sale_supply/100) if uploaded_file is None and fundraising_style != 'Custom' else float(sys_param['public_sale_raised'][0]/1e6)][0]), disabled=True, help="The amount of money raised in the public sale.")

                raised_funds = equity_investments + seed_raised + presale_1_raised + presale_2_raised + public_sale_raised
                if fundraising_style == 'Custom' or show_full_fund_table:
                    st.write(f"Total Raised: {raised_funds:.3f} $m")
        
        with col24:
            if fundraising_style == 'Custom' or show_full_fund_table:
                seed_allocation = ((seed_raised) / ((seed_valuation)/initial_supply) / initial_supply) * 1e2
                presale_1_allocation = ((presale_1_raised) / ((presale_1_valuation)/initial_supply) / initial_supply) * 1e2
                presale_2_allocation = ((presale_2_raised) / ((presale_2_valuation)/initial_supply) / initial_supply) * 1e2
                public_sale_allocation = ((public_sale_raised) / ((launch_valuation)/initial_supply) / initial_supply) * 1e2
                st.number_input('Seed Alloc / %', disabled=True, value=seed_allocation, help="The seed round token allocation as percentage of the initial total supply.")
                st.number_input('Presale 1 Alloc / %', disabled=True, value=presale_1_allocation, help="The first presale token allocation as percentage of the initial total supply.")
                st.number_input('Presale 2 Alloc / %', disabled=True, value=presale_2_allocation, help="The second presale token allocation as percentage of the initial total supply.")
                st.number_input('Public Sale Alloc / %', disabled=True, value=public_sale_allocation, help="The public sale token allocation as percentage of the initial total supply.")
        
        if fundraising_style == 'Custom' or show_full_fund_table:
            col21a, col22a, col23a = st.columns(3)
            with col21a:
                plts.bar_plot_plotly_from_variables({'Round': ['Angels', 'Seed', 'Presale 1', 'Presale 2', 'Public Sale'], 'Raised / $': [equity_investments, seed_raised, presale_1_raised, presale_2_raised, public_sale_raised]}, 'Round', 'Raised / $', info_box=None, plot_title='Fundraising Round Raised Capital')
            with col22a:
                plts.bar_plot_plotly_from_variables({'Round': ['Angels', 'Seed', 'Presale 1', 'Presale 2', 'Public Sale'], 'Valuation / $m': [equity_investments / (initial_supply * equity_perc/100), seed_valuation, presale_1_valuation, presale_2_valuation, launch_valuation]}, 'Round', 'Valuation / $m', info_box=None, plot_title='Fundraising Round Token Valuations')
            with col23a:
                plts.bar_plot_plotly_from_variables({'Round': ['Angels', 'Seed', 'Presale 1', 'Presale 2', 'Public Sale'], 'Allocation / %': [equity_perc, seed_allocation, presale_1_allocation, presale_2_allocation, public_sale_allocation]}, 'Round', 'Allocation / %', info_box=None, plot_title='Fundraising Round Token Allocations')
        
    fundraising_style = fundraising_style if not show_full_fund_table else 'Custom'

    fr_return_dict = {
        "fundraising_style" : fundraising_style,
        "seed_valuation" : seed_valuation,
        "presale_1_valuation" : presale_1_valuation,
        "presale_2_valuation" : presale_2_valuation,
        "seed_raised" : seed_raised,
        "presale_1_raised" : presale_1_raised,
        "presale_2_raised" : presale_2_raised,
        "public_sale_raised" : public_sale_raised,
        "raised_funds" : raised_funds,
        "show_full_fund_table" : show_full_fund_table
    }

    return fr_return_dict
