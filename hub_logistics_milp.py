# Hub Logistics Problem

# The goal of this Jupyter notebook is to find the optimal solution to solve the Hub logistics problem by applying the MILP model to the InputDataHubSmallInstance dataset.

# Consider a transportation/telecommunication network that contains a set of
# origin/destination nodes and the need of transferring a flow between each
# pair of origin-destination (O-D) nodes. Each node can be an origin or a
# destination at the same time. The aim is to locate a set of nodes as hubs
# and to allocate the remaining nodes (spokes) to the located hub to minimize
# the network’s total cost (i.e., fixed and variable costs).


!pip install pulp

# Imports of modules
# Below we import the pulp module necessary to make this code work properly.

from pulp import *
import pandas as pd
import numpy as np
from itertools import product

if __name__ == "__main__":

   InputData = "InputDataHubSmallInstance.xlsx"

  # Input Data Preparation
   def read_excel_data(InputData, sheet_name):
      data = pd.read_excel(InputData, sheet_name=sheet_name, header=None)
      values = data.values
      if min(values.shape) == 1:  # This If is to make the code insensitive to column-wise or row-wise expression #
          if values.shape[0] == 1:
              values = values.tolist()
          else:
              values = values.transpose()
              values = values.tolist()
          return values[0]
      else:
          data_dict = {}
          if min(values.shape) == 2:  # For single-dimension parameters in Excel
              if values.shape[0] == 2:
                  for i in range(values.shape[1]):
                      data_dict[i+1] = values[1][i]
              else:
                  for i in range(values.shape[0]):
                      data_dict[i+1] = values[i][1]

          else:  # For two-dimension (matrix) parameters in Excel
              for i in range(values.shape[0]):
                  for j in range(values.shape[1]):
                      data_dict[(i+1, j+1)] = values[i][j]
          return data_dict

   # This section reads the data from Excel

   # Read a set (set is the name of the worksheet)
   # The set has eight elements
   NodeNum = read_excel_data(InputData, "NodeNum")
   print("NodeNum: ", NodeNum)

   flow_wij = read_excel_data(InputData, "flow(wij)")
   print("flow(wij): ", flow_wij)

   varCost_cij = read_excel_data(InputData, "varCost(cij)")
   print("varCost(cij): ", varCost_cij)

   fixCost_fk = read_excel_data(InputData, "fixCost(fk)")
   print("fixCost(fk): ", fixCost_fk)

   alpha = read_excel_data(InputData, "alpha")
   print("alpha: ", alpha)

   ckmax = read_excel_data(InputData, "Cap(ckmax)")
   print("Cap(ckmax): ", ckmax)

   N = []
   for i in range(NodeNum[0]):
    N.append(i+1)
   print("N=",N)


# Creating the LP model

# Create the decision variables
# Ykl = 1 if arc (k; l) links two hubs; 0 otherwise.
y_var = LpVariable.dicts('y', (N, N), 0, 1, "Binary")
# Zik = 1 if the spoke i is allocated to the hub k; 0 otherwise.
z_var = LpVariable.dicts('z', (N, N), 0, 1, "Binary")
# Xikl = the amount of flow with origin in i 2 N traversing arc (k; l)
x_var = LpVariable.dicts('x', (N, N, N), 0)

# Create the 'hub_select' variable to contain the problem data
problem = LpProblem("Hub_Logistics", LpMinimize)

# Total flow originating from node i
O={}
total_src_flow = 0
for i in N:
  for key, value in flow_wij.items():
    if key[0]==i:
      total_src_flow += flow_wij[key]
  O[i] = total_src_flow
  total_src_flow = 0
print(O)

# Total flow destinating in node i
D={}
total_des_flow = 0
for j in N:
  for key, value in flow_wij.items():
    if key[1]==j:
      total_des_flow += flow_wij[key]
  D[j] = total_des_flow
  total_des_flow = 0
print(D)

# The objective function
# Total cost = Fixed cost + Variable cost

# The fixed cost
fixed_cost= lpSum([fixCost_fk[k-1]*z_var[k][k]for k in N])
print(fixed_cost)

