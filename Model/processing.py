import matplotlib.pyplot as plt
import pandas as pd




def plot_stacked_area_graph(df, total_token_supply):
    # pivot the dataframe to create a multi-level index with Investor_Name and timestep
    df_pivot = df.pivot(index='timestep', columns='Investor_Name', values='current_allocation')
    
    # multiply the values by the total token supply to convert from percentage to token amount
    df_pivot = df_pivot * total_token_supply
    
    # plot the stacked area graph
    df_pivot.plot.area(stacked=True)
    
    # set the title and labels for the plot
    plt.title('Investor Allocation Over Time')
    plt.xlabel('Time Step')
    plt.ylabel('Token Allocation')
    
    # show the plot
    plt.show()






def extract_investors(df):
    investors_df = pd.DataFrame(columns=['Investor_Name', 'current_allocation', 'timestep'])
    for index, row in df.iterrows():
        timestep = row['timestep']
        investors_dict = row['investors']
        for investor_name, investor_data in investors_dict.items():
            allocation = investor_data['current_allocation']
            investors_df = pd.concat([investors_df,
                                      pd.DataFrame({'Investor_Name': [investor_name],
                                                    'current_allocation': [allocation],
                                                    'timestep': [timestep]})])
    investors_df.reset_index(drop=True, inplace=True)
    return investors_df