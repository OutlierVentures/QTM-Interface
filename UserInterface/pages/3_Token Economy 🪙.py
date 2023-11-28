import streamlit as st
from plots import *
from PIL import Image

# Get the current directory
current_dir = os.path.dirname(os.path.abspath(__file__))
# Go up one folder
parent_dir = os.path.abspath(os.path.join(os.path.abspath(os.path.join(current_dir, os.pardir)), os.pardir))
# Append the parent directory to sys.path
sys.path.append(parent_dir)

image = Image.open(parent_dir+'/images/ov_logo.jpg')
st.image(image, width=125)
st.title('Quantitative Token Model')

# side bar
if 'param_id' in st.session_state:
    param_id_init = st.session_state['param_id']
else:
    param_id_init = ""
# get all existing project names
try:
    db_sorted = get_simulation_data('simulationData.db', 'sys_param').sort_values('project_name', ascending=True)
    project_names = db_sorted['project_name']
    project_names = project_names.to_list()
    project_names.append('')
except:
    db_sorted = pd.DataFrame()
    project_names = ['']
if 'project_name' not in st.session_state:
    st.session_state['project_name'] = ''

if 'project_name' in st.session_state and 'param_id' in st.session_state and len(db_sorted) > 0:
    st.session_state['project_name'] = st.sidebar.selectbox('Project Name', tuple(project_names), index=[db_sorted['id'].to_list().index(st.session_state['param_id']) if st.session_state['param_id'] in db_sorted['id'].to_list() else len(project_names)-1][0])
    st.session_state['param_id'] = st.sidebar.text_input('Parameter ID',[db_sorted[db_sorted['project_name']==st.session_state['project_name']]['id'].iloc[0] if st.session_state['project_name'] in db_sorted['project_name'].to_list() else ""][0])
else:
    st.session_state['project_name'] = st.sidebar.selectbox('Project Name', tuple(project_names), index=len(project_names)-1)
    st.session_state['param_id'] = st.sidebar.text_input('Parameter ID', "")

try:
    if st.session_state['param_id'] not in get_simulation_data('simulationData.db', 'sys_param')['id'].to_list():
        st.sidebar.markdown(f"Parameter ID: {st.session_state['param_id']} does not exist. Please enter a valid parameter ID or run the simulation with your parameter set to get a parameter ID.")
    else:
        st.sidebar.markdown(f"This is a valid parameter ID ✅")
except:
    pass
st.sidebar.markdown("## Token Economy 🪙")

# main page
st.markdown("## Token Economy 🪙")
if 'param_id' in st.session_state:
    if st.session_state['param_id'] != "":
        sys_param_df = get_simulation_data('simulationData.db', 'sys_param')
        sys_param = sys_param_df[sys_param_df['id'] == st.session_state['param_id']]
        if 'max_months' in st.session_state:
            if st.session_state['max_months']<sys_param['simulation_duration'].iloc[0]:
                st.error(f"The simulation stopped after {st.session_state['max_months']} months, because the business ran out of funds.", icon="⚠️")
            plot_token_economy(st.session_state['param_id'], st.session_state['max_months'])
        else:
            plot_token_economy(st.session_state['param_id'], sys_param['simulation_duration'].iloc[0])


df = get_simulation_data('simulationData.db', 'simulation_data_'+str(st.session_state['param_id']))
st.dataframe(df)