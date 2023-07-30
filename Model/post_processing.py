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
    data['circulating_supply'] = token_economy_ds.map(lambda s: s["circulating_supply"])
    data['selling_perc'] = token_economy_ds.map(lambda s: s["selling_perc"])
    data['utility_perc'] = token_economy_ds.map(lambda s: s["utility_perc"])
    data['holding_perc'] = token_economy_ds.map(lambda s: s["holding_perc"])
    data['minted_tokens'] = token_economy_ds.map(lambda s: s["minted_tokens"])
    data['incentivised_tokens'] = token_economy_ds.map(lambda s: s["incentivised_tokens"])
    data['incentivised_tokens_usd'] = token_economy_ds.map(lambda s: s["incentivised_tokens_usd"])
    data['incentivised_tokens_cum'] = token_economy_ds.map(lambda s: s["incentivised_tokens_cum"])
    data['airdrop_tokens'] = token_economy_ds.map(lambda s: s["airdrop_tokens"])
    data['airdrop_tokens_usd'] = token_economy_ds.map(lambda s: s["airdrop_tokens_usd"])
    data['airdrop_tokens_cum'] = token_economy_ds.map(lambda s: s["airdrop_tokens_cum"])
    data['selling_allocation'] = token_economy_ds.map(lambda s: s["selling_allocation"])
    data['utility_allocation'] = token_economy_ds.map(lambda s: s["utility_allocation"])
    data['holding_allocation'] = token_economy_ds.map(lambda s: s["holding_allocation"])
        #apr
    data['apr_tokens'] = token_economy_ds.map(lambda s: s["apr_tokens"])
    data['apr_tokens_usd'] = token_economy_ds.map(lambda s: s["apr_tokens_usd"])
    
    
    ## Liquidity Pool ##
    data['tokens'] = liquidity_pool_ds.map(lambda s: s["tokens"])
    data['usdc'] = liquidity_pool_ds.map(lambda s: s["usdc"])
    data['constant_product'] = liquidity_pool_ds.map(lambda s: s["constant_product"])
    data['token_price'] = liquidity_pool_ds.map(lambda s: s["token_price"])

    
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


    ## USER ADOPTION ##
    for key in user_adoption_ds[user_adoption_ds.keys()[0]]:
        key_values = user_adoption_ds.apply(lambda s: s.get(key))
        data[key] = key_values


    cash_balance = business_assumptions_ds.apply(lambda s: s.get('cash_balance'))
    data['cash_balance'] = cash_balance
    
    return data