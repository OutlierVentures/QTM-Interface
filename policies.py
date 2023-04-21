#!/usr/bin/env python
# coding: utf-8

# In[2]:


## Need to make a vest
def digest_and_olden(params, substep, state_history, prev_state):
    agents = prev_state['agents']
    delta_food = {agent: -1 for agent in agents.keys()}
    delta_age = {agent: +1 for agent in agents.keys()}
    return {'agent_delta_food': delta_food,
          'agent_delta_age': delta_age}




# In[ ]:





# In[ ]:




