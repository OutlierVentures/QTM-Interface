import streamlit as st

def basicTokenInformationInput(sys_param):
    """
    This function creates the basic token information section of the UI.
    """
    with st.expander("**Basic Token Information**"):
        st.markdown("### Basic Token Information")
        col11, col12, col13 = st.columns(3)            
        with col11:
            equity_investors = st.toggle('Equity Investors', value=sys_param['equity_external_shareholders_perc'][0] != 0.0, help="Enable early equity angel investors")
            initial_supply = st.number_input('Initial Total Token Supply / mil.', min_value=0.001, max_value=1000000.0, value=float(sys_param['initial_total_supply'][0]/1e6) , help="The initial total token supply.")
        with col12:
            launch_valuation = st.number_input('Public Sale Valuation / $m', min_value=0.1, max_value=500.0, value=float(sys_param['public_sale_valuation'][0]/1e6), help="This is the valuation at which the public sale tokens are sold. It is equivalent to the token launch valuation.")
            public_sale_supply = st.number_input('Public Sale Supply / %', min_value=0.0, max_value=95.0, value=float(str(sys_param['public_sale_supply_perc'][0]).split("%")[0]), help="The percentage of tokens sold in the public sale.")
            st.write("Launch Price: "+ str(launch_valuation/initial_supply)+" $/token")
        with col13:
            if equity_investors:
                equity_investments = st.number_input('Angel & Equity Raises / $m', min_value=0.0, value=float(sys_param['angel_raised'][0]/1e6), help="The amount of money raised from equity investors.")
                equity_perc = st.number_input('Equity sold / %', min_value=0.0, max_value=100.0, value=float(str(sys_param['equity_external_shareholders_perc'][0]).split("%")[0]), help="The percentage of equity sold to external shareholders.")
            else:
                equity_investments = 0.0
                equity_perc = 0.0
    
    bti_return_dict = {
        "equity_investors" : equity_investors,
        "initial_supply" : initial_supply,
        "launch_valuation" : launch_valuation,
        "public_sale_supply" : public_sale_supply,
        "equity_investments" : equity_investments,
        "equity_perc" : equity_perc
    }

    return bti_return_dict