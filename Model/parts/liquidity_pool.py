from .utils import *

# POLICY FUNCTIONS
def initialize_liquidity_pool(params, substep, state_history, prev_state, **kwargs):
    """
    Function to initialize the liquidity pool in the first timestep
    """

    current_month = prev_state['timestep']
    liquidity_pool = prev_state['liquidity_pool']
    agents = prev_state['agents']

    if current_month == 0:
        required_usdc = params['initial_required_usdc']
        required_tokens = params['initial_lp_token_allocation']
        constant_product = required_usdc * required_tokens
        token_price = required_usdc / required_tokens

        # initialize the liquidity pool from the system parameters
        liquidity_pool = {
        'tokens' : required_tokens,
        'usdc' : required_usdc,
        'constant_product' : constant_product,
        'token_price' : token_price
        }

        # subtract the required funds from the funding bucket.
        business_fund_holder = params['business_fund_holder']

        sum_of_raised_capital = calculate_raised_capital(params)

        if required_usdc > sum_of_raised_capital:
            raise ValueError('The required funds to seed the DEX liquidity are '+str(required_usdc)+' and higher than the sum of raised capital '+str(sum_of_raised_capital)+'!')
        else:
            # subtract the required funds from the funding bucket.
            found_stakeholder = False
            for stakeholder in agents:
                if agents[stakeholder]['type'] == business_fund_holder:
                    
                    # add all raised funds to the business fund holder
                    agents[stakeholder]['usd_funds'] = sum_of_raised_capital

                    # subtract the required funds to seed the liquidity pool from the business fund holder
                    agents[stakeholder]['usd_funds'] -= required_usdc
                    if agents[stakeholder]['usd_funds'] < 0:
                        raise ValueError("The stakeholder "+agents[stakeholder]['type']+" has only $"+str(agents[stakeholder]['usd_funds']+required_usdc)+" funds, but $"+str(required_usdc)+" are required for seeding the DEX liquidity pool!")
                    found_stakeholder = True
            
            if not found_stakeholder:
                raise ValueError("The DEX liquidity couldn't be seeded as there is no stakeholder with name: "+business_fund_holder)
        
        return {'liquidity_pool': liquidity_pool, 'agents': agents}
    else:
        return {'liquidity_pool': prev_state['liquidity_pool'], 'agents': agents}


# STATE UPDATE FUNCTIONS
def update_agents_after_lp_seeding(params, substep, state_history, prev_state, policy_input, **kwargs):
    """
    Function to update the agents based on the changes in business funds to seed the liquidity pool.
    """
    updated_agents = policy_input['agents']

    return ('agents', updated_agents)

def update_lp_after_lp_seeding(params, substep, state_history, prev_state, policy_input, **kwargs):
    """
    Function to update the agents based on the changes in business funds to seed the liquidity pool.
    """
    updated_liquidity_pool = policy_input['liquidity_pool']

    return ('liquidity_pool', updated_liquidity_pool)