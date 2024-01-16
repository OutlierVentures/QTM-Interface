import streamlit as st
from UserInterface.plots import *
from PIL import Image

# Get the current directory
current_dir = os.path.dirname(os.path.abspath(__file__))
# Go up one folder
parent_dir = os.path.abspath(os.path.join(os.path.abspath(current_dir), os.pardir))
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

st.sidebar.markdown("## Fundraising 💰")

# main page
st.markdown("## Fundraising 💰")

if 'param_id' in st.session_state:
    if st.session_state['param_id'] != "":
        plot_fundraising(st.session_state['param_id'])