# The variable cost which is computed based on the amount of flow
var_cost_1 = 0
for i in N:
  for k in N:
    for key, value in varCost_cij.items():
      if (i,k) == key:
        var_cost_1 += ((varCost_cij[key]*O[i])+(varCost_cij[tuple(reversed(key))]*D[i]))*z_var[i][k]

# The variable cost which is applied the discount
var_cost_2 = 0
for i in N:
  for k in N:
    for l in N:
      if l != k:
        for key, value in varCost_cij.items():
          if (l,k) == key:
            var_cost_2 += alpha[0]*varCost_cij[key]*x_var[i][k][l]

# The objective function
problem += fixed_cost + var_cost_1 + var_cost_2

# Constraints
# Constrain 1: Each node is allocated to exactly one hub
for i in N:
    problem += lpSum([z_var[i][k] for k in N]) == 1

# Constrain 2: If node i is allocated to hub k, then hub k is active
for l, k in product(N, N):
  if l > k:
    problem += z_var[k][l] + y_var[k][l] <= z_var[l][l]

for l, k in product(N, N):
  if l > k:
    problem += z_var[l][k] + y_var[l][k] <= z_var[k][k]

# Constrain 3: Transit of flow through the tree
for i in N:
  for k in N:
    for l in N:
      if l > k:
        problem += x_var[i][k][l] + x_var[i][l][k] <= O[i] * y_var[k][l]

# Constrain 4: Flow conservation constraint
for k in N:
  for i in N:
    if k != i:
      problem += O[i] * z_var[i][k] + lpSum([x_var[i][k][l] for l in N if k != l]) == lpSum([x_var [i][l][k] for l in N if k!=l]) + lpSum([flow_wij[key]*z_var[l][k] for l in N for key, value in flow_wij.items() if (i,l) == key])

# Constrain 5: Capacity constraint for each hub
for k in N:
   problem += lpSum([O[i] * z_var[i][k] for i in N]) + lpSum([x_var[i][l][k] for i in N for l in N]) <= ckmax[k-1]

# Constrain 6: Tree structure
problem += lpSum([y_var[k][l] for k in N for l in N]) == lpSum([z_var[k][k] for k in N])-1

# Solving the LP model with the default solver of PuLP

# The problem is solved using PuLP's choice of Solver
# (the default solver is Coin Cbc)
problem.solve()

# Printing the status of the solution, the optimal values of the variables and the value of the objective function

# The status of the solution is printed to the screen
print("Status:", LpStatus[problem.status])
from IPython.utils import io



# The optimal value of the decision variables is saved and the optimised objective function value is printed to the screen
for v in problem.variables():
  with io.capture_output() as captured:
    print(v.name, "=", v.varValue);

print ("Objective value of hub logistics = ", problem.objective.value())

for v in problem.variables():
  if v.varValue != 0.0:
     with io.capture_output() as captured:
      print(v.name, "=", v.varValue)

import networkx as nx
import matplotlib.pyplot as plt

# Create an empty graph
G = nx.Graph()

# Define the hubs (squares)
hubs = [1, 2, 4, 6]

# Add hubs as nodes with square shape
G.add_nodes_from(hubs)

# Define the nodes (circles)
nodes = [3, 5, 7, 8]

# Add nodes as nodes with default shape
G.add_nodes_from(nodes)

# Define the edges
edges = [(1, 6), (2, 4), (2, 6), (5, 1), (3, 2), (7, 2), (8, 6)]

# Add edges to the graph
G.add_edges_from(edges)

# Create a layout for the graph
pos = nx.spring_layout(G)

# Draw the hubs and nodes with different shapes and colours
nx.draw_networkx_nodes(G, pos, nodelist=hubs, node_shape='s', node_color='lightblue', node_size=1000)
nx.draw_networkx_nodes(G, pos, nodelist=nodes, node_shape='o', node_color='lightpink', node_size=1000)

# Draw the edges
nx.draw_networkx_edges(G, pos)

# Add labels to the nodes
nx.draw_networkx_labels(G, pos)

# Display the graph
plt.axis('off')
plt.show()

