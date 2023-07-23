Readme - Transportation Network Optimization with MILP

Objective:
The objective of this case study is to optimize a transportation network by identifying a set of hub nodes and assigning the remaining nodes as spokes to these hubs. The goal is to minimize the total cost of the network, considering both fixed and variable costs associated with transportation or communication.

Problem Description:

The transportation network consists of a set of nodes, each capable of acting as both an origin and a destination.
Nodes are fixed in their locations, and each spoke must be connected to one hub.
Hubs are connected using a non-directed tree structure, ensuring no cycles are allowed.
Each hub has a set price to choose from, and each link has a connection fee to be included in the solution.
The decision variables include Ykl, which is equal to 1 if arc(k,l) links two hubs; 0 otherwise, Zik, which is equal to 1 if spoke I is allocated to hub k; 0 otherwise, and Xikl, representing the amount of flow with origin in i ∈ N traversing arc (k, l).
Modeling as MILP:
The problem can be formulated as a Mixed-Integer Linear Programming (MILP) model. The decision variables and the objective function are defined as follows:

Decision Variables:

Ykl: Binary variable representing whether arc (k, l) links two hubs (1) or not (0).
Zik: Binary variable representing whether spoke I is allocated to hub k (1) or not (0). When i=k, the variable Zik represents whether a hub is located at node k.
Xikl: Continuous variable representing the amount of flow with origin in node i traversing arc (k, l).
Objective Function:
The objective function is to minimize the total cost, which is the sum of the total fixed cost and the total variable cost.

Total Fixed Cost: Σk∈N fk * Zkk
Total Variable Cost: Σi∈N Σk∈N (Cki * Oi + Cki * Di) * Zik + Σi∈N Σk∈N Σl∈N(l≠k) * Ckl * Xikl
Objective Function:
Z = Σk∈N fk * Zkk + Σi∈N Σk∈N (Cki * Oi + Cki * Di) * Zik + Σi∈N Σk∈N Σl∈N(l≠k) * Ckl * Xikl

Solution Approach:
To solve the MILP model, appropriate solvers like CPLEX, Gurobi, or SCIP can be used. These solvers can efficiently handle large-scale MILP problems and provide optimal or near-optimal solutions.

Instructions:

Install the required libraries or solvers needed to execute the MILP model in Python.
If using the LP file, input the LP file to the preferred solver and run the optimization.
If using the Python script, ensure that the required input data is provided in an appropriate format (e.g., CSV file).
Execute the Python script to obtain the optimized solution for the transportation network problem.
Note:

The MILP model formulation and Python script provided here are for illustrative purposes. The actual implementation may vary depending on the specific problem and data requirements.
Make sure to adhere to the licensing and usage terms of the solver and libraries employed in the project.
Feel free to modify the MILP model or the Python script as needed to fit specific problem constraints or to add additional features.
References:
[Provide any references or academic papers that inspired or provided insights into the MILP formulation for the transportation network optimization problem.]