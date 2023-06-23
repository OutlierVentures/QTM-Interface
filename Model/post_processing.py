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
    
    # Get metrics

    ## Agent quantity
    team_count = agent_ds.map(lambda s: sum([1 for agent in s.values() if agent['type'] == 'team']))
    foundation_count = agent_ds.map(lambda s: sum([1 for agent in s.values() if agent['type'] == 'foundation']))


    ## agents tokens quantitiy
    team_tokens = agent_ds.map(lambda s: sum([agent['tokens'] 
                                               for agent 
                                               in s.values() if agent['type'] == 'team']))
    foundation_tokens = agent_ds.map(lambda s: sum([agent['tokens'] 
                                               for agent 
                                               in s.values() if agent['type'] == 'foundation']))
    
    ## agents usd_funds quantitiy
    team_usd_funds = agent_ds.map(lambda s: sum([agent['usd_funds'] 
                                               for agent 
                                               in s.values() if agent['type'] == 'team']))
    foundation_usd_funds = agent_ds.map(lambda s: sum([agent['usd_funds'] 
                                               for agent 
                                               in s.values() if agent['type'] == 'foundation']))

    ## agents tokens locked quantity
    team_tokens_locked = agent_ds.map(lambda s: sum([agent['tokens_locked'] 
                                               for agent 
                                               in s.values() if agent['type'] == 'team']))
    foundation_tokens_locked = agent_ds.map(lambda s: sum([agent['tokens_locked'] 
                                               for agent 
                                               in s.values() if agent['type'] == 'foundation']))

    ## agents tokens vested quantity
    team_tokens_vested = agent_ds.map(lambda s: sum([agent['tokens_vested'] 
                                               for agent 
                                               in s.values() if agent['type'] == 'team']))
    foundation_tokens_vested = agent_ds.map(lambda s: sum([agent['tokens_vested'] 
                                               for agent 
                                               in s.values() if agent['type'] == 'foundation']))

    # Create an analysis dataset
    data = (pd.DataFrame({'timestep': timesteps,
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
                          'team_agents': team_count,
                          'foundation_agents': foundation_count,
                          'team_tokens': team_tokens,
                          'foundation_tokens': foundation_tokens,
                          'team_usd_funds': team_usd_funds,
                          'foundation_usd_funds': foundation_usd_funds,
                          'team_tokens_locked': team_tokens_locked,
                          'foundation_tokens_locked': foundation_tokens_locked,
                          'team_tokens_vested': team_tokens_vested,
                          'foundation_tokens_vested': foundation_tokens_vested,
                          'agents': agent_ds,
                          'liquidity_pool': liquidity_pool_ds,
                          'token_economy': token_economy_ds})
           )
    
    return data