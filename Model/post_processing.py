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
        
        # Agent attributes
        key_values = agent_ds.apply(lambda s: s.get(key))
        for key2 in key_values[key_values.keys()[0]]:
            data[agent_ds[agent_ds.keys()[0]][key]['name']+'_'+key2] = agent_ds.map(lambda s: [agent[key2] for agent in s.values() if agent['name'] == agent_ds[agent_ds.keys()[0]][key]['name']][0])

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
    
    ## AGGREGATED METRICS ##
    data["From_Holding_Supply_Selling"] = data["airdrop_receivers_selling_tokens"].add(data["incentivisation_receivers_selling_tokens"])
    data["From_Holding_Supply_Utility"] = data["airdrop_receivers_utility_tokens"].add(data["incentivisation_receivers_utility_tokens"])
    data["From_Holding_Supply_Holding"] = data["airdrop_receivers_holding_tokens"].add(data["incentivisation_receivers_holding_tokens"])
    
    return data