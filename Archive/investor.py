#!/usr/bin/env python
# coding: utf-8

# In[2]:



class Investor:
    def __init__(self, name, vesting_percent, cliff_months, issuing_months,allocated_tokens=0):
        self._name = name
        self._vesting_percent:float = vesting_percent
        self._cliff_months:int = cliff_months
        self._issuing_months:int = issuing_months
        self._allocated_tokens:int = allocated_tokens
        
    def get_name(self):
        return self._name
    
    def set_name(self, name):
        self._name = name
        
    def get_vesting_percent(self):
        return self._vesting_percent
    
    def set_vesting_percent(self, vesting_percent):
        self._vesting_percent = vesting_percent
        
    def get_cliff_months(self):
        return self._cliff_months
    
    def set_cliff_months(self, cliff_months):
        self._cliff_months = cliff_months
        
    def get_issuing_months(self):
        return self._issuing_months
    
    def set_issuing_months(self, issuing_months):
        self._issuing_months = issuing_months
        
    def get_allocated_tokens(self):
        return self._allocated_tokens
    
    def set_allocated_tokens(self, allocated_tokens):
        self._allocated_tokens = allocated_tokens
        
    def __getstate__(self):
        return (self._name, self._vesting_percent, self._cliff_months, self._issuing_months, self._allocated_tokens)

    def __setstate__(self, state):
        self._name, self._vesting_percent, self._cliff_months, self._issuing_months, self._allocated_tokens = state


# In[ ]:





# In[ ]:




