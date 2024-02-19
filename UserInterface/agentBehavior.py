import streamlit as st

def agentBehaviorInput(sys_param, adoption_style, adoption_dict):
    """
    This function creates the agent behavior section of the UI.
    """
    with st.expander("**Agent Behavior**"):
        st.markdown("### Agent Behavior")
        agent_behavior_choices = ['Static', 'Simple']
        agent_behavior = st.radio('Agent Meta Bucket Behavior',tuple(agent_behavior_choices), index=agent_behavior_choices.index(sys_param['agent_behavior'][0].capitalize()), help="Pick the agent behavior model. **Static**:  Every agent will use tokens for selling, utility, and holding always at the same rate throughout the whole simulation. **Random**: Token holders and their adoption react to staking APRs; Product users get attracted by incentives; A little random noise gets added to the agents decisions.").lower()
        col73, col74, col75 = st.columns(3)
        if agent_behavior == 'static':
            st.write("**Meta Bucket Allocations**")
            col7a, col7b, col7c, col7d = st.columns(4)
            with col7a:
                avg_token_selling_allocation = st.number_input('Avg. Token Selling Alloc. / %', label_visibility="visible", min_value=0.0, max_value=100.0, value=[float(sys_param['avg_token_selling_allocation'][0])*100 if adoption_style == 'Custom' else adoption_dict[adoption_style]['avg_token_selling_allocation']][0], disabled=False, key="avg_token_selling_allocation", help="The average monthly token allocation for selling purposes from all holding supply.")
            with col7b:
                avg_token_holding_allocation = st.number_input('Avg. Token Holding Alloc. / %', label_visibility="visible", min_value=0.0, max_value=100.0, value=[float(sys_param['avg_token_holding_allocation'][0])*100 if adoption_style == 'Custom' else adoption_dict[adoption_style]['avg_token_holding_allocation']][0], disabled=False, key="avg_token_holding_allocation", help="The average monthly token allocation for holding purposes from all holding supply.")
            with col7c:
                avg_token_utility_allocation = st.number_input('Avg. Token Utility Alloc. / %', label_visibility="visible", min_value=0.0, max_value=100.0, value=[float(sys_param['avg_token_utility_allocation'][0])*100 if adoption_style == 'Custom' else adoption_dict[adoption_style]['avg_token_utility_allocation']][0], disabled=False, key="avg_token_utility_allocation", help="The average monthly token allocation for utility purposes from all holding supply.")
            with col7d:
                avg_token_utility_removal = st.number_input('Avg. Token Utility Removal / %', label_visibility="visible", min_value=0.0, max_value=100.0, value=[float(sys_param['avg_token_utility_removal'][0])*100 if adoption_style == 'Custom' else adoption_dict[adoption_style]['avg_token_utility_removal']][0], disabled=False, key="avg_token_utility_removal", help="The average monthly token removal from staking and liquidity mining utilities.")
            random_seed = 1111.11
        elif agent_behavior == 'simple':
            with col73:
                random_seed = st.number_input("Random Seed", label_visibility="visible", min_value=float(0.0), value=float(sys_param['random_seed'][0]) if 'random_seed' in sys_param and sys_param['random_seed'][0] != None else 1111.11, disabled=False, key="random_seed", help="The random seed for the random agent behavior. This will be used to reproduce the same random agent behavior.")
            avg_token_utility_removal = float(sys_param['avg_token_utility_removal'][0])*100
        avg_token_utility_allocation = avg_token_utility_allocation if agent_behavior =='static' else 60.0
        avg_token_selling_allocation = avg_token_selling_allocation if agent_behavior =='static' else 30.0
        avg_token_holding_allocation = avg_token_holding_allocation if agent_behavior =='static' else 10.0
        meta_bucket_alloc_sum = avg_token_utility_allocation + avg_token_selling_allocation + avg_token_holding_allocation
        if meta_bucket_alloc_sum != 100 and agent_behavior == 'static':
            st.error(f"The sum of the average token allocations for utility, selling and holding ({avg_token_utility_allocation + avg_token_selling_allocation + avg_token_holding_allocation}%) is not equal to 100%. Please adjust the values!", icon="⚠️")
    
    # Dynamic Agent Selling Behavior Parameters. These are hardcoded for now to avoid too much complexity for the user, but might be implemented here in the future.
    # The agent selling probability S depends on the change in token holders Tc as follows:
    # S = 1 / (S_B**(Tc * S_e)) * S_0
    S_B = 10
    S_e = 5
    S_0 = 0.03

    ab_return_dict = {
        "agent_behavior" : agent_behavior,
        "avg_token_utility_allocation" : avg_token_utility_allocation,
        "avg_token_selling_allocation" : avg_token_selling_allocation,
        "avg_token_holding_allocation" : avg_token_holding_allocation,
        "avg_token_utility_removal" : avg_token_utility_removal,
        "random_seed" : random_seed,
        "meta_bucket_alloc_sum" : meta_bucket_alloc_sum,
        "S_B" : S_B,
        "S_e" : S_e,
        "S_0" : S_0
    }

    return ab_return_dict
