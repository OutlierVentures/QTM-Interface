import streamlit as st
from UserInterface.plots import *
from UserInterface.helpers import to_excel, ui_base, returnToStart, header

# Get the current directory
current_dir = os.path.dirname(os.path.abspath(__file__))
# Go up one folder
parent_dir = os.path.abspath(os.path.join(os.path.abspath(current_dir), os.pardir))
# Append the parent directory to sys.path
sys.path.append(parent_dir)

if 'authentication_status' in st.session_state:
    if st.session_state["authentication_status"]:
        header(parent_dir)
        ui_base(parent_dir)

        st.sidebar.markdown("## Data 💾")

        # main page
        st.markdown("## Data 💾")
        st.markdown("### Full Timeseries Data")
        if st.session_state["username"] == 'admin':
            # download the full 'simulationData.db' database
            st.markdown('---')
            st.markdown('Download the full database as .db file.')
            st.download_button(label='📥 Download Database as .db',
                                data=open('simulationData.db', 'rb').read(),
                                file_name='simulationData.db')
        
        if 'param_id' in st.session_state:
            if st.session_state['param_id'] != "":
                # get simulation result data data frame
                df = get_simulation_data('simulationData.db', 'simulation_data_'+str(st.session_state['param_id']))
                # get simulation parameter data frame
                df_params = pd.read_sql(f'SELECT * FROM sys_param', sqlite3.connect('simulationData.db'))
                df_params = df_params[df_params['id'] == st.session_state['param_id']]
                st.markdown('---')
                st.write('Simulation Parameter Set')
                st.dataframe(df_params)
                df_params_xlsx = to_excel(df_params)
                st.download_button(label='📥 Download Parameter Set as .xlsx',
                                        data=df_params_xlsx,
                                        file_name= f"QTM_Parameters_{st.session_state['project_name']}.xlsx")
                st.markdown('---')
                st.write('Simulation Results')
                st.dataframe(df)
                df_xlsx = to_excel(df)
                st.download_button(label='📥 Download Data as .xlsx',
                                        data=df_xlsx ,
                                        file_name= f"QTM_Results_{st.session_state['project_name']}.xlsx")

        
                # create user defined plots
                st.markdown('---')
                st.markdown("### Create Custom Plots")
                plot_user_custom(st.session_state['param_id'], st.session_state['max_months'] if 'max_months' in st.session_state else int(max(df['timestep'].astype(float))))
    else:
        returnToStart()
else:
    returnToStart()
