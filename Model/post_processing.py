import pandas as pd
import warnings

warnings.filterwarnings("ignore")

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
    timesteps = df.timestep
    date = df.date

    agent_ds = df.agents
    liquidity_pool_ds = df.liquidity_pool
    token_economy_ds = df.token_economy
    user_adoption_ds = df.user_adoption
    business_assumptions_ds = df.business_assumptions
    utilities_ds = df.utilities
    
    # Create an analysis dataset
    data = (pd.DataFrame({'timestep': timesteps,
                          'date': date,
                          'run': df.run,
                          'agents': agent_ds,
                          'liquidity_pool': liquidity_pool_ds,
                          'token_economy': token_economy_ds,
                          'user_adoption':user_adoption_ds
                          })
           )

    ## Token Economy ##
    for key in token_economy_ds[token_economy_ds.keys()[0]]:
        key_values = token_economy_ds.apply(lambda s: s.get(key))
        data[key] = key_values     

    ## Liquidity Pool ##
    for key in liquidity_pool_ds[liquidity_pool_ds.keys()[0]]:
        key_values = liquidity_pool_ds.apply(lambda s: s.get(key))
        data[key] = key_values  
    
    ## AGENTS ##
    for key in agent_ds[agent_ds.keys()[0]]:
        # Agent quantity
        data[agent_ds[agent_ds.keys()[0]][key]['name']+'_agents'] = agent_ds.map(lambda s: sum([1 for agent in s.values() if agent['name'] == agent_ds[agent_ds.keys()[0]][key]['name']]))
        
        # Agent tokens quantity
        data[agent_ds[agent_ds.keys()[0]][key]['name']+'_tokens'] = agent_ds.map(lambda s: sum([agent['tokens'] for agent in s.values() if agent['name'] == agent_ds[agent_ds.keys()[0]][key]['name']]))

        # Agents usd_funds quantitiy
        data[agent_ds[agent_ds.keys()[0]][key]['name']+'_usd_funds'] = agent_ds.map(lambda s: sum([agent['usd_funds'] for agent in s.values() if agent['name'] == agent_ds[agent_ds.keys()[0]][key]['name']]))

        # Agents tokens apr locked quantity
        data[agent_ds[agent_ds.keys()[0]][key]['name']+'_tokens_apr_locked'] = agent_ds.map(lambda s: sum([agent['tokens_apr_locked'] for agent in s.values() if agent['name'] == agent_ds[agent_ds.keys()[0]][key]['name']]))

        # Agents tokens buyback locked quantity
        data[agent_ds[agent_ds.keys()[0]][key]['name']+'_tokens_buyback_locked'] = agent_ds.map(lambda s: sum([agent['tokens_buyback_locked'] for agent in s.values() if agent['name'] == agent_ds[agent_ds.keys()[0]][key]['name']]))

        # Agents tokens vested quantity
        data[agent_ds[agent_ds.keys()[0]][key]['name']+'_tokens_vested'] = agent_ds.map(lambda s: sum([agent['tokens_vested'] for agent in s.values() if agent['name'] == agent_ds[agent_ds.keys()[0]][key]['name']]))

        # Agents tokens vested cumulative quantity
        data[agent_ds[agent_ds.keys()[0]][key]['name']+'_tokens_vested_cum'] = agent_ds.map(lambda s: sum([agent['tokens_vested_cum'] for agent in s.values() if agent['name'] == agent_ds[agent_ds.keys()[0]][key]['name']]))

        # Agents meta bucket selling tokens quantity
        data[agent_ds[agent_ds.keys()[0]][key]['name']+'_selling_tokens'] = agent_ds.map(lambda s: sum([agent['selling_tokens'] for agent in s.values() if agent['name'] == agent_ds[agent_ds.keys()[0]][key]['name']]))

        # Agents meta bucket utility tokens quantity
        data[agent_ds[agent_ds.keys()[0]][key]['name']+'_utility_tokens'] = agent_ds.map(lambda s: sum([agent['utility_tokens'] for agent in s.values() if agent['name'] == agent_ds[agent_ds.keys()[0]][key]['name']]))

        # Agents meta bucket holding tokens quantity
        data[agent_ds[agent_ds.keys()[0]][key]['name']+'_holding_tokens'] = agent_ds.map(lambda s: sum([agent['holding_tokens'] for agent in s.values() if agent['name'] == agent_ds[agent_ds.keys()[0]][key]['name']]))

    
    ## UTILITIES ##
    for key in utilities_ds[utilities_ds.keys()[0]]:
        key_values = utilities_ds.apply(lambda s: s.get(key))
        data[key] = key_values  

    ## USER ADOPTION ##
    for key in user_adoption_ds[user_adoption_ds.keys()[0]]:
        key_values = user_adoption_ds.apply(lambda s: s.get(key))
        data[key] = key_values

    ## BUSINESS ASSUMPTIONS ##
    for key in business_assumptions_ds[business_assumptions_ds.keys()[0]]:
        key_values = business_assumptions_ds.apply(lambda s: s.get(key))
        data[key] = key_values 
    
    return data