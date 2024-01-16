import streamlit as st
from datetime import datetime

def tokenAllocationsAndVestingInput(sys_param, equity_perc, seed_raised, presale_1_raised, presale_2_raised, public_sale_raised, raised_funds, launch_valuation, seed_valuation, presale_1_valuation, presale_2_valuation, initial_supply, token_launch_date, token_launch):
    """
    This function creates the token allocations and vesting section of the UI.
    """
    with st.expander("**Token Allocations & Vesting**"):
        st.markdown("### Token Allocations & Vesting")
        vesting_dict = {} # structure: {name: {'allocation': allocation, 'initial_vesting': initial_vesting, 'cliff': cliff, 'duration': duration}}
        col31, col32 = st.columns(2)
        with col31:
            vesting_style_choices = ['Slow', 'Medium', 'Fast','Custom']
            vesting_style = st.radio('Vesting Style',tuple(vesting_style_choices), index=vesting_style_choices.index(sys_param['vesting_style'][0]) if 'vesting_style' in sys_param else 0, help=f"The vesting style determines how fast the tokens are released. The faster the higher the initial vesting and the lower the cliff and duration months.")
            if vesting_style != 'Custom':
                show_full_alloc_table = st.toggle('Show Full Table', value=False, help="Show the full token allocation and vesting table.")
            else:
                show_full_alloc_table = False
        with col32:
            incentivisation_toggle = st.toggle('Incentivisation Vesting', value=sys_param['incentivisation_allocation'][0] > 0.0, help="Enable token incentives for your ecosystem. These can have several applications, e.g. liquidity incentives or behavior/action incentives. Whenever you want to incentivize something through a fixed vesting rewards approach enable the incentivisation allocation.")
            staking_vesting_toggle = st.toggle('Staking Vesting', value=sys_param['staking_vesting_allocation'][0] > 0.0, help="Enable staking vesting token allocations. These tokens will automatically vest as rewards for stakers. Note that the QTM provides 3 different staking mechanisms: **(1) Staking Vesting (2) Staking fixed APR rewards (3) Staking revenue share buybacks and distribute rewards**. At this input you only switch on/off the staking vesting mechanism (1) as it is relevant for the initial token allocations.")
            airdrop_toggle = st.toggle('Airdrops', value=sys_param['airdrop_allocation'][0] > 0.0, help="Enable airdrops. Airdrops are a great way to distribute tokens to a large number of people. They can be used to incentivize certain actions or to reward early supporters.")

        col41, col42, col43, col44, col45 = st.columns(5)
        with col41:
            if vesting_style == 'Custom' or show_full_alloc_table:
                st.write("Name")
                if equity_perc > 0:
                    st.text_input("Angel","Angel", label_visibility="collapsed", disabled=True, key="angel_name")
                if seed_raised > 0:
                    st.text_input("Seed","Seed", label_visibility="collapsed", disabled=True, key="seed_name")
                if presale_1_raised > 0:
                    st.text_input("Presale 1","Presale 1", label_visibility="collapsed", disabled=True, key="presale_1_name")
                if presale_2_raised > 0:    
                    st.text_input("Presale 2","Presale 2", label_visibility="collapsed", disabled=True, key="presale_2_name")
                if public_sale_raised > 0:    
                    st.text_input("Public Sale","Public Sale", label_visibility="collapsed", disabled=True, key="public_sale_name")
                st.text_input("Team","Team", label_visibility="collapsed", disabled=True, key="team_name")
                st.text_input("Advisors","Advisors", label_visibility="collapsed", disabled=True, key="advisors_name")
                st.text_input("Strategic Partners","Strat. Partners", label_visibility="collapsed", disabled=True, key="partners_name")
                st.text_input("Reserve","Reserve", label_visibility="collapsed", disabled=True, key="reserve_name")
                st.text_input("Community","Community", label_visibility="collapsed", disabled=True, key="community_name")
                st.text_input("Foundation","Foundation", label_visibility="collapsed", disabled=True, key="foundation_name")
                if incentivisation_toggle:
                    st.text_input("Incentivisation","Incentivisation", label_visibility="collapsed", disabled=True, key="incentivisation_name")
                if staking_vesting_toggle:
                    st.text_input("Staking Vesting","Staking Vesting", label_visibility="collapsed", disabled=True, key="staking_vesting_name")
                if airdrop_toggle:
                    st.text_input("Airdrops","Airdrops", label_visibility="hidden", disabled=True, key="airdrops_name")
                    st.write('')
        with col42:
            if vesting_style == 'Custom' or show_full_alloc_table:
                st.write("Allocation / %")
                equity_allocation = (equity_perc/100) * (sys_param['team_allocation'][0]/(1-equity_perc/100))
                if equity_perc > 0:
                    equity_allocation_new = st.number_input('equity_allocation_new', label_visibility="collapsed", min_value=0.0, value=equity_allocation, disabled=True, key="angel_allocation")
                else:
                    equity_allocation_new = 0.0
                if seed_raised > 0:
                    seed_allocation = st.number_input('seed_allocation', label_visibility="collapsed", min_value=0.0, value=((seed_raised) / ((seed_valuation)/initial_supply) / initial_supply) * 1e2, disabled=True, key="seed_allocation")
                else:
                    seed_allocation = 0.0
                if presale_1_raised > 0:
                    presale_1_allocation = st.number_input('presale_1_allocation', label_visibility="collapsed", min_value=0.0, value=((presale_1_raised) / ((presale_1_valuation)/initial_supply) / initial_supply) * 1e2, disabled=True, key="presale_1_allocation")
                else:
                    presale_1_allocation = 0.0
                if presale_2_raised > 0:
                    presale_2_allocation = st.number_input('presale_2_allocation', label_visibility="collapsed", min_value=0.0, value=((presale_2_raised) / ((presale_2_valuation)/initial_supply) / initial_supply) * 1e2, disabled=True, key="presale_2_allocation")   
                else:
                    presale_2_allocation = 0.0
                if public_sale_raised > 0:
                    public_sale_allocation = st.number_input('public_sale_allocation', label_visibility="collapsed", min_value=0.0, value=((public_sale_raised) / ((launch_valuation)/initial_supply) / initial_supply) * 1e2, disabled=True, key="public_sale_allocation")
                else:
                    public_sale_allocation = 0.0
                team_allocation = st.number_input('team_allocation', label_visibility="collapsed", min_value=0.0, value=sys_param['team_allocation'][0], disabled=False, key="team_allocation")
                ov_advisor_allocation = st.number_input('ov_advisor_allocation', label_visibility="collapsed", min_value=0.0, value=sys_param['ov_allocation'][0]+sys_param['advisor_allocation'][0], disabled=False, key="ov_advisor_allocation")
                strategic_partners_allocation = st.number_input('strategic_partners_allocation', label_visibility="collapsed", min_value=0.0, value=sys_param['strategic_partners_allocation'][0], disabled=False, key="partner_allocation")
                reserve_allocation = st.number_input('reserve_allocation', label_visibility="collapsed", min_value=0.0, value=sys_param['reserve_allocation'][0], disabled=False, key="reserve_allocation")
                community_allocation = st.number_input('community_allocation', label_visibility="collapsed", min_value=0.0, value=sys_param['community_allocation'][0], disabled=False, key="community_allocation")
                foundation_allocation = st.number_input('foundation_allocation', label_visibility="collapsed", min_value=0.0, value=sys_param['foundation_allocation'][0], disabled=False, key="foundation_allocation")
                if incentivisation_toggle:
                    incentivisation_allocation = st.number_input('incentivisation_allocation', label_visibility="collapsed", min_value=0.0, value=sys_param['incentivisation_allocation'][0], disabled=False, key="incentivisation_allocation")
                else:
                    incentivisation_allocation = 0.0
                if staking_vesting_toggle:
                    staking_vesting_allocation = st.number_input('staking_vesting_allocation', label_visibility="collapsed", min_value=0.0, value=sys_param['staking_vesting_allocation'][0], disabled=False, key="staking_vesting_allocation")
                else:
                    staking_vesting_allocation = 0.0
                if airdrop_toggle:
                    airdrop_allocation = st.number_input('airdrop_allocation', label_visibility="hidden", min_value=0.0, value=sys_param['airdrop_allocation'][0], disabled=False, key="airdrop_allocation")
                else:
                    airdrop_allocation = 0.0
                lp_allocation = (100 - equity_allocation_new - seed_allocation - presale_1_allocation
                                - presale_2_allocation - public_sale_allocation - team_allocation - ov_advisor_allocation
                                - strategic_partners_allocation - reserve_allocation - community_allocation
                                - foundation_allocation - incentivisation_allocation - staking_vesting_allocation
                                - airdrop_allocation)

            else:
                equity_allocation_new = (equity_perc/100) * (sys_param['team_allocation'][0]/(1-equity_perc/100))
                seed_allocation = ((seed_raised) / ((seed_valuation)/initial_supply) / initial_supply) * 1e2
                presale_1_allocation = ((presale_1_raised) / ((presale_1_valuation)/initial_supply) / initial_supply) * 1e2
                presale_2_allocation = ((presale_2_raised) / ((presale_2_valuation)/initial_supply) / initial_supply) * 1e2
                public_sale_allocation = ((public_sale_raised) / ((launch_valuation)/initial_supply) / initial_supply) * 1e2
                team_allocation = sys_param['team_allocation'][0]
                ov_advisor_allocation = sys_param['ov_allocation'][0]+sys_param['advisor_allocation'][0]
                strategic_partners_allocation = sys_param['strategic_partners_allocation'][0]
                reserve_allocation = sys_param['reserve_allocation'][0]
                community_allocation = sys_param['community_allocation'][0]
                foundation_allocation = sys_param['foundation_allocation'][0]
                incentivisation_allocation = sys_param['incentivisation_allocation'][0]
                staking_vesting_allocation = sys_param['staking_vesting_allocation'][0]
                airdrop_allocation = sys_param['airdrop_allocation'][0]
                airdrop_amount1 = sys_param['airdrop_amount1'][0]
                airdrop_amount2 = sys_param['airdrop_amount2'][0]
                airdrop_amount3 = sys_param['airdrop_amount3'][0]
                airdrop_date1 = datetime.strptime(sys_param['airdrop_date1'][0], "%d.%m.%Y")
                airdrop_date2 = datetime.strptime(sys_param['airdrop_date2'][0], "%d.%m.%Y")
                airdrop_date3 = datetime.strptime(sys_param['airdrop_date3'][0], "%d.%m.%Y")
                lp_allocation = (100 - equity_allocation_new - seed_allocation - presale_1_allocation
                                - presale_2_allocation - public_sale_allocation - team_allocation - ov_advisor_allocation
                                - strategic_partners_allocation - reserve_allocation - community_allocation
                                - foundation_allocation - incentivisation_allocation - staking_vesting_allocation
                                - airdrop_allocation)

                
        with col43:
            if vesting_style == 'Slow':
                init_vesting_dict = {
                    "angel" : 0.0,
                    "seed" : 0.0,
                    "presale_1" : 0.0,
                    "presale_2" : 0.0,
                    "public_sale" : 10.0,
                    "team" : 0.0,
                    "advisor" : 0.0,
                    "strategic_partners" : 0.0,
                    "reserve" : 10.0,
                    "community" : 10.0,
                    "foundation" : 10.0,
                    "incentivisation" : 0.0,
                    "staking_vesting" : 0.0
                }
            if vesting_style == 'Medium':
                init_vesting_dict = {
                    "angel" : 0.0,
                    "seed" : 0.0,
                    "presale_1" : 0.0,
                    "presale_2" : 5.0,
                    "public_sale" : 15.0,
                    "team" : 0.0,
                    "advisor" : 0.0,
                    "strategic_partners" : 0.0,
                    "reserve" : 10.0,
                    "community" : 10.0,
                    "foundation" : 10.0,
                    "incentivisation" : 0.0,
                    "staking_vesting" : 0.0
                }
            if vesting_style == 'Fast':
                init_vesting_dict = {
                    "angel" : 0.0,
                    "seed" : 0.0,
                    "presale_1" : 5.0,
                    "presale_2" : 15.0,
                    "public_sale" : 35.0,
                    "team" : 0.0,
                    "advisor" : 0.0,
                    "strategic_partners" : 0.0,
                    "reserve" : 25.0,
                    "community" : 25.0,
                    "foundation" : 25.0,
                    "incentivisation" : 5.0,
                    "staking_vesting" : 5.0
                }
            if vesting_style == 'Custom' or show_full_alloc_table:
                st.write("Init. Vesting / %")
                if equity_perc > 0:
                    angel_initial_vesting = st.number_input("angel_initial_vesting", label_visibility="collapsed", min_value=0.0, value=[sys_param['angel_initial_vesting'][0] if vesting_style == 'Custom' else init_vesting_dict['angel']][0], key="angel_initial_vesting")
                else:
                    angel_initial_vesting = 0.0
                if seed_raised > 0:
                    seed_initial_vesting = st.number_input("seed_initial_vesting", label_visibility="collapsed", min_value=0.0, value=[sys_param['seed_initial_vesting'][0] if vesting_style == 'Custom' else init_vesting_dict['seed']][0], key="seed_initial_vesting")
                else:
                    seed_initial_vesting = 0.0
                if presale_1_raised > 0:
                    presale_1_initial_vesting = st.number_input("presale_1_initial_vesting", label_visibility="collapsed", min_value=0.0, value=[sys_param['presale_1_initial_vesting'][0] if vesting_style == 'Custom' else init_vesting_dict['presale_1']][0], key="presale_1_initial_vesting")
                else:
                    presale_1_initial_vesting = 0.0
                if presale_2_raised > 0:
                    presale_2_initial_vesting = st.number_input("presale_2_initial_vesting", label_visibility="collapsed", min_value=0.0, value=[sys_param['presale_2_initial_vesting'][0] if vesting_style == 'Custom' else init_vesting_dict['presale_2']][0], key="presale_2_initial_vesting")
                else:
                    presale_2_initial_vesting = 0.0
                if public_sale_raised > 0:
                    public_sale_initial_vesting = st.number_input("public_sale_initial_vesting", label_visibility="collapsed", min_value=0.0, value=[sys_param['public_sale_initial_vesting'][0] if vesting_style == 'Custom' else init_vesting_dict['public_sale']][0], key="public_sale_initial_vesting")
                else:
                    public_sale_initial_vesting = 0.0
                team_initial_vesting = st.number_input("team_initial_vesting", label_visibility="collapsed", min_value=0.0, value=[sys_param['team_initial_vesting'][0] if vesting_style == 'Custom' else init_vesting_dict['team']][0], key="team_initial_vesting")
                advisor_initial_vesting = st.number_input("advisor_initial_vesting", label_visibility="collapsed", min_value=0.0, value=[(sys_param['ov_initial_vesting'][0]+sys_param['advisor_initial_vesting'][0])/2 if vesting_style == 'Custom' else init_vesting_dict['advisor']][0], key="advisor_initial_vesting")
                strategic_partners_initial_vesting = st.number_input("strategic_partners_initial_vesting", label_visibility="collapsed", min_value=0.0, value=[sys_param['strategic_partners_initial_vesting'][0] if vesting_style == 'Custom' else init_vesting_dict['strategic_partners']][0], key="strategic_partners_initial_vesting")
                reserve_initial_vesting = st.number_input("reserve_initial_vesting", label_visibility="collapsed", min_value=0.0, value=[sys_param['reserve_initial_vesting'][0] if vesting_style == 'Custom' else init_vesting_dict['reserve']][0], key="reserve_initial_vesting")
                community_initial_vesting = st.number_input("community_initial_vesting", label_visibility="collapsed", min_value=0.0, value=[sys_param['community_initial_vesting'][0] if vesting_style == 'Custom' else init_vesting_dict['community']][0], key="community_initial_vesting")
                foundation_initial_vesting = st.number_input("foundation_initial_vesting", label_visibility="collapsed", min_value=0.0, value=[sys_param['foundation_initial_vesting'][0] if vesting_style == 'Custom' else init_vesting_dict['foundation']][0], key="foundation_initial_vesting")
                if incentivisation_toggle:
                    incentivisation_initial_vesting = st.number_input("incentivisation_initial_vesting", label_visibility="collapsed", min_value=0.0, value=[sys_param['incentivisation_initial_vesting'][0] if vesting_style == 'Custom' else init_vesting_dict['incentivisation']][0], key="incentivisation_initial_vesting")
                else:
                    incentivisation_initial_vesting = 0.0
                if staking_vesting_toggle:
                    staking_vesting_initial_vesting = st.number_input("staking_vesting_initial_vesting", label_visibility="collapsed", min_value=0.0, value=[sys_param['staking_vesting_initial_vesting'][0] if vesting_style == 'Custom' else init_vesting_dict['staking_vesting']][0], key="staking_vesting_initial_vesting")
                else:
                    staking_vesting_initial_vesting = 0.0
                if airdrop_toggle:
                    airdrop_date1 = st.date_input("Airdrop Date 1", min_value=token_launch_date, value=datetime.strptime(sys_param['airdrop_date1'][0], "%d.%m.%Y"), help="The date of the first airdrop.")
                    airdrop_amount1 = st.number_input("Amount 1 / %", min_value=0.0, value=sys_param['airdrop_amount1'][0], help="The share of tokens distributed from the airdrop allocation in the first airdrop.")

        with col44:
            if vesting_style == 'Slow':
                cliff_dict = {
                    "angel" : 24,
                    "seed" : 18,
                    "presale_1" : 12,
                    "presale_2" : 9,
                    "public_sale" : 3,
                    "team" : 24,
                    "advisor" : 18,
                    "strategic_partners" : 18,
                    "reserve" : 0,
                    "community" : 0,
                    "foundation" : 0,
                    "incentivisation" : 0,
                    "staking_vesting" : 0
                }
            if vesting_style == 'Medium':
                cliff_dict = {
                    "angel" : 18,
                    "seed" : 12,
                    "presale_1" : 9,
                    "presale_2" : 6,
                    "public_sale" : 0,
                    "team" : 18,
                    "advisor" : 12,
                    "strategic_partners" : 12,
                    "reserve" : 0,
                    "community" : 0,
                    "foundation" : 0,
                    "incentivisation" : 0,
                    "staking_vesting" : 0
                }
            if vesting_style == 'Fast':
                cliff_dict = {
                    "angel" : 12,
                    "seed" : 9,
                    "presale_1" : 6,
                    "presale_2" : 3,
                    "public_sale" : 0,
                    "team" : 12,
                    "advisor" : 9,
                    "strategic_partners" : 9,
                    "reserve" : 0,
                    "community" : 0,
                    "foundation" : 0,
                    "incentivisation" : 0,
                    "staking_vesting" : 0
                }
            if vesting_style == 'Custom' or show_full_alloc_table:
                st.write("Cliff / Mon.")
                if equity_perc > 0:
                    angel_cliff = st.number_input("angel_cliff", label_visibility="collapsed", min_value=0, value=int([sys_param['angel_cliff'][0] if vesting_style == 'Custom' else cliff_dict['angel']][0]), key="angel_cliff")
                else:
                    angel_cliff = 0.0
                if seed_raised > 0:
                    seed_cliff = st.number_input("seed_cliff", label_visibility="collapsed", min_value=0, value=int([sys_param['seed_cliff'][0] if vesting_style == 'Custom' else cliff_dict['seed']][0]), key="seed_cliff")
                else:
                    seed_cliff = 0.0
                if presale_1_raised:
                    presale_1_cliff = st.number_input("presale_1_cliff", label_visibility="collapsed", min_value=0, value=int([sys_param['presale_1_cliff'][0] if vesting_style == 'Custom' else cliff_dict['presale_1']][0]), key="presale_1_cliff")
                else:
                    presale_1_cliff = 0.0
                if presale_2_raised > 0:
                    presale_2_cliff = st.number_input("presale_2_cliff", label_visibility="collapsed", min_value=0, value=int([sys_param['presale_2_cliff'][0] if vesting_style == 'Custom' else cliff_dict['presale_2']][0]), key="presale_2_cliff")
                else:
                    presale_2_cliff = 0.0
                if public_sale_raised > 0:
                    public_sale_cliff = st.number_input("public_sale_cliff", label_visibility="collapsed", min_value=0, value=int([sys_param['public_sale_cliff'][0] if vesting_style == 'Custom' else cliff_dict['public_sale']][0]), key="public_sale_cliff")
                else:
                    public_sale_cliff = 0.0
                team_cliff = st.number_input("team_cliff", label_visibility="collapsed", min_value=0, value=int([sys_param['team_cliff'][0] if vesting_style == 'Custom' else cliff_dict['team']][0]), key="team_cliff")
                advisor_cliff = st.number_input("advisor_cliff", label_visibility="collapsed", min_value=0, value=int([sys_param['advisor_cliff'][0] if vesting_style == 'Custom' else cliff_dict['advisor']][0]), key="advisor_cliff")
                strategic_partners_cliff = st.number_input("strategic_partners_cliff", label_visibility="collapsed", min_value=0, value=int([sys_param['strategic_partners_cliff'][0] if vesting_style == 'Custom' else cliff_dict['strategic_partners']][0]), key="strategic_partners_cliff")
                reserve_cliff = st.number_input("reserve_cliff", label_visibility="collapsed", min_value=0, value=int([sys_param['reserve_cliff'][0] if vesting_style == 'Custom' else cliff_dict['reserve']][0]), key="reserve_cliff")
                community_cliff = st.number_input("community_cliff", label_visibility="collapsed", min_value=0, value=int([sys_param['community_cliff'][0] if vesting_style == 'Custom' else cliff_dict['community']][0]), key="community_cliff")
                foundation_cliff = st.number_input("foundation_cliff", label_visibility="collapsed", min_value=0, value=int([sys_param['foundation_cliff'][0] if vesting_style == 'Custom' else cliff_dict['foundation']][0]), key="foundation_cliff")
                if incentivisation_toggle:
                    incentivisation_cliff = st.number_input("incentivisation_cliff", label_visibility="collapsed", min_value=0, value=int([sys_param['incentivisation_cliff'][0] if vesting_style == 'Custom' else cliff_dict['incentivisation']][0]), key="incentivisation_cliff")
                else:
                    incentivisation_cliff = 0.0
                if staking_vesting_toggle:
                    staking_vesting_cliff = st.number_input("staking_vesting_cliff", label_visibility="collapsed", min_value=0, value=int([sys_param['staking_vesting_cliff'][0] if vesting_style == 'Custom' else cliff_dict['staking_vesting']][0]), key="staking_vesting_cliff")
                else:
                    staking_vesting_cliff = 0.0
                if airdrop_toggle:
                    airdrop_date2 = st.date_input("Airdrop Date 2", min_value=token_launch_date, value=datetime.strptime(sys_param['airdrop_date2'][0], "%d.%m.%Y"), help="The date of the second airdrop.")
                    airdrop_amount2 = st.number_input("Amount 2 / %", min_value=0.0, value=sys_param['airdrop_amount2'][0], help="The share of tokens distributed from the airdrop allocation in the second airdrop.")
    
        with col45:
            if vesting_style == 'Slow':
                duration_dict = {
                    "angel" : 72,
                    "seed" : 48,
                    "presale_1" : 36,
                    "presale_2" : 24,
                    "public_sale" : 12,
                    "team" : 72,
                    "advisor" : 48,
                    "strategic_partners" : 48,
                    "reserve" : 72,
                    "community" : 72,
                    "foundation" : 72,
                    "incentivisation" : 72,
                    "staking_vesting" : 72
                }
            if vesting_style == 'Medium':
                duration_dict = {
                    "angel" : 48,
                    "seed" : 36,
                    "presale_1" : 24,
                    "presale_2" : 12,
                    "public_sale" : 6,
                    "team" : 48,
                    "advisor" : 36,
                    "strategic_partners" : 36,
                    "reserve" : 48,
                    "community" : 48,
                    "foundation" : 48,
                    "incentivisation" : 48,
                    "staking_vesting" : 48
                }
            if vesting_style == 'Fast':
                duration_dict = {
                    "angel" : 36,
                    "seed" : 24,
                    "presale_1" : 12,
                    "presale_2" : 6,
                    "public_sale" : 3,
                    "team" : 36,
                    "advisor" : 24,
                    "strategic_partners" : 24,
                    "reserve" : 24,
                    "community" : 24,
                    "foundation" : 24,
                    "incentivisation" : 24,
                    "staking_vesting" : 24
                }
            if vesting_style == 'Custom' or show_full_alloc_table:
                st.write("Duration / Mon.")
                if equity_perc > 0:
                    angel_duration = st.number_input("angel_duration", label_visibility="collapsed", min_value=0, value=int([sys_param['angel_vesting_duration'][0] if vesting_style == 'Custom' else duration_dict['angel']][0]), key="angel_vesting_duration")
                else:
                    angel_duration = 0.0
                if seed_raised > 0:
                    seed_duration = st.number_input("seed_duration", label_visibility="collapsed", min_value=0, value=int([sys_param['seed_vesting_duration'][0] if vesting_style == 'Custom' else duration_dict['seed']][0]), key="seed_vesting_duration")
                else:
                    seed_duration = 0.0
                if presale_1_raised > 0:
                    presale_1_duration = st.number_input("presale_1_duration", label_visibility="collapsed", min_value=0, value=int([sys_param['presale_1_vesting_duration'][0] if vesting_style == 'Custom' else duration_dict['presale_1']][0]), key="presale_1_vesting_duration")
                else:
                    presale_1_duration = 0.0
                if presale_2_raised > 0:
                    presale_2_duration = st.number_input("presale_2_duration", label_visibility="collapsed", min_value=0, value=int([sys_param['presale_2_vesting_duration'][0] if vesting_style == 'Custom' else duration_dict['presale_2']][0]), key="presale_2_vesting_duration")
                else:
                    presale_2_duration = 0.0
                if public_sale_raised > 0:
                    public_sale_duration = st.number_input("public_sale_duration", label_visibility="collapsed", min_value=0, value=int([sys_param['public_sale_vesting_duration'][0] if vesting_style == 'Custom' else duration_dict['public_sale']][0]), key="public_sale_vesting_duration")
                else:
                    public_sale_duration = 0.0
                team_duration = st.number_input("team_duration", label_visibility="collapsed", min_value=0, value=int([sys_param['team_vesting_duration'][0] if vesting_style == 'Custom' else duration_dict['team']][0]), key="team_vesting_duration")
                advisor_duration = st.number_input("advisor_duration", label_visibility="collapsed", min_value=0, value=int([(sys_param['advisor_vesting_duration'][0] + sys_param['ov_vesting_duration'][0])/2 if vesting_style == 'Custom' else duration_dict['advisor']][0]), key="advisor_vesting_duration")
                strategic_partners_duration = st.number_input("strategic_partners_duration", label_visibility="collapsed", min_value=0, value=int([sys_param['strategic_partner_vesting_duration'][0] if vesting_style == 'Custom' else duration_dict['strategic_partners']][0]), key="strategic_partners_vesting_duration")
                reserve_duration = st.number_input("reserve_duration", label_visibility="collapsed", min_value=0, value=int([sys_param['reserve_vesting_duration'][0] if vesting_style == 'Custom' else duration_dict['reserve']][0]), key="reserve_vesting_duration")
                community_duration = st.number_input("community_duration", label_visibility="collapsed", min_value=0, value=int([sys_param['community_vesting_duration'][0] if vesting_style == 'Custom' else duration_dict['community']][0]), key="community_vesting_duration")
                foundation_duration = st.number_input("foundation_duration", label_visibility="collapsed", min_value=0, value=int([sys_param['foundation_vesting_duration'][0] if vesting_style == 'Custom' else duration_dict['foundation']][0]), key="foundation_vesting_duration")
                if incentivisation_toggle:
                    incentivisation_duration = st.number_input("incentivisation_duration", label_visibility="collapsed", min_value=0, value=int([sys_param['incentivisation_vesting_duration'][0] if vesting_style == 'Custom' else duration_dict['incentivisation']][0]), key="incentivisation_vesting_duration")
                else:
                    incentivisation_duration = 0.0
                if staking_vesting_toggle:
                    staking_vesting_duration = st.number_input("staking_vesting_duration", label_visibility="collapsed", min_value=0, value=int([sys_param['staking_vesting_vesting_duration'][0] if vesting_style == 'Custom' else duration_dict['staking_vesting']][0]), key="staking_vesting_vesting_duration")
                else:
                    staking_vesting_duration = 0.0
                if airdrop_toggle:
                    airdrop_date3 = st.date_input("Airdrop Date 3", min_value=token_launch_date, value=datetime.strptime(sys_param['airdrop_date3'][0], "%d.%m.%Y"), help="The date of the third airdrop.")
                    airdrop_amount3 = st.number_input("Amount 3 / %", min_value=0.0, value=sys_param['airdrop_amount3'][0], help="The share of tokens distributed from the airdrop allocation in the third airdrop.")

        if token_launch:
            if show_full_alloc_table or vesting_style == 'Custom':
                col51, col52, col53 = st.columns(3)
                with col51:
                    st.text_input("DEX LP","DEX Liquidity Pool", label_visibility="hidden", disabled=True, key="lp_name")
                with col52:
                    st.number_input('LP Token Allocation / %', label_visibility="visible", value=lp_allocation, disabled=True, key="lp_allocation", help="The percentage of tokens allocated to the liquidity pool. This is the remaining percentage of tokens after all other allocations have been made. It must not be < 0 and determines the required capital to seed the liquidity.")
                with col53:
                    dex_capital = st.number_input('DEX Capital / $m', value=float((lp_allocation/100 )* initial_supply * launch_valuation / initial_supply), disabled=True, key="liquidity_capital_requirements", help="The required capital to seed the liquidity: lp_allocation x total_initial_supply / 100 % * token_launch_price.")
            else:
                dex_capital = (lp_allocation/100 )* initial_supply * launch_valuation / initial_supply
            if dex_capital > raised_funds:
                st.error(f"The required capital ({round(dex_capital,2)}m) to seed the liquidity is higher than the raised funds (${round(raised_funds,2)}m). Please reduce the LP Token Allocation or the Launch Valuation!", icon="⚠️")
            if lp_allocation < 0:
                st.error(f"The LP token allocation ({round(lp_allocation,2)}%) is negative. Please increase the token launch valuation or reduce stakeholder allocations!", icon="⚠️")
        
        else:
            dex_capital = 0.0
        
        airdrop_date1 = datetime(airdrop_date1.year, airdrop_date1.month, airdrop_date1.day)
        airdrop_date2 = datetime(airdrop_date2.year, airdrop_date2.month, airdrop_date2.day)
        airdrop_date3 = datetime(airdrop_date3.year, airdrop_date3.month, airdrop_date3.day)

        if airdrop_toggle:
            if airdrop_date1 < token_launch_date:
                st.error(f"The first airdrop date ({airdrop_date1.strftime('%d.%m.%Y')}) is before the launch date ({token_launch_date}). Please adjust the airdrop date!", icon="⚠️")
            if airdrop_date2 < token_launch_date:
                st.error(f"The second airdrop date ({airdrop_date2.strftime('%d.%m.%Y')}) is before the launch date ({token_launch_date}). Please adjust the airdrop date!", icon="⚠️")
            if airdrop_date3 < token_launch_date:
                st.error(f"The third airdrop date ({airdrop_date3.strftime('%d.%m.%Y')}) is before the launch date ({token_launch_date}). Please adjust the airdrop date!", icon="⚠️")
        
                
        airdrop_dict = {
            'ad1': {
                'date': [airdrop_date1.strftime('%d.%m.%Y') if airdrop_toggle else sys_param['airdrop_date1'][0]][0],
                'amount': [airdrop_amount1 if airdrop_toggle else sys_param['airdrop_amount1'][0]][0]
            },
            'ad2': {
                'date': [airdrop_date2.strftime('%d.%m.%Y') if airdrop_toggle else sys_param['airdrop_date2'][0]][0],
                'amount': [airdrop_amount2 if airdrop_toggle else sys_param['airdrop_amount2'][0]][0]
            },
            'ad3': {
                'date': [airdrop_date3.strftime('%d.%m.%Y') if airdrop_toggle else sys_param['airdrop_date3'][0]][0],
                'amount': [airdrop_amount3 if airdrop_toggle else sys_param['airdrop_amount3'][0]][0]
            }}

        # fill vesting_dict
        vesting_dict = {
            "angel" : {
                "allocation" : equity_allocation_new,
                "initial_vesting" : [angel_initial_vesting if vesting_style == 'Custom' or show_full_alloc_table else init_vesting_dict['angel']][0],
                "cliff" : [angel_cliff if vesting_style == 'Custom' or show_full_alloc_table else cliff_dict['angel']][0],
                "duration" : [angel_duration if vesting_style == 'Custom' or show_full_alloc_table else duration_dict['angel']][0]
            },
            "seed" : {
                "allocation" : seed_allocation,
                "initial_vesting" : [seed_initial_vesting if vesting_style == 'Custom' or show_full_alloc_table else init_vesting_dict['seed']][0],
                "cliff" : [seed_cliff if vesting_style == 'Custom' or show_full_alloc_table else cliff_dict['seed']][0],
                "duration" : [seed_duration if vesting_style == 'Custom' or show_full_alloc_table else duration_dict['seed']][0]
            },
            "presale_1" : {
                "allocation" : presale_1_allocation,
                "initial_vesting" : [presale_1_initial_vesting if vesting_style == 'Custom' or show_full_alloc_table else init_vesting_dict['presale_1']][0],
                "cliff" : [presale_1_cliff if vesting_style == 'Custom' or show_full_alloc_table else cliff_dict['presale_1']][0],
                "duration" : [presale_1_duration if vesting_style == 'Custom' or show_full_alloc_table else duration_dict['presale_1']][0]
            },
            "presale_2" : {
                "allocation" : presale_2_allocation,
                "initial_vesting" : [presale_2_initial_vesting if vesting_style == 'Custom' or show_full_alloc_table else init_vesting_dict['presale_2']][0],
                "cliff" : [presale_2_cliff if vesting_style == 'Custom' or show_full_alloc_table else cliff_dict['presale_2']][0],
                "duration" : [presale_2_duration if vesting_style == 'Custom' or show_full_alloc_table else duration_dict['presale_2']][0]
            },
            "public_sale" : {
                "allocation" : public_sale_allocation,
                "initial_vesting" : [public_sale_initial_vesting if vesting_style == 'Custom' or show_full_alloc_table else init_vesting_dict['public_sale']][0],
                "cliff" : [public_sale_cliff if vesting_style == 'Custom' or show_full_alloc_table else cliff_dict['public_sale']][0],
                "duration" : [public_sale_duration if vesting_style == 'Custom' or show_full_alloc_table else duration_dict['public_sale']][0]
            },
            "team" : {
                "allocation" : team_allocation,
                "initial_vesting" : [team_initial_vesting if vesting_style == 'Custom' or show_full_alloc_table else init_vesting_dict['team']][0],
                "cliff" : [team_cliff if vesting_style == 'Custom' or show_full_alloc_table else cliff_dict['team']][0],
                "duration" : [team_duration if vesting_style == 'Custom' or show_full_alloc_table else duration_dict['team']][0]
            },
            "advisor" : {
                "allocation" : ov_advisor_allocation,
                "initial_vesting" : [advisor_initial_vesting if vesting_style == 'Custom' or show_full_alloc_table else init_vesting_dict['advisor']][0],
                "cliff" : [advisor_cliff if vesting_style == 'Custom' or show_full_alloc_table else cliff_dict['advisor']][0],
                "duration" : [advisor_duration if vesting_style == 'Custom' or show_full_alloc_table else duration_dict['advisor']][0]
            },
            "strategic_partners" : {
                "allocation" : strategic_partners_allocation,
                "initial_vesting" : [strategic_partners_initial_vesting if vesting_style == 'Custom' or show_full_alloc_table else init_vesting_dict['strategic_partners']][0],
                "cliff" : [strategic_partners_cliff if vesting_style == 'Custom' or show_full_alloc_table else cliff_dict['strategic_partners']][0],
                "duration" : [strategic_partners_duration if vesting_style == 'Custom' or show_full_alloc_table else duration_dict['strategic_partners']][0]
            },
            "reserve" : {
                "allocation" : reserve_allocation,
                "initial_vesting" : [reserve_initial_vesting if vesting_style == 'Custom' or show_full_alloc_table else init_vesting_dict['reserve']][0],
                "cliff" : [reserve_cliff if vesting_style == 'Custom' or show_full_alloc_table else cliff_dict['reserve']][0],
                "duration" : [reserve_duration if vesting_style == 'Custom' or show_full_alloc_table else duration_dict['reserve']][0]
            },
            "community" : {
                "allocation" : community_allocation,
                "initial_vesting" : [community_initial_vesting if vesting_style == 'Custom' or show_full_alloc_table else init_vesting_dict['community']][0],
                "cliff" : [community_cliff if vesting_style == 'Custom' or show_full_alloc_table else cliff_dict['community']][0],
                "duration" : [community_duration if vesting_style == 'Custom' or show_full_alloc_table else duration_dict['community']][0]
            },
            "foundation" : {
                "allocation" : foundation_allocation,
                "initial_vesting" : [foundation_initial_vesting if vesting_style == 'Custom' or show_full_alloc_table else init_vesting_dict['foundation']][0],
                "cliff" : [foundation_cliff if vesting_style == 'Custom' or show_full_alloc_table else cliff_dict['foundation']][0],
                "duration" : [foundation_duration if vesting_style == 'Custom' or show_full_alloc_table else duration_dict['foundation']][0]
            },
            "incentivisation" : {
                "allocation" : incentivisation_allocation,
                "initial_vesting" : [incentivisation_initial_vesting if vesting_style == 'Custom' or show_full_alloc_table else init_vesting_dict['incentivisation']][0],
                "cliff" : [incentivisation_cliff if vesting_style == 'Custom' or show_full_alloc_table else cliff_dict['incentivisation']][0],
                "duration" : [incentivisation_duration if vesting_style == 'Custom' or show_full_alloc_table else duration_dict['incentivisation']][0]
            },
            "staking_vesting" : {
                "allocation" : staking_vesting_allocation,
                "initial_vesting" : [staking_vesting_initial_vesting if vesting_style == 'Custom' or show_full_alloc_table else init_vesting_dict['staking_vesting']][0],
                "cliff" : [staking_vesting_cliff if vesting_style == 'Custom' or show_full_alloc_table else cliff_dict['staking_vesting']][0],
                "duration" : [staking_vesting_duration if vesting_style == 'Custom' or show_full_alloc_table else duration_dict['staking_vesting']][0]
            }            
        }

    angel_initial_vesting = [angel_initial_vesting if vesting_style == 'Custom' or show_full_alloc_table else init_vesting_dict['angel']][0]
    angel_cliff = [angel_cliff if vesting_style == 'Custom' or show_full_alloc_table else cliff_dict['angel']][0]
    angel_duration = [angel_duration if vesting_style == 'Custom' or show_full_alloc_table else duration_dict['angel']][0]
    seed_initial_vesting = [seed_initial_vesting if vesting_style == 'Custom' or show_full_alloc_table else init_vesting_dict['seed']][0]
    seed_cliff = [seed_cliff if vesting_style == 'Custom' or show_full_alloc_table else cliff_dict['seed']][0]
    seed_duration = [seed_duration if vesting_style == 'Custom' or show_full_alloc_table else duration_dict['seed']][0]
    presale_1_initial_vesting = [presale_1_initial_vesting if vesting_style == 'Custom' or show_full_alloc_table else init_vesting_dict['presale_1']][0]
    presale_1_cliff = [presale_1_cliff if vesting_style == 'Custom' or show_full_alloc_table else cliff_dict['presale_1']][0]
    presale_1_duration = [presale_1_duration if vesting_style == 'Custom' or show_full_alloc_table else duration_dict['presale_1']][0]
    presale_2_initial_vesting = [presale_2_initial_vesting if vesting_style == 'Custom' or show_full_alloc_table else init_vesting_dict['presale_2']][0]
    presale_2_cliff = [presale_2_cliff if vesting_style == 'Custom' or show_full_alloc_table else cliff_dict['presale_2']][0]
    presale_2_duration = [presale_2_duration if vesting_style == 'Custom' or show_full_alloc_table else duration_dict['presale_2']][0]
    public_sale_initial_vesting = [public_sale_initial_vesting if vesting_style == 'Custom' or show_full_alloc_table else init_vesting_dict['public_sale']][0]
    public_sale_cliff = [public_sale_cliff if vesting_style == 'Custom' or show_full_alloc_table else cliff_dict['public_sale']][0]
    public_sale_duration = [public_sale_duration if vesting_style == 'Custom' or show_full_alloc_table else duration_dict['public_sale']][0]
    team_initial_vesting = [team_initial_vesting if vesting_style == 'Custom' or show_full_alloc_table else init_vesting_dict['team']][0]
    team_cliff = [team_cliff if vesting_style == 'Custom' or show_full_alloc_table else cliff_dict['team']][0]
    team_duration = [team_duration if vesting_style == 'Custom' or show_full_alloc_table else duration_dict['team']][0]
    advisor_initial_vesting = [advisor_initial_vesting if vesting_style == 'Custom' or show_full_alloc_table else init_vesting_dict['advisor']][0]
    advisor_cliff = [advisor_cliff if vesting_style == 'Custom' or show_full_alloc_table else cliff_dict['advisor']][0]
    advisor_duration = [advisor_duration if vesting_style == 'Custom' or show_full_alloc_table else duration_dict['advisor']][0]
    strategic_partners_initial_vesting = [strategic_partners_initial_vesting if vesting_style == 'Custom' or show_full_alloc_table else init_vesting_dict['strategic_partners']][0]
    strategic_partners_cliff = [strategic_partners_cliff if vesting_style == 'Custom' or show_full_alloc_table else cliff_dict['strategic_partners']][0]
    strategic_partners_duration = [strategic_partners_duration if vesting_style == 'Custom' or show_full_alloc_table else duration_dict['strategic_partners']][0]
    reserve_initial_vesting = [reserve_initial_vesting if vesting_style == 'Custom' or show_full_alloc_table else init_vesting_dict['reserve']][0]
    reserve_cliff = [reserve_cliff if vesting_style == 'Custom' or show_full_alloc_table else cliff_dict['reserve']][0]
    reserve_duration = [reserve_duration if vesting_style == 'Custom' or show_full_alloc_table else duration_dict['reserve']][0]
    community_initial_vesting = [community_initial_vesting if vesting_style == 'Custom' or show_full_alloc_table else init_vesting_dict['community']][0]
    community_cliff = [community_cliff if vesting_style == 'Custom' or show_full_alloc_table else cliff_dict['community']][0]
    community_duration = [community_duration if vesting_style == 'Custom' or show_full_alloc_table else duration_dict['community']][0]
    foundation_initial_vesting = [foundation_initial_vesting if vesting_style == 'Custom' or show_full_alloc_table else init_vesting_dict['foundation']][0]
    foundation_cliff = [foundation_cliff if vesting_style == 'Custom' or show_full_alloc_table else cliff_dict['foundation']][0]
    foundation_duration = [foundation_duration if vesting_style == 'Custom' or show_full_alloc_table else duration_dict['foundation']][0]
    incentivisation_initial_vesting = [incentivisation_initial_vesting if vesting_style == 'Custom' or show_full_alloc_table else init_vesting_dict['incentivisation']][0]
    incentivisation_cliff = [incentivisation_cliff if vesting_style == 'Custom' or show_full_alloc_table else cliff_dict['incentivisation']][0]
    incentivisation_duration = [incentivisation_duration if vesting_style == 'Custom' or show_full_alloc_table else duration_dict['incentivisation']][0]
    staking_vesting_initial_vesting = [staking_vesting_initial_vesting if vesting_style == 'Custom' or show_full_alloc_table else init_vesting_dict['staking_vesting']][0]
    staking_vesting_cliff = [staking_vesting_cliff if vesting_style == 'Custom' or show_full_alloc_table else cliff_dict['staking_vesting']][0]
    staking_vesting_duration = [staking_vesting_duration if vesting_style == 'Custom' or show_full_alloc_table else duration_dict['staking_vesting']][0]
    vesting_style = vesting_style if not show_full_alloc_table else 'Custom'

    return_dict = {
        "seed_raised" : seed_raised,
        "presale_1_raised" : presale_1_raised,
        "presale_2_raised" : presale_2_raised,
        "public_sale_raised" : public_sale_raised,
        "team_allocation" : team_allocation,
        "ov_advisor_allocation" : ov_advisor_allocation,
        "strategic_partners_allocation" : strategic_partners_allocation,
        "reserve_allocation" : reserve_allocation,
        "community_allocation" : community_allocation,
        "foundation_allocation" : foundation_allocation,
        "incentivisation_allocation" : incentivisation_allocation,
        "staking_vesting_allocation" : staking_vesting_allocation,
        "airdrop_allocation" : airdrop_allocation,
        "airdrop_amount1" : airdrop_amount1,
        "airdrop_amount2" : airdrop_amount2,
        "airdrop_amount3" : airdrop_amount3,
        "airdrop_date1" : airdrop_date1,
        "airdrop_date2" : airdrop_date2,
        "airdrop_date3" : airdrop_date3,
        "lp_allocation" : lp_allocation,
        "angel_initial_vesting" : angel_initial_vesting,
        "angel_cliff" : angel_cliff,
        "angel_duration" : angel_duration,
        "seed_initial_vesting" : seed_initial_vesting,
        "seed_cliff" : seed_cliff,
        "seed_duration" : seed_duration,
        "presale_1_initial_vesting" : presale_1_initial_vesting,
        "presale_1_cliff" : presale_1_cliff,
        "presale_1_duration" : presale_1_duration,
        "presale_2_initial_vesting" : presale_2_initial_vesting,
        "presale_2_cliff" : presale_2_cliff,
        "presale_2_duration" : presale_2_duration,
        "public_sale_initial_vesting" : public_sale_initial_vesting,
        "public_sale_cliff" : public_sale_cliff,
        "public_sale_duration" : public_sale_duration,
        "team_initial_vesting" : team_initial_vesting,
        "team_cliff" : team_cliff,
        "team_duration" : team_duration,
        "advisor_initial_vesting" : advisor_initial_vesting,
        "advisor_cliff" : advisor_cliff,
        "advisor_duration" : advisor_duration,
        "strategic_partners_initial_vesting" : strategic_partners_initial_vesting,
        "strategic_partners_cliff" : strategic_partners_cliff,
        "strategic_partners_duration" : strategic_partners_duration,
        "reserve_initial_vesting" : reserve_initial_vesting,
        "reserve_cliff" : reserve_cliff,
        "reserve_duration" : reserve_duration,
        "community_initial_vesting" : community_initial_vesting,
        "community_cliff" : community_cliff,
        "community_duration" : community_duration,
        "foundation_initial_vesting" : foundation_initial_vesting,
        "foundation_cliff" : foundation_cliff,
        "foundation_duration" : foundation_duration,
        "incentivisation_initial_vesting" : incentivisation_initial_vesting,
        "incentivisation_cliff" : incentivisation_cliff,
        "incentivisation_duration" : incentivisation_duration,
        "staking_vesting_initial_vesting" : staking_vesting_initial_vesting,
        "staking_vesting_cliff" : staking_vesting_cliff,
        "staking_vesting_duration" : staking_vesting_duration,
        "dex_capital" : dex_capital,
        "vesting_dict" : vesting_dict,
        "airdrop_dict" : airdrop_dict,
        "incentivisation_toggle" : incentivisation_toggle,
        "staking_vesting_toggle" : staking_vesting_toggle,
        "airdrop_toggle" : airdrop_toggle,
        "show_full_alloc_table" : show_full_alloc_table,
        "vesting_style" : vesting_style,
    }

    return return_dict

