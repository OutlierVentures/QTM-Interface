import matplotlib.pyplot as plt
import pandas as pd




def plot_stacked_area_graph(df):
    # pivot the dataframe to create a multi-level index with Investor_Name and timestep

    df_pivot = df.pivot(index='timestep', columns='Investor_Name', values='current_allocation')
    
    # create a list of x values (time steps)
    x = df_pivot.index
    
    # create a list of y values (token allocations for each investor)
    y = df_pivot.to_numpy().T
    
    # plot the stacked area graph using stackplot
    plt.stackplot(x, y, labels=df_pivot.columns)
    
    # set the title and labels for the plot
    plt.title('Investor Allocation Over Time')
    plt.xlabel('Time Step')
    plt.ylabel('Token Allocation')
    
    # format the y-axis labels as integers
    plt.gca().yaxis.set_major_formatter('{:.0f}'.format)
    
    # show the legend and plot
    plt.legend()
    plt.show()



def effective_token_price_plot(df):
    data = []
    for investor, values in df['investors'][0].items():
        name = investor
        price = values['effective_token_price']
        data.append((name, price))
    data = pd.DataFrame(data, columns=['Name', 'effective_token_price'])

    df_filtered = data[data['effective_token_price'] != 0]
    df_filtered = df_filtered.sort_values(by='effective_token_price', ascending=False)
    df_filtered[['effective_token_price']].plot(kind='bar', rot=0)
    plt.title('Effective Token Price by Investor Type')
    plt.xlabel('Investor Type')
    plt.ylabel('Effective Token Price')
    plt.show()







def extract_allocation(df):
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
    investors_df['current_allocation'] = investors_df['current_allocation'].astype(float)
    investors_df['timestep'] = investors_df['timestep'].astype(int)


    return investors_df




def initial_allocation_pie(df):
    sum = 0
    percentages = []
    labels = []
    for i, investor in df['investors'][0].items():
        percentage = investor['percentage_allocation']
        labels.append(i+": "+str((round(percentage*100, 2)))+"%")
        percentages.append(percentage)
        sum += percentage

    labels.append("Blank")
    percentages.append(1-sum)

    plt.pie(percentages, labels=labels, normalize=True)
    plt.show()