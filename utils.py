#!/usr/bin/env python
# coding: utf-8

# In[2]:



# Initialization
def new_agent(agent_type: str, location: Tuple[int, int],
              food: int=10, age: int=0) -> dict:
    agent = {'type': agent_type,
             'location': location,
             'food': food,
             'age':age}
    return agent


#Generate them
def generate_agents(N: int,M: int,initial_sites: int,
                    n_predators: int,
                    n_prey: int) -> Dict[str, dict]:
    
    available_locations = [(n, m) for n in range(N) for m in range(M)]
    initial_agents = {}
    type_queue = ['prey'] * n_prey
    type_queue += ['predator'] * n_predators
    random.shuffle(type_queue)
    for agent_type in type_queue:
        location = random.choice(available_locations)
        available_locations.remove(location)
        created_agent = new_agent(agent_type, location)
        initial_agents[uuid.uuid4()] = created_agent
    return 






# In[ ]:





# In[ ]:




