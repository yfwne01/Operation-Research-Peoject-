#!/usr/bin/env python
# coding: utf-8

# In[3]:


#Testing Kits Production for COVID-19 - Operations Research

#load packages 
import csv
import pandas as pd
import numpy as np
from pulp import *
import gurobipy as grb
from gurobipy import *
from gurobipy import Model, GRB, LinExpr, quicksum
import pandas as pd
from collections import OrderedDict


# In[5]:


#read the excel sheet
lp_data = pd.read_excel('Project_Data.xlsx', sheet_name='Table1', index_col=0)
# resetting index 
lp_data.reset_index(inplace = True) 
lp_data


# In[6]:


lp_supply = pd.read_excel('Project_Data.xlsx', sheet_name='Table2', index_col=0)
lp_supply


# In[7]:


#get the total cost for each path from a supply center to a state 

lp_data["Center1_shipping_cost"] = lp_data["Center 1"]* 0.001
lp_data["Center2_shipping_cost"] = lp_data["Center 2"] * 0.001
lp_data["Center3_shipping_cost"] = lp_data["Center 3"] * 0.001

lp_data["Center1_total_cost"] = lp_data["Center1_shipping_cost"] +1
lp_data["Center2_total_cost"] = lp_data["Center2_shipping_cost"] +1
lp_data["Center3_total_cost"] = lp_data["Center3_shipping_cost"] +1
lp_data.head(5)


# In[8]:


#Cost matrix
cost_matrix = lp_data[['Center1_total_cost','Center2_total_cost','Center3_total_cost']].to_numpy().transpose()
cost_matrix


# In[11]:


#Demand list (51)
demand_list = lp_data['1% of Population'].tolist() 
demand_list


# In[9]:


#Supply list (3)
supply_list = [1500000,1200000,1350000]
supply_list


# In[12]:


#Part 1
#LP
#build the model
m = Model()

#create variables
x = m.addVars(3,51,lb= 0.0, ub=GRB.INFINITY,vtype=GRB.CONTINUOUS,name="x")

#get the objective function

obj = quicksum(cost_matrix[i][j]*x[i,j] for i in range(3) for j in range(51))
        
m.setObjective(obj, GRB.MINIMIZE)

# Add constraints
#demand
for j in range(51):
    con1 = m.addConstr(sum(x[i,j] for i in range(3)) >= demand_list[j])

     #m.addConstr(x.sum('*',j) >= demand_list[j], name= "demand")

    
#supply
for i in range(3):
    con2 = m.addConstr(sum(x[i,j] for j in range(51)) <= supply_list[i])

     #m.addConstr(x.sum(i,'*') <= supply_list[i], name = "supply")
    
 # Optimize model
m.optimize()


# In[13]:


print('Obj: %g' % m.objVal)


# In[14]:


for v in m.getVars():
    print('%s %g' % (v.varName, v.x))


# In[87]:


#Sensitivity Report


# In[44]:


#get the objective coefficient sensitivity information
for v in m.getVars():
    print('Coeff Upper Bound', v.varName, v.SAObjUp)


# In[30]:


#get the objective coefficient sensitivity information
for v in m.getVars():
    print('Coeff Lower Bound', v.varName, v.SAObjLow)


# In[ ]:


#get the RHS sensitivity information


# In[48]:


#shadow price
for con in m.getConstrs():
    print('Shadow Price',con.Pi)


# In[49]:


#RHS bound
for con in m.getConstrs():
    print('Lower Range for constraint',con.SARHSLow)


# In[110]:


#RHS bound
for con in m.getConstrs():
    print('Upper Range for constraint',con.SARHSUp)


# In[70]:


#RHS bound
for con in m.getConstrs():
    print('Allowable RHS Increase',con.SARHSUp-con.RHS)


# In[69]:


#RHS bound
for con in m.getConstrs():
    print('Allowable RHS Decrease',con.RHS-con.SARHSLow)


# In[53]:


#RHS bound
for con in m.getConstrs():
    print('RHS Coeff',con.RHS)


# In[ ]:


#Part 2


# In[54]:


lp_updated = pd.read_excel('Project_Data.xlsx', sheet_name='Table3', index_col=0)
# resetting index 
lp_updated.reset_index(inplace = True) 
lp_updated


# In[55]:


#Demand list (51)
demand_list = lp_updated['Estimated Testing Kits'].tolist() 
demand_list


# In[58]:


#get the total cost for each path from a supply center to a state 

lp_data["Center1_shipping_cost"] = lp_data["Center 1"]* 0.002
lp_data["Center2_shipping_cost"] = lp_data["Center 2"] * 0.002
lp_data["Center3_shipping_cost"] = lp_data["Center 3"] * 0.002

lp_data["Center1_total_cost"] = lp_data["Center1_shipping_cost"] +1.5
lp_data["Center2_total_cost"] = lp_data["Center2_shipping_cost"] +1.5
lp_data["Center3_total_cost"] = lp_data["Center3_shipping_cost"] +1.5
lp_data


# In[59]:


#Cost matrix
cost_matrix = lp_data[['Center1_total_cost','Center2_total_cost','Center3_total_cost']].to_numpy().transpose()
cost_matrix


# In[60]:


#Part 2
#LP
#build the model
m = Model()

#create variables
x = m.addVars(3,51,lb= 0.0, ub=GRB.INFINITY,vtype=GRB.CONTINUOUS,name="x")

#get the objective function

obj = quicksum(cost_matrix[i][j]*x[i,j] for i in range(3) for j in range(51))
        
m.setObjective(obj, GRB.MINIMIZE)

# Add constraints
#demand
for j in range(51):
    con1 = m.addConstr(sum(x[i,j] for i in range(3)) >= demand_list[j])

     #m.addConstr(x.sum('*',j) >= demand_list[j], name= "demand")

    
#supply
for i in range(3):
    con2 = m.addConstr(sum(x[i,j] for j in range(51)) <= supply_list[i])

     #m.addConstr(x.sum(i,'*') <= supply_list[i], name = "supply")
    
 # Optimize model
m.optimize()


# In[118]:


print('Obj: %g' % m.objVal)


# In[119]:


for v in m.getVars():
    print('%s %g' % (v.varName, v.x))


# In[ ]:


#Sensitivity Report


# In[61]:


#get the objective coefficient sensitivity information
for v in m.getVars():
    print('Coeff Upper Bound', v.varName, v.SAObjUp)


# In[62]:


#get the objective coefficient sensitivity information
for v in m.getVars():
    print('Coeff Lower Bound', v.varName, v.SAObjLow)


# In[122]:


#get the RHS sensitivity information


# In[63]:


#shadow price
for con in m.getConstrs():
    print('Shadow Price',con.Pi)


# In[64]:


#RHS bound
for con in m.getConstrs():
    print('Lower Range for constraint',con.SARHSLow)


# In[65]:


#RHS bound
for con in m.getConstrs():
    print('Upper Range for constraint',con.SARHSUp)


# In[72]:


#RHS bound
for con in m.getConstrs():
    print('Allowable RHS Increase',con.SARHSUp-con.RHS)


# In[71]:


#RHS bound
for con in m.getConstrs():
    print('Allowable RHS Decrease',con.RHS-con.SARHSLow)


# In[67]:


#RHS bound
for con in m.getConstrs():
    print('RHS Coeff',con.RHS)


# In[ ]:




