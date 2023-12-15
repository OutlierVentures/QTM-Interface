import pandas as pd
import warnings

warnings.filterwarnings("ignore")

def postprocessing(df0, includeInitialization, substep, category):
    '''
    Definition:
    Refine and extract metrics from the simulation
    
    Parameters:
    df: simulation dataframe
    substep: the substep you would like to extract the metrics from
    category: the category you would like to extract the metrics from.
    Options: 'all', 'liquidity_pool', 'agents', 'token_economy', 'user_adoption', 'business_assumptions', 'utilities'
    '''
    print("Postprocessing for substep: ", substep, " and category: ", category, "started..")
    # subset to last substep
    df = df0[df0['substep'] == substep]
    
    if includeInitialization:
        print("Including initialization data..")
        df2 = df0[(df0['substep'] == int(df0['substep'].min())+1)]
        df2 = df2[df2['timestep'] == int(df2['timestep'].min())]
        df2['timestep'][1] = 0

        df = pd.concat([df2, df], ignore_index=True)

    # Get the ABM results
    timesteps = df.timestep
    date = df.date
    
    # Create an analysis dataset
    data = (pd.DataFrame({'timestep': timesteps,
                          'date': date,
                          'run': df.run
                          })
           )

    ## Token Economy ##
    if category == 'token_economy' or category == 'all':
        token_economy_ds = df.token_economy
        for key in token_economy_ds[token_economy_ds.keys()[0]]:
            key_values = token_economy_ds.apply(lambda s: s.get(key))
            data[key] = key_values     

    ## Liquidity Pool ##
    if category == 'liquidity_pool' or category == 'all':
        liquidity_pool_ds = df.liquidity_pool
        for key in liquidity_pool_ds[liquidity_pool_ds.keys()[0]]:
            key_values = liquidity_pool_ds.apply(lambda s: s.get(key))
            data[key] = key_values  
    
    ## AGENTS ##
    if category == 'agents' or category == 'all':
        agent_ds = df.agents
        for key in agent_ds[agent_ds.keys()[0]]:
            # Agent quantity
            data[agent_ds[agent_ds.keys()[0]][key]['a_name']+'_agents'] = agent_ds.map(lambda s: sum([1 for agent in s.values() if agent['a_name'] == agent_ds[agent_ds.keys()[0]][key]['a_name']]))
            
            # Agent attributes
            key_values = agent_ds.apply(lambda s: s.get(key))
            for key2 in key_values[key_values.keys()[0]]:
                data[agent_ds[agent_ds.keys()[0]][key]['a_name']+'_'+key2] = agent_ds.map(lambda s: [agent[key2] for agent in s.values() if agent['a_name'] == agent_ds[agent_ds.keys()[0]][key]['a_name']][0])

    ## UTILITIES ##
    if category == 'utilities' or category == 'all':
        utilities_ds = df.utilities
        for key in utilities_ds[utilities_ds.keys()[0]]:
            key_values = utilities_ds.apply(lambda s: s.get(key))
            data[key] = key_values  

    ## USER ADOPTION ##
    if category == 'user_adoption' or category == 'all':
        user_adoption_ds = df.user_adoption
        for key in user_adoption_ds[user_adoption_ds.keys()[0]]:
            key_values = user_adoption_ds.apply(lambda s: s.get(key))
            data[key] = key_values

    ## BUSINESS ASSUMPTIONS ##
    if category == 'business_assumptions' or category == 'all':
        business_assumptions_ds = df.business_assumptions
        for key in business_assumptions_ds[business_assumptions_ds.keys()[0]]:
            key_values = business_assumptions_ds.apply(lambda s: s.get(key))
            data[key] = key_values
    
    ## AGGREGATED METRICS ##




    print("Postprocessing for substep: ", substep, " finished!")
    
    return data