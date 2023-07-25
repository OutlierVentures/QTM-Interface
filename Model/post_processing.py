import pandas as pd

def postprocessing(df):
    '''
    Definition:
    Refine and extract metrics from the simulation
    
    Parameters:
    df: simulation dataframe
    '''
    # subset to last substep
    df = df[df['substep'] == df.substep.max()] 

    # Get the ABM results
    agent_ds = df.agents
    liquidity_pool_ds = df.liquidity_pool
    token_economy_ds = df.token_economy
    user_adoption_ds = df.user_adoption
    business_assumptions_ds = df.business_assumptions


    """ token_price_ds = df.token_price
    dex_lp_tokens_ds = df.dex_lp_tokens
    dex_lp_usdc_ds = df.dex_lp_usdc
    fdv_mc_ds = df.fdv_mc
    implied_fdv_mc_ds = df.implied_fdv_mc
    mc_ds = df.mc
    circ_supply_ds = df.circ_supply
    tokens_locked_ds = df.tokens_locked
    vesting_rate_ds = df.vesting_rate """

    timesteps = df.timestep
    date = df.date
    
    # Create an analysis dataset
    data = (pd.DataFrame({'timestep': timesteps,
                          'date': date,
                          'run': df.run,
                          """ 'token_price': token_price_ds,
                          'dex_lp_tokens': dex_lp_tokens_ds,
                          'dex_lp_usdc': dex_lp_usdc_ds,
                          'fdv_mc': fdv_mc_ds,
                          'implied_fdv_mc': implied_fdv_mc_ds,
                          'mc': mc_ds,
                          'circ_supply': circ_supply_ds,
                          'tokens_locked': tokens_locked_ds,
                          'vesting_rate': vesting_rate_ds, """
                          'agents': agent_ds,
                          'liquidity_pool': liquidity_pool_ds,
                          'token_economy': token_economy_ds,
                          'user_adoption_ds':user_adoption_ds
                          })
           )

    ## Agent quantity
    for key in agent_ds[agent_ds.keys()[0]]:
        data[agent_ds[agent_ds.keys()[0]][key]['name']+'_agents'] = agent_ds.map(lambda s: sum([1 for agent in s.values() if agent['name'] == agent_ds[agent_ds.keys()[0]][key]['name']]))

    ## agents tokens quantitiy
    for key in agent_ds[agent_ds.keys()[0]]:
        data[agent_ds[agent_ds.keys()[0]][key]['name']+'_tokens'] = agent_ds.map(lambda s: sum([agent['tokens'] for agent in s.values() if agent['name'] == agent_ds[agent_ds.keys()[0]][key]['name']]))

    ## agents usd_funds quantitiy
    for key in agent_ds[agent_ds.keys()[0]]:
        data[agent_ds[agent_ds.keys()[0]][key]['name']+'_usd_funds'] = agent_ds.map(lambda s: sum([agent['usd_funds'] for agent in s.values() if agent['name'] == agent_ds[agent_ds.keys()[0]][key]['name']]))

    ## agents tokens locked quantity
    for key in agent_ds[agent_ds.keys()[0]]:
        data[agent_ds[agent_ds.keys()[0]][key]['name']+'_tokens_locked'] = agent_ds.map(lambda s: sum([agent['tokens_locked'] for agent in s.values() if agent['name'] == agent_ds[agent_ds.keys()[0]][key]['name']]))

    ## agents tokens vested quantity
    for key in agent_ds[agent_ds.keys()[0]]:
            data[agent_ds[agent_ds.keys()[0]][key]['name']+'_tokens_vested'] = agent_ds.map(lambda s: sum([agent['tokens_vested'] for agent in s.values() if agent['name'] == agent_ds[agent_ds.keys()[0]][key]['name']]))


    ## user adoption
    for key in user_adoption_ds[user_adoption_ds.keys()[0]]:
        key_values = user_adoption_ds.apply(lambda s: s.get(key))
        data[key] = key_values


    cash_balance = business_assumptions_ds.apply(lambda s: s.get('cash_balance'))
    data['cash_balance'] = cash_balance
    
    return data